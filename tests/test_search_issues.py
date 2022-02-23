#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import respx
from httpx import Response

from ghs.base import base_url
from ghs.search_client import search, search_issues_add_labels


async def test_search(respx_mock, search_issues_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        query_args = (
            "q=org:kytos-ng+org:amlight+label:epic_nosql_db&page=1&per_page=100"
        )
        respx_mock.get(f"/search/issues?{query_args}").mock(
            return_value=Response(200, json=search_issues_data)
        )
        response = await search("org:kytos-ng org:amlight label:epic_nosql_db")
        response = json.loads(response)
        assert len(response.get("items")) == len(search_issues_data.get("items"))


async def test_search_issues_add_labels(
    respx_mock, repo_labels_data, search_issues_data
) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        query_args = (
            "q=org:kytos-ng+org:amlight+label:epic_nosql_db&page=1&per_page=100"
        )
        respx_mock.get(f"/search/issues?{query_args}").mock(
            return_value=Response(200, json=search_issues_data)
        )

        for issue in search_issues_data.get("items"):
            url = issue.get("url").split("/")
            owner = url[-4]
            repo = url[-3]
            issue_number = url[-1]
            respx_mock.post(f"/repos/{owner}/{repo}/issues/{issue_number}/labels").mock(
                return_value=Response(200, json=repo_labels_data)
            )

        query_expr = "org:kytos-ng org:amlight label:epic_nosql_db"
        labels = [label.get("name") for label in repo_labels_data]
        response = await search_issues_add_labels(query_expr, labels)
        assert len(search_issues_data.get("items")) == len(response.keys())
