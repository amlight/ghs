#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import Counter
from typing import List, Optional

import httpx

from .base import base_url, headers


def _build_args(dict_args, kv_sep="=", arg_sep="&") -> str:
    """Build query search args."""
    return arg_sep.join([f"{k}{kv_sep}{v}" for k, v in dict_args.items()])


def _priority_to_int(priority: str) -> int:
    """Get an int given a priority."""
    priorities = {
        "priority_critical": 90,
        "priority_major": 70,
        "priority_medium": 50,
        "priority_low": 30,
    }
    return priorities.get(priority, 0)


def _find_priority(labels: List[str]) -> Optional[str]:
    """Find a priority value given label names."""
    prio = {label: label for label in labels if label.startswith("priority")}
    return (
        prio.get("priority_critical")
        or prio.get("priority_major")
        or prio.get("priority_medium")
        or prio.get("priority_low")
    )


def _map_search_item(item: dict) -> dict:
    """Map a search item."""
    labels = [label.get("name") for label in item.get("labels", [])]
    priority = _find_priority(labels)
    return {
        "title": item.get("title"),
        "html_url": item.get("html_url"),
        "state": item.get("state"),
        "priority": priority,
        "labels": labels,
        "created_at": item.get("created_at"),
        "closed_at": item.get("closed_at"),
    }


async def _search(**kwargs) -> dict:
    """Search issues and PRs."""
    # TODO handle pagination
    url_args = _build_args(kwargs, kv_sep=":", arg_sep="+")
    url = f"{base_url()}/search/issues?q={url_args}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers())
        r.raise_for_status()
        return r.json()


async def search(**kwargs) -> str:
    """Search issues and PRs."""
    response = await _search(**kwargs)
    items = [_map_search_item(item) for item in response.get("items")]
    items = sorted(
        items, key=lambda x: _priority_to_int(x.get("priority")), reverse=True
    )
    counter = Counter([item.get("state") for item in items])
    open_items = counter.get("open", 0)
    closed_items = counter.get("closed", 0)
    progress = closed_items / open_items if open_items else 0
    stats = {"open": open_items, "closed": closed_items, "progress": progress}
    return json.dumps({"items": items, "stats": stats}, sort_keys=True, indent=4)
