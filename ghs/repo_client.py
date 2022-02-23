#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, List, Optional, Union

import httpx

from .base import base_url, headers


async def org_repos(org: str) -> List[dict]:
    """List org repos."""
    url = f"{base_url()}/orgs/{org}/repos"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers())
        r.raise_for_status()
        repos = r.json()
        return [repo for repo in repos if not repo.get("archived")]


async def org_repos_by_attr(
    org: str, by_attr: str, included_repos: Optional[List[str]] = None
) -> List[Any]:
    """List org repos by attr."""
    repos = [repo.get(by_attr) for repo in await org_repos(org)]
    if included_repos is not None:
        repos = [repo for repo in repos if repo in included_repos]
    return repos


async def add_labels(
    owner: str, repo: str, issue_number: Union[int, str], labels: List[str]
) -> dict:
    """Add a list of labels on a repo."""
    url = f"{base_url()}/repos/{owner}/{repo}/issues/{issue_number}/labels"
    async with httpx.AsyncClient() as client:
        r = await client.post(
            url, headers=headers(), json=[str(label) for label in labels]
        )
        return {"status_code": r.status_code, "response": r.json()}
