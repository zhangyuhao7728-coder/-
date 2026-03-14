#!/usr/bin/env python3
"""
手机阅读版格式化
"""
import re

def format_mobile(md_text: str) -> str:
    """Markdown转手机阅读版HTML"""
    # 这个工具在 tools/转手机版.py 中已有实现
    # 这里只是引用
    from tools.手机版 import convert
    return convert(md_text)
