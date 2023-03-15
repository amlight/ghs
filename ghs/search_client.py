#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import math
from collections import Counter
from typing import List, Optional

import httpx
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random,
)

from .base import base_url, headers
from .label_client import add_labels


def _build_args(dict_args, kv_sep="=", arg_sep="&") -> str:
    """Build URL args."""
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
        "number": item.get("number"),
        "title": item.get("title"),
        "html_url": item.get("html_url"),
        "state": item.get("state"),
        "priority": priority,
        "labels": labels,
        "created_at": item.get("created_at"),
        "closed_at": item.get("closed_at"),
        "assignee": item.get("assignee"),
    }


async def _search(query_expr: str, page=1, per_page=100) -> dict:
    """Search issues and PRs."""
    url_args = "+".join(query_expr.split(" "))
    page_args = _build_args({"page": page, "per_page": per_page}, "=", "&")
    url = f"{base_url()}/search/issues?q={url_args}&{page_args}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers())
        r.raise_for_status()
        return r.json()


def _map_search_response(items: List[dict]) -> str:
    """Map search reponse."""
    items = sorted(
        items, key=lambda x: _priority_to_int(x.get("priority")), reverse=True
    )
    counter = Counter([item.get("state") for item in items])
    open_items = counter.get("open", 0)
    closed_items = counter.get("closed", 0)
    progress = closed_items / len(items) if len(items) else 0
    stats = {
        "open": open_items,
        "closed": closed_items,
        "progress": progress,
    }
    return json.dumps(
        {
            "items": items,
            "stats": stats,
            "partial_results": True if len(items) == 1000 else False,
        },
        sort_keys=True,
        indent=4,
    )


async def search(
    query_expr: str, max_retries: int = 3, min_retry_wait: int = 65
) -> str:
    """Search issues and PRs, the query_expr is an expression that GitHub search
    supports such as 'org:some_org label:some_label'."""
    try:
        async for attempt in AsyncRetrying(
            retry=retry_if_exception_type((httpx.HTTPStatusError,)),
            wait=wait_random(min_retry_wait, min_retry_wait + 5),
            stop=stop_after_attempt(max_retries),
        ):
            with attempt:
                response = await _search(query_expr)
                items = [_map_search_item(item) for item in response.get("items")]
                per_page = 100

                remaining_pages = min(
                    math.ceil(
                        (int(response.get("total_count")) - len(items)) / per_page
                    ),
                    9,
                )
                coros = [
                    _search(query_expr, page=page, per_page=per_page)
                    for page in range(2, 2 + remaining_pages)
                ]
                for response in await asyncio.gather(*coros):
                    for item in response.get("items"):
                        items.append(_map_search_item(item))
                return _map_search_response(items)
    except RetryError:
        raise


async def search_issues_add_labels(query_expr: str, labels: List[str]) -> dict:
    """Add labels to issues given a search query_expr"""
    results = await search(query_expr)
    results = json.loads(results)
    coros = []
    ids = []
    for result in results.get("items", []):
        number = result.get("number")
        html_url = result.get("html_url", "").split("/")
        owner, repo = html_url[-4], html_url[-3]
        coros.append(add_labels(owner, repo, number, labels))
        ids.append(result.get("html_url"))
    results = await asyncio.gather(*coros)
    return {key: result.get("status_code") for key, result in zip(ids, results)}
