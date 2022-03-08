#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def base_url() -> str:
    return "https://api.github.com"


def token(token="") -> str:
    return token or os.environ.get("GH_TOKEN", "")


def headers() -> dict:
    headers = {}
    if token():
        headers["Authorization"] = f"token {token()}"
    return headers
