#!/usr/bin/env python3
"""
公众号文章抓取工具
用法：
  python tools/抓取文章.py --url "文章链接"
  python tools/抓取文章.py --url "文章链接" --output my_article
"""
import os
import sys
import argparse
import re
import requests
from datetime import datetime
from urllib.parse import urlparse

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw_articles')
PARSED_DIR = os.path.join(DATA_DIR, 'parsed_articles')

# 创建目录
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def download_article(url: str) -> str:
    """下载文章"""
    print(f"📥 正在下载: {url}")
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        sys.exit(1)

def parse_wechat_article(html: str) -> dict:
    """解析微信公众号文章"""
    import re
    
    # 提取标题
    title_match = re.search(r'<title>(.+?)</title>', html)
    title = title_match.group(1) if title_match else "无标题"
    
    # 提取正文（公众号文章通常在 #js_content 下）
    content_match = re.search(r'<div id="js_content"[^>]*>(.+?)</div>', html, re.DOTALL)
    content = content_match.group(1) if content_match else ""
    
    # 清理HTML标签，保留基本格式
    # 保留p, br, img等
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    
    # 转Markdown
    content = html_to_markdown(content)
    
    return {
        'title': title,
        'content': content,
        'url': '',
        'date': datetime.now().strftime('%Y-%m-%d')
    }

def parse_general_article(html: str, url: str) -> dict:
    """解析一般网页文章"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 标题
    title = ''
    if soup.title:
        title = soup.title.string
    if not title:
        h1 = soup.find('h1')
        if h1:
            title = h1.get_text()
    
    # 正文
    article = soup.find('article') or soup.find('main') or soup.find('div', class_=re.compile('content|article|post'))
    
    if article:
        content = article.get_text(separator='\n', strip=True)
    else:
        # 取body
        body = soup.find('body')
        content = body.get_text(separator='\n', strip=True) if body else ''
    
    return {
        'title': title or '无标题',
        'content': content[:5000],  # 限制长度
        'url': url,
        'date': datetime.now().strftime('%Y-%m-%d')
    }

def html_to_markdown(html: str) -> str:
    """简单HTML转Markdown"""
    import re
    
    md = html
    
    # 标题
    md = re.sub(r'<h1[^>]*>(.+?)</h1>', r'# \1\n', md)
    md = re.sub(r'<h2[^>]*>(.+?)</h2>', r'## \1\n', md)
    md = re.sub(r'<h3[^>]*>(.+?)</h3>', r'### \1\n', md)
    
    # 加粗
    md = re.sub(r'<strong>(.+?)</strong>', r'**\1**', md)
    md = re.sub(r'<b>(.+?)</b>', r'**\1**', md)
    
    # 链接
    md = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.+?)</a>', r'[\2](\1)', md)
    
    # 图片
    md = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![](\1)', md)
    
    # 换行
    md = re.sub(r'<br\s*/?>', '\n', md)
    md = re.sub(r'</p>', '\n\n', md)
    md = re.sub(r'</div>', '\n', md)
    
    # 清理剩余标签
    md = re.sub(r'<[^>]+>', '', md)
    
    # 清理多余空白
    md = re.sub(r'\n{3,}', '\n\n', md)
    
    return md.strip()

def save_article(article: dict, name: str) -> tuple:
    """保存文章"""
    # 生成文件名
    date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
    filename = f"{date}_{name}"
    
    # 保存原文
    html_file = os.path.join(RAW_DIR, f"{filename}.html")
    
    # 保存解析后
    md_file = os.path.join(PARSED_DIR, f"{filename}.md")
    
    # 生成Markdown内容
    md_content = f"""# {article['title']}

> 来源: {article['url']}
> 日期: {article['date']}

---

{article['content']}
"""
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return html_file, md_file

def main():
    parser = argparse.ArgumentParser(description='公众号文章抓取')
    parser.add_argument('--url', '-u', required=True, help='文章链接')
    parser.add_argument('--output', '-o', default='', help='输出文件名（不含扩展名）')
    parser.add_argument('--save-html', action='store_true', help='同时保存HTML原文')
    
    args = parser.parse_args()
    
    url = args.url
    name = args.output or 'article'
    
    print(f"\n{'='*40}")
    print("📥 公众号文章抓取工具")
    print(f"{'='*40}\n")
    
    # 下载
    html = download_article(url)
    
    # 解析
    print("🔍 正在解析...")
    
    # 判断是否为微信公众号
    if 'weixin.qq.com' in url:
        article = parse_wechat_article(html)
    else:
        article = parse_general_article(html, url)
    
    print(f"📌 标题: {article['title']}")
    print(f"📝 字数: {len(article['content'])}")
    
    # 保存
    html_file, md_file = save_article(article, name)
    
    print(f"\n✅ 已保存:")
    print(f"   📄 Markdown: {md_file}")
    
    if args.save_html:
        html_file = os.path.join(RAW_DIR, f"{name}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"   🌐 HTML: {html_file}")
    
    print(f"\n✨ 完成！")

if __name__ == '__main__':
    main()
