#!/usr/bin/env python3
"""
L2 结构化清洗层 (无依赖版本)
去导航栏、去广告、去重复内容，只保留文章主体
"""

import json
import os
import re
from datetime import datetime

L1_DIR = "knowledge/L1_raw"
L2_DIR = "knowledge/L2_clean"

# 需要移除的HTML标签
REMOVE_PATTERNS = [
    r'<script[^>]*>.*?</script>',
    r'<style[^>]*>.*?</style>',
    r'<nav[^>]*>.*?</nav>',
    r'<header[^>]*>.*?</header>',
    r'<footer[^>]*>.*?</footer>',
    r'<aside[^>]*>.*?</aside>',
    r'<iframe[^>]*>.*?</iframe>',
    r'<form[^>]*>.*?</form>',
    r'<button[^>]*>.*?</button>',
    r'<noscript[^>]*>.*?</noscript>',
    r'class="[^"]*nav[^"]*"',
    r'class="[^"]*header[^"]*"',
    r'class="[^"]*footer[^"]*"',
    r'class="[^"]*menu[^"]*"',
    r'class="[^"]*sidebar[^"]*"',
    r'class="[^"]*ad[^"]*"',
    r'class="[^"]*advertisement[^"]*"',
    r'class="[^"]*popup[^"]*"',
    r'class="[^"]*modal[^"]*"',
    r'id="[^"]*nav[^"]*"',
    r'id="[^"]*header[^"]*"',
    r'id="[^"]*footer[^"]*"',
    r'id="[^"]*sidebar[^"]*"',
]

def clean_html(html_content):
    """清洗HTML，提取主体内容"""
    if not html_content:
        return ""
    
    text = html_content
    
    # 移除脚本和样式
    for pattern in REMOVE_PATTERNS:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 提取 body 内容
    body_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL | re.IGNORECASE)
    if body_match:
        text = body_match.group(1)
    
    # 移除HTML标签，保留文本
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # 清理空白
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 限制长度
    return text[:50000]

def extract_title(html_content):
    """提取标题"""
    match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_description(html_content):
    """提取描述"""
    match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def process_source(source_name):
    """处理单个来源"""
    l1_file = f"{L1_DIR}/{source_name}/2026-03-02.json"
    
    if not os.path.exists(l1_file):
        print(f"   ⚠️ 文件不存在")
        return None
    
    with open(l1_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html_content = data.get("content", {}).get("html_preview", "")
    
    if not html_content:
        return None
    
    # 清洗
    cleaned = clean_html(html_content)
    meta = data.get("metadata", {})
    
    result = {
        "source": source_name,
        "original_url": meta.get("url", ""),
        "original_hash": meta.get("hash", ""),
        "cleaned_at": datetime.now().isoformat(),
        "title": data.get("content", {}).get("title", ""),
        "description": data.get("content", {}).get("description", ""),
        "cleaned_content": cleaned,
        "content_length": len(cleaned)
    }
    
    return result

def save_cleaned(source, data):
    """保存清洗后的内容"""
    os.makedirs(f"{L2_DIR}/{source}", exist_ok=True)
    
    filename = f"{L2_DIR}/{source}/2026-03-02.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename

def main():
    print("=" * 60)
    print("🧹 L2 结构化清洗层")
    print("=" * 60)
    
    sources = ["real_python", "w3schools", "geeksforgeeks", "kaggle"]
    
    for source in sources:
        print(f"\n📥 清洗: {source}...")
        
        result = process_source(source)
        
        if result:
            filename = save_cleaned(source, result)
            print(f"   ✅ 已保存: {filename}")
            print(f"   📏 清洗后长度: {result['content_length']:,} chars")
        else:
            print(f"   ❌ 失败")
    
    print("\n" + "=" * 60)
    print("✅ L2 清洗完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()
