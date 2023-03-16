#!/usr/bin/env python
# -*- coding: utf-8 -*-

import respx
from httpx import Response

from ghs.base import base_url
from ghs.issue_client import repo_issue_create


async def test_repo_issue_create(respx_mock, repo_issue_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "kytos"
        respx_mock.post(f"/repos/{owner}/{repo}/issues").mock(
            return_value=Response(200, json=repo_issue_data)
        )
        response = await repo_issue_create(owner, repo, "some title")
        assert response["number"] == repo_issue_data["number"]
        assert response["title"] == repo_issue_data["title"]
        assert response["html_url"] == repo_issue_data["html_url"]
