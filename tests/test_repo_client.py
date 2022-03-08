#!/usr/bin/env python
# -*- coding: utf-8 -*-

import respx
from httpx import Response

from ghs.base import base_url
from ghs.repo_client import org_repos, org_repos_by_attr


async def test_org_repos(respx_mock, repos_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )
        response = await org_repos(org)
        assert len(response) == len(repos_data)


async def test_org_repos_by_attr(respx_mock, repos_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )
        response = await org_repos_by_attr(org, "name")
        names = [repo.get("name") for repo in repos_data]
        assert response == names


async def test_org_repos_by_attr_included_repos(respx_mock, repos_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )

        included_repos = ["non_existent"]
        response = await org_repos_by_attr(org, "name", included_repos)
        assert not len(response)

        included_repos = ["kytos"]
        response = await org_repos_by_attr(org, "name", included_repos)
        assert len(response) == 1
        assert response[0] == repos_data[0]["name"]
