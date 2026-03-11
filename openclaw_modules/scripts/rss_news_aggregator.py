#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 新闻聚合器 - 分类整合版
智能分类 + 相似度去重
"""

import os
import json
import hashlib
import re
import subprocess
from datetime import datetime
from collections import defaultdict

# 完整RSS源列表
RSS_SOURCES = [
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss", "cat": "科技"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "cat": "AI"},
    {"name": "Anthropic", "url": "https://www.anthropic.com/news.rss", "cat": "AI"},
    {"name": "Google AI", "url": "https://blog.google/technology/ai/rss/", "cat": "AI"},
    {"name": "Meta AI", "url": "https://ai.meta.com/feed/", "cat": "AI"},
    {"name": "DeepMind", "url": "https://deepmind.com/blog/feed/rss", "cat": "AI"},
    {"name": "OpenClaw", "url": "https://github.com/openclaw/openclaw/releases.atom", "cat": "Agent"},
    {"name": "Cloudflare", "url": "https://blog.cloudflare.com/rss/", "cat": "部署"},
    {"name": "Hugging Face", "url": "https://huggingface.co/blog/feed.xml", "cat": "LLM"},
    {"name": "Vercel", "url": "https://vercel.com/blog/rss.xml", "cat": "部署"},
    {"name": "DEV Community", "url": "https://dev.to/feed", "cat": "开发"},
    {"name": "36kr", "url": "https://36kr.com/newsflashes", "cat": "科技"},
    {"name": "掘金", "url": "https://juejin.cn/feed", "cat": "开发"},
]

CACHE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/rss_cache.json")

# 分类颜色
CAT_EMOJI = {
    "AI": "🤖",
    "LLM": "🧠",
    "Agent": "🔐",
    "部署": "☁️",
    "开发": "💻",
    "科技": "📱",
    "博客": "📝",
    "开源": "🔓",
}

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    return ' '.join(text.split())

def similarity(text1, text2):
    t1 = clean_text(text1)
    t2 = clean_text(text2)
    if not t1 or not t2:
        return 0
    words1 = set(t1.split())
    words2 = set(t2.split())
    if not words1 or not words2:
        return 0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union) * 100

def deduplicate(articles, threshold=80):
    unique = []
    for article in articles:
        is_dup = False
        for existing in unique:
            if similarity(article['title'], existing['title']) >= threshold:
                is_dup = True
                break
        if not is_dup:
            unique.append(article)
    return unique

def categorize(article):
    """智能分类"""
    title = article['title'].lower()
    source = article['source'].lower()
    
    # 关键词匹配
    if any(k in title for k in ['gpt', 'claude', 'gemini', 'llm', 'model', 'ai', '人工智能']):
        return "AI"
    if any(k in title for k in ['agent', 'openclaw', 'claude code', 'operator']):
        return "Agent"
    if any(k in title for k in ['deploy', 'cloud', 'vercel', 'cloudflare', 'aws', '部署']):
        return "部署"
    if any(k in title for k in ['code', 'programming', 'developer', '开发', 'python', 'javascript']):
        return "开发"
    if any(k in title for k in ['hugging', 'transformer', '权重']):
        return "LLM"
    
    return article.get('cat', '科技')

def fetch_url(url):
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "8", "-L", url],
            capture_output=True,
            text=True,
            timeout=12
        )
        return result.stdout if result.returncode == 0 else None
    except:
        return None

def parse_rss(xml, source_name, cat):
    articles = []
    if not xml:
        return articles
    
    items = xml.split('<item>')
    for item in items[1:5]:
        title = ""
        link = ""
        
        ts = item.find('<title>')
        te = item.find('</title>')
        if ts != -1 and te != -1:
            title = item[ts+7:te].strip()
        
        ls = item.find('<link>')
        le = item.find('</link>')
        if ls != -1 and le != -1:
            link = item[ls+6:le].strip()
        
        if title and len(title) > 3:
            articles.append({
                'title': title[:100],
                'link': link,
                'source': source_name,
                'cat': cat,
            })
    
    return articles

def translate_and_summarize(articles):
    if not articles:
        return None
    
    # 限制翻译数量，减少额度消耗
    articles = articles[:1]
    news_list = "\n".join([f"{i+1}. {a['title']}" for i, a in enumerate(articles)])
    
    prompt = f"""请将以下科技新闻翻译成中文并简要总结，每条1句话：

{news_list}

格式：
1. [翻译+总结]"""

    print("🤖 本地模型翻译中...")
    
    try:
        result = subprocess.run(
            ["ollama", "run", "qwen2.5:7b", prompt],  # 使用轻量版模型
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    return None

def format_output(articles, summaries):
    """分类整合输出"""
    # 按分类分组
    categories = defaultdict(list)
    for a in articles:
        cat = categorize(a)
        categories[cat].append(a)
    
    output = f"📰 AI科技新闻 - {datetime.now().strftime('%m-%d %H:%M')}\n"
    output += f"📊 来源: {len(RSS_SOURCES)}个 | 分类: {len(categories)}类\n\n"
    
    # 输出分类
    for cat in ["AI", "Agent", "LLM", "部署", "开发", "科技"]:
        if cat in categories and categories[cat]:
            emoji = CAT_EMOJI.get(cat, "📌")
            output += f"{emoji} {cat}\n"
            for a in categories[cat][:2]:
                title = a['title'][:50] + "..." if len(a['title']) > 50 else a['title']
                output += f"   • {title}\n"
            output += "\n"
    
    return output

def main(limit=3):
    print(f"📰 正在获取新闻...")
    
    all_articles = []
    success = 0
    
    for source in RSS_SOURCES:
        xml = fetch_url(source['url'])
        if xml:
            articles = parse_rss(xml, source['name'], source['cat'])
            if articles:
                all_articles.extend(articles)
                success += 1
    
    print(f"✅ 成功获取: {success}/{len(RSS_SOURCES)} 个源")
    
    # 智能去重
    unique = deduplicate(all_articles, threshold=80)
    
    # 缓存
    cache = load_cache()
    new_articles = []
    for a in unique:
        h = hashlib.md5(a['title'].encode()).hexdigest()[:16]
        if h not in cache:
            cache[h] = True
            new_articles.append(a)
    
    save_cache(cache)
    new_articles = new_articles[:limit]
    
    if new_articles:
        print(f"📮 去重后: {len(new_articles)} 条")
        
        # 翻译
        summary = translate_and_summarize(new_articles)
        
        # 分类整合
        output = format_output(new_articles, summary)
        print("\n" + output)
        
        return output
    else:
        print("✅ 暂无新新闻")
    
    return None

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    main(limit)
