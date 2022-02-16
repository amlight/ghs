#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

import pytest

from tests.data import repo_labels_data as _repo_labels_data
from tests.data import repos_data as _repos_data


@pytest.fixture
def repos_data() -> List[dict]:
    return _repos_data()


@pytest.fixture
def repo_labels_data() -> List[dict]:
    return _repo_labels_data()
