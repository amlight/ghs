#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import respx
from httpx import Response

from ghs.base import base_url
from ghs.label_client import (
    org_repos_labels,
    org_repos_labels_create,
    org_repos_labels_delete,
    org_repos_priority_labels_create,
    repo_label_create,
    repo_label_delete,
    repo_labels,
    repo_labels_by_attr,
    repo_labels_delete,
    repo_priority_labels_create,
)


async def test_repo_labels(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"
        respx_mock.get(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data)
        )
        response = await repo_labels(owner, repo)
        assert len(response) == len(repo_labels_data)


async def test_repo_labels_by_attr(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"
        respx_mock.get(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data)
        )
        attr = "name"
        response = await repo_labels_by_attr(owner, repo, attr)
        assert len(response) == 3
        assert [label.get(attr) for label in repo_labels_data] == response

        included_labels = ["documentation"]
        response = await repo_labels_by_attr(owner, repo, attr, included_labels)
        assert response == included_labels


async def test_repo_label_delete(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"
        label = "documentation"
        respx_mock.delete(f"/repos/{owner}/{repo}/labels/{label}").mock(
            return_value=Response(200, json=repo_labels_data)
        )
        response = await repo_label_delete(owner, repo, label)
        assert response == 200


async def test_repo_labels_delete(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"
        labels = ["documentation", "blueprint"]

        respx_mock.get(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data)
        )
        for label in labels:
            respx_mock.delete(f"/repos/{owner}/{repo}/labels/{label}").mock(
                return_value=Response(200, json=repo_labels_data)
            )
        response = await repo_labels_delete(owner, repo, labels)
        assert response == {label: 200 for label in labels}

        with pytest.raises(ValueError) as e:
            response = await repo_labels_delete(owner, repo, [])
        assert "labels need to be explicitly set" in str(e)


async def test_repo_label_create(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"
        label = "2022.2.0"
        description = f"Kytos-ng version {label}"

        repo_labels_data[0]["label"] = label
        repo_labels_data[0]["description"] = description
        respx_mock.post(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data[0])
        )
        response = await repo_label_create(owner, repo, label, description)
        assert response == {"status_code": 200, "response": repo_labels_data[0]}


async def test_repo_priority_labels_create(respx_mock, repo_labels_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        owner = "kytos-ng"
        repo = "flow_manager"

        priority_labels = {
            "priority_critical": {
                "color": "B60205",
                "description": "Critical priority",
            },
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
        respx_mock.get(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data)
        )
        respx_mock.post(f"/repos/{owner}/{repo}/labels").mock(
            return_value=Response(200, json=repo_labels_data[0])
        )

        response = await repo_priority_labels_create(owner, repo)
        assert len(response) == len(priority_labels)


async def test_org_repos_labels(respx_mock, repo_labels_data, repos_data) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )
        repos = [repo.get("name") for repo in repos_data]
        for repo in repos:
            respx_mock.get(f"/repos/{org}/{repo}/labels").mock(
                return_value=Response(200, json=repo_labels_data)
            )

        response = await org_repos_labels(org)
        assert repos == list(response.keys())


async def test_org_repos_labels_delete(
    respx_mock, repo_labels_data, repos_data
) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )
        repos = [repo.get("name") for repo in repos_data]
        labels = [label.get("name") for label in repo_labels_data]
        for repo in repos:
            respx_mock.get(f"/repos/{org}/{repo}/labels").mock(
                return_value=Response(200, json=repo_labels_data)
            )
            for label in labels:
                respx_mock.delete(f"/repos/{org}/{repo}/labels/{label}").mock(
                    return_value=Response(200, json=repo_labels_data)
                )

        response = await org_repos_labels_delete(org, labels)
        assert repos == list(response.keys())


async def test_org_repos_priority_labels_create(
    respx_mock, repo_labels_data, repos_data
) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )

        repos = [repo.get("name") for repo in repos_data]
        for repo in repos:
            respx_mock.get(f"/repos/{org}/{repo}/labels").mock(
                return_value=Response(200, json=repo_labels_data)
            )
            respx_mock.post(f"/repos/{org}/{repo}/labels").mock(
                return_value=Response(200, json=repo_labels_data[0])
            )

        response = await org_repos_priority_labels_create(org)
        assert repos == list(response.keys())


async def test_org_repos_labels_create(
    respx_mock, repo_labels_data, repos_data
) -> None:
    with respx.mock(base_url=base_url()) as respx_mock:
        org = "kytos-ng"
        respx_mock.get(f"/orgs/{org}/repos").mock(
            return_value=Response(200, json=repos_data)
        )

        repos = [repo.get("name") for repo in repos_data]
        for repo in repos:
            respx_mock.post(f"/repos/{org}/{repo}/labels").mock(
                return_value=Response(200, json=repo_labels_data[0])
            )

        name = repo_labels_data[0]["name"]
        response = await org_repos_labels_create(org, name)
        assert repos == list(response.keys())
