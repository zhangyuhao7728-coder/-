#!/usr/bin/env python3
"""
自动抓取任务执行器 - 版本化存储
数据采集层 (L1) -> 结构化清洗层 (L2)
"""

import json
import requests
from datetime import datetime
import os
import re
import hashlib

CONFIG_FILE = "config/scrape_tasks.json"
OUTPUT_DIR = "knowledge/L1_raw"

# 来源映射
SOURCE_MAP = {
    "realpython.com": "real_python",
    "w3schools.com": "w3schools", 
    "geeksforgeeks.org": "geeksforgeeks",
    "kaggle.com": "kaggle"
}

def load_tasks():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data.get("tasks", [])

def get_source(url):
    """从URL提取来源"""
    for domain, source in SOURCE_MAP.items():
        if domain in url:
            return source
    return "unknown"

def compute_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def extract_info(html, url):
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.I)
    title = title_match.group(1) if title_match else url
    
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
    desc = desc_match.group(1) if desc_match else ""
    
    h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.I)
    h1_tags = [h.strip() for h in h1_matches[:3]]
    
    return {"title": title.strip(), "description": desc[:200], "h1_tags": h1_tags}

def scrape_site(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=30, verify=False)
        resp.encoding = 'utf-8'
        
        info = extract_info(resp.text, url)
        content_hash = compute_hash(resp.text)
        
        return {
            "status": "success",
            "title": info["title"],
            "description": info["description"],
            "h1_tags": info["h1_tags"],
            "content": resp.text[:50000],
            "content_hash": content_hash,
            "content_length": len(resp.text),
            "url": url
        }
    except Exception as e:
        return {"status": "failed", "error": str(e), "url": url}

def save_versioned(task, result):
    source = get_source(task.get("url", ""))
    source_dir = f"{OUTPUT_DIR}/{source}"
    os.makedirs(source_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{source_dir}/{date_str}.json"
    
    metadata = {
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "hash": result.get("content_hash", ""),
        "content_length": result.get("content_length", 0),
        "task_type": task.get("task_type", "scrape"),
        "scrape_depth": task.get("scrape_depth", 1),
        "url": task.get("url", "")
    }
    
    data = {
        "metadata": metadata,
        "content": {
            "title": result.get("title", ""),
            "description": result.get("description", ""),
            "h1_tags": result.get("h1_tags", []),
            "html_preview": result.get("content", "")[:10000]
        }
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return filename, metadata

def run_scrape_tasks():
    tasks = load_tasks()
    
    print("=" * 60)
    print("🐍 Python 学习网站 - 版本化抓取 (L1)")
    print("=" * 60)
    
    for task in tasks:
        url = task.get("url", "")
        source = get_source(url)
        
        print(f"\n📥 {source}: {url}...")
        
        result = scrape_site(url)
        
        if result["status"] == "success":
            filename, metadata = save_versioned(task, result)
            print(f"   ✅ {filename}")
            print(f"   📊 Hash: {metadata['hash'][:16]}...")
            print(f"   📏 {metadata['content_length']:,} bytes")
        else:
            print(f"   ❌ {result.get('error', '')[:50]}")
    
    print("\n" + "=" * 60)
    print("✅ L1 数据采集完成!")
    print("=" * 60)

if __name__ == "__main__":
    run_scrape_tasks()
