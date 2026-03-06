#!/usr/bin/env python3
"""
Python 学习网站抓取任务
"""

import requests
from bs4 import BeautifulSoup
import json
import time

# 学习网站列表
SITES = [
    {"name": "Real Python", "url": "https://realpython.com/", "category": "教程"},
    {"name": "W3Schools Python", "url": "https://www.w3schools.com/python/", "category": "教程"},
    {"name": "GeeksforGeeks Python", "url": "https://www.geeksforgeeks.org/python-programming-language/", "category": "算法"},
    {"name": "Kaggle Python", "url": "https://www.kaggle.com/learn/python", "category": "数据科学"},
]

def scrape_site(site):
    """抓取单个网站"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(site["url"], headers=headers, timeout=30)
        resp.encoding = 'utf-8'
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 提取标题
        title = soup.title.string if soup.title else site["name"]
        
        # 提取描述
        desc = ""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta:
            desc = meta.get('content', '')[:200]
        
        return {
            "name": site["name"],
            "url": site["url"],
            "category": site["category"],
            "status": "success",
            "title": title.strip(),
            "description": desc,
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "name": site["name"],
            "url": site["url"],
            "category": site["category"],
            "status": "failed",
            "error": str(e),
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

def main():
    print("=" * 50)
    print("🐍 Python 学习网站抓取任务")
    print("=" * 50)
    
    results = []
    for site in SITES:
        print(f"\n📥 正在抓取: {site['name']}...")
        result = scrape_site(site)
        results.append(result)
        
        if result["status"] == "success":
            print(f"   ✅ 成功: {result['title'][:50]}")
        else:
            print(f"   ❌ 失败: {result['error'][:50]}")
        
        time.sleep(1)  # 避免请求过快
    
    # 保存结果
    output = {
        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(SITES),
        "success": sum(1 for r in results if r["status"] == "success"),
        "sites": results
    }
    
    with open("knowledge/L1/python_resources.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print(f"✅ 完成! 成功: {output['success']}/{output['total']}")
    print(f"📁 已保存到: knowledge/L1/python_resources.json")
    print("=" * 50)

if __name__ == "__main__":
    main()
