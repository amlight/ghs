#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from typing import Any, Dict, List, Optional

import httpx

from .base import base_url, headers
from .repo_client import org_repos_by_attr


async def repo_labels(owner: str, repo: str) -> List[dict]:
    """List repo labels."""
    url = f"{base_url()}/repos/{owner}/{repo}/labels"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers())
        r.raise_for_status()
        return r.json()


async def repo_labels_by_attr(
    owner: str, repo: str, by_attr: str, included_labels: Optional[List[str]] = None
) -> List[Any]:
    """List repo labels by attr."""
    labels = [label.get(by_attr) for label in await repo_labels(owner, repo)]
    if included_labels is not None:
        labels = [label for label in labels if label in included_labels]
    return labels


async def repo_label_delete(owner: str, repo: str, label: str) -> int:
    """Delete a repo label."""
    async with httpx.AsyncClient() as client:
        url = f"{base_url()}/repos/{owner}/{repo}/labels/{label}"
        r = await client.delete(url, headers=headers())
        return r.status_code


async def repo_labels_delete(owner: str, repo: str, included_labels: List[str]) -> dict:
    """Delete labels of repo idempotently."""
    if not included_labels:
        raise ValueError("For deletion, labels need to be explicitly set")

    labels = await repo_labels_by_attr(owner, repo, "name", included_labels)
    coros = [repo_label_delete(owner, repo, label) for label in labels]
    return {
        label: result for label, result in zip(labels, await asyncio.gather(*coros))
    }


async def repo_label_create(
    owner: str,
    repo: str,
    name: str,
    description: Optional[str] = None,
    color: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a label."""
    async with httpx.AsyncClient() as client:
        url = f"{base_url()}/repos/{owner}/{repo}/labels"
        body = {"name": str(name)}
        if color:
            body["color"] = color
        if description:
            body["description"] = description

        r = await client.post(url, headers=headers(), json=body)
        return {"status_code": r.status_code, "response": r.json()}


async def repo_priority_labels_create(
    owner: str,
    repo: str,
) -> List[dict]:
    """Create priority labels."""
    priority_labels = {
        "priority_critical": {"color": "B60205", "description": "Critical priority"},
        "priority_major": {"color": "D93F0B", "description": "Major priority"},
        "priority_medium": {"color": "FEF2C0", "description": "Medium priority"},
        "priority_low": {"color": "BFDADC", "description": "Low priority"},
        "in_progress": {"color": "C2E0C6", "description": "In progress"},
        "blocked": {"color": "B60205", "description": "Blocked"},
        "future_release": {
            "color": "1D76DB",
            "description": "Planned for the next release",
        },
    }
    labels = await repo_labels_by_attr(
        owner, repo, "name", list(priority_labels.keys())
    )
    coros = [
        repo_label_create(
            owner,
            repo,
            label,
            priority_labels[label]["description"],
            priority_labels[label]["color"],
        )
        for label in priority_labels
        if label not in labels
    ]
    return await asyncio.gather(*coros)


async def org_repos_labels(
    org: str,
    included_labels: Optional[List[str]] = None,
    included_repos: Optional[List[str]] = None,
) -> dict:
    """List labels of an org indexed by their repos."""
    repos = await org_repos_by_attr(org, "name", included_repos)
    coros = [repo_labels_by_attr(org, repo, "name", included_labels) for repo in repos]
    results = await asyncio.gather(*coros)
    return {repo: result for repo, result in zip(repos, results)}


async def org_repos_labels_delete(
    org: str,
    included_labels: List[str],
    included_repos: Optional[List[str]] = None,
) -> dict:
    """Delete labels of an org."""
    repos = await org_repos_by_attr(org, "name", included_repos)
    coros = [repo_labels_delete(org, repo, included_labels) for repo in repos]
    results = await asyncio.gather(*coros)
    return {repo: result for repo, result in zip(repos, results)}


async def org_repos_labels_create(
    org: str,
    name: str,
    description: Optional[str] = None,
    color: Optional[str] = None,
    included_repos: Optional[List[str]] = None,
) -> dict:
    """Create labels in an org."""
    repos = await org_repos_by_attr(org, "name", included_repos)
    coros = [
        repo_label_create(org, repo, str(name), description, color) for repo in repos
    ]
    results = await asyncio.gather(*coros)
    return {repo: result for repo, result in zip(repos, results)}


async def org_repos_priority_labels_create(
    org: str,
    included_labels: Optional[List[str]] = None,
    included_repos: Optional[List[str]] = None,
) -> dict:
    """Create priority labels for all repos."""
    repos = await org_repos_by_attr(org, "name", included_repos)
    coros = [repo_priority_labels_create(org, repo) for repo in repos]
    results = await asyncio.gather(*coros)
    return {repo: result for repo, result in zip(repos, results)}
