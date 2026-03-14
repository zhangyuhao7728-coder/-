#!/usr/bin/env python3
"""
简单的网页抓取示例
"""
import urllib.request
import re

def fetch_page(url):
    """抓取网页"""
    try:
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        return f"错误: {e}"

def extract_text(html):
    """提取纯文本"""
    # 移除脚本和样式
    text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '\n', text)
    # 清理空白
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

# 测试：抓取百度首页
url = "https://www.baidu.com"
print(f"正在抓取: {url}")
print("=" * 40)

html = fetch_page(url)
if not html.startswith("错误"):
    text = extract_text(html)
    print(text[:500])
    print(f"\n✅ 抓取成功！总长度: {len(html)} 字符")
else:
    print(html)
