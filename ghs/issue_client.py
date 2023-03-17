#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from typing import List

import httpx

from .base import base_url, headers
from .repo_client import org_repos_by_attr


async def repo_issue_create(
    owner: str,
    repo: str,
    title: str,
    body: str = "",
    assignees: List[str] = None,
    labels: List[str] = None,
) -> dict:
    """Create an issue in a repository."""
    assignees = assignees if assignees else []
    labels = labels if labels else []
    url = f"{base_url()}/repos/{owner}/{repo}/issues"
    async with httpx.AsyncClient() as client:
        r = await client.post(
            url,
            headers=headers(),
            json={
                "title": title,
                "body": body,
                "assignees": assignees,
                "labels": labels,
            },
        )
        r.raise_for_status()
        rbody = r.json()
        return {
            "number": rbody.get("number"),
            "title": rbody.get("title"),
            "html_url": rbody.get("html_url"),
        }


async def org_repos_issue_create(
    org: str,
    title: str,
    body: str = "",
    assignees: List[str] = None,
    labels: List[str] = None,
    included_repos: List[str] = None,
):
    """Create an issue in repos of an org."""
    repos = await org_repos_by_attr(org, "name", included_repos)
    coros = [
        repo_issue_create(org, repo, title, body, assignees, labels) for repo in repos
    ]
    results = await asyncio.gather(*coros)
    return {repo: result for repo, result in zip(repos, results)}
