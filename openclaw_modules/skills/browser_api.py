#!/usr/bin/env python3
"""
Browser API - 极简版
"""

import requests

def visit_page(url: str) -> dict:
    """访问页面并返回结果"""
    r = requests.get(
        "http://localhost:8000/visit",
        params={"url": url},
        timeout=60
    )
    return r.json()


# 使用示例
if __name__ == "__main__":
    print(visit_page("https://github.com"))
