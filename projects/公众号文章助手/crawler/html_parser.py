#!/usr/bin/env python3
"""
HTML解析器
"""
def parse_html(html: str) -> dict:
    """解析HTML为纯文本"""
    # 简单实现
    import re
    # 移除脚本和样式
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # 移除标签
    text = re.sub(r'<[^>]+>', '', text)
    # 清理空白
    text = re.sub(r'\s+', ' ', text).strip()
    return {'text': text}
