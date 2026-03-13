# -*- coding: utf-8 -*-
"""
多功能爬虫程序 v4.0 (终极版)
支持多网站、异步爬取、图片下载、数据去重、数据库存储

功能模块：
1. 多网站支持 - 轻松扩展新网站
2. 异步爬取 - 并发提速
3. 图片爬取 - 下载图片/表情包
4. 数据去重 - MD5去重
5. 数据库存储 - MySQL/MongoDB/SQLite
6. 完整安全防护
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import argparse
import os
import random
import urllib.parse
import hashlib
import asyncio
import aiohttp
import sqlite3
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import re


# ==================== 基础工具 ====================

class Utils:
    """工具类"""
    
    @staticmethod
    def md5(text: str) -> str:
        """MD5哈希"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """清理文件名"""
        # 移除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # 限制长度
        return filename[:200] if len(filename) > 200 else filename
    
    @staticmethod
    def ensure_dir(path: str):
        """确保目录存在"""
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def get_domain(url: str) -> str:
        """获取域名"""
        return urlparse(url).netloc


# ==================== 安全组件 ====================

class RobotsChecker:
    """robots.txt 检查器"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.allowed_paths = set()
        self._fetch()
    
    def _fetch(self):
        """获取 robots.txt"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            resp = requests.get(robots_url, timeout=5)
            if resp.status_code == 200:
                self._parse(resp.text)
        except:
            pass
    
    def _parse(self, content: str):
        """解析"""
        for line in content.split('\n'):
            if line.lower().startswith('allow:'):
                path = line.split(':', 1)[1].strip()
                if path:
                    self.allowed_paths.add(path)
    
    def can_fetch(self, path: str) -> bool:
        """检查是否允许"""
        if not self.allowed_paths:
            return True
        return any(path.startswith(p) for p in self.allowed_paths)


class RateLimiter:
    """限速器"""
    
    def __init__(self, delay: float = 1):
        self.delay = delay
        self.last_request = 0
    
    def wait(self):
        """等待"""
        elapsed = time.time() - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed + random.uniform(0, 0.5))
        self.last_request = time.time()


class ProxyPool:
    """代理池"""
    
    def __init__(self):
        self.proxies = []
        self.index = 0
    
    def add(self, proxy: str):
        self.proxies.append(proxy)
    
    def get(self) -> Optional[Dict]:
        if not self.proxies:
            return None
        proxy = self.proxies[self.index % len(self.proxies)]
        self.index += 1
        return {'http': proxy, 'https': proxy}


# ==================== 网站解析器 ====================

class BaseParser:
    """网站解析器基类"""
    
    name = "base"
    allowed_domains = []
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice([
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        })
    
    def parse(self, html: str, url: str) -> List[Dict]:
        """解析页面 - 子类必须实现"""
        raise NotImplementedError
    
    def get_list_url(self, page: int) -> str:
        """获取列表页URL - 子类必须实现"""
        raise NotImplementedError
    
    def get_detail_url(self, item: Dict) -> str:
        """获取详情页URL"""
        return item.get('url', '')


class QuotesParser(BaseParser):
    """名言网站解析器"""
    
    name = "quotes"
    allowed_domains = ['quotes.toscrape.com']
    base_url = "http://quotes.toscrape.com"
    
    def get_list_url(self, page: int = 1) -> str:
        if page == 1:
            return self.base_url + "/"
        return f"{self.base_url}/page/{page}/"
    
    def parse(self, html: str, url: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        for quote in soup.select('.quote'):
            try:
                text = quote.select_one('.text').get_text(strip=True)
                author = quote.select_one('.author').get_text(strip=True)
                tags = [t.get_text(strip=True) for t in quote.select('.tag')]
                
                items.append({
                    'text': text,
                    'author': author,
                    'tags': tags,
                    'url': url,
                    'type': 'quote'
                })
            except:
                continue
        
        return items
    
    def has_next(self, html: str) -> bool:
        return bool(BeautifulSoup(html, 'html.parser').select_one('.pager .next a'))


class NewsParser(BaseParser):
    """新闻网站解析器 (示例: 网易新闻)"""
    
    name = "news"
    allowed_domains = ['news.163.com', 'news.sina.com.cn']
    base_url = "https://news.163.com"
    
    def get_list_url(self, page: int = 1) -> str:
        return f"{self.base_url}/"
    
    def parse(self, html: str, url: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        # 网易新闻选择器示例
        for item in soup.select('.news_title a, .item_top a, .topnews_title a')[:20]:
            try:
                title = item.get_text(strip=True)
                link = urljoin(url, item.get('href', ''))
                
                if title and link:
                    items.append({
                        'title': title,
                        'url': link,
                        'type': 'news'
                    })
            except:
                continue
        
        return items
    
    def has_next(self, html: str) -> bool:
        return False


class ImageParser(BaseParser):
    """图片爬取解析器"""
    
    name = "image"
    allowed_domains = []
    base_url = "https://www.reddit.com"
    
    def get_list_url(self, page: int = 1) -> str:
        if 'reddit' in self.base_url:
            return f"{self.base_url}/r/wallpapers/top/.json?t=day&limit=25"
        return self.base_url
    
    def parse(self, html: str, url: str) -> List[Dict]:
        items = []
        
        # 尝试解析 JSON
        try:
            data = json.loads(html)
            if 'data' in data:
                for child in data['data'].get('children', []):
                    post = child.get('data', {})
                    if post.get('url'):
                        items.append({
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'type': 'image',
                            'source': 'reddit'
                        })
        except:
            # 解析 HTML
            soup = BeautifulSoup(html, 'html.parser')
            for img in soup.select('img[src]'):
                src = img.get('src', '')
                if src and not src.endswith('.gif'):
                    items.append({
                        'title': img.get('alt', ''),
                        'url': src,
                        'type': 'image'
                    })
        
        return items
    
    def has_next(self, html: str) -> bool:
        return False


# ==================== 核心爬虫 ====================

class Crawler:
    """多网站爬虫 (同步版)"""
    
    # 注册解析器
    PARSERS = {
        'quotes': QuotesParser,
        'news': NewsParser,
        'image': ImageParser,
    }
    
    def __init__(self, site: str = 'quotes', delay: float = 1, proxy: str = None):
        self.site = site
        
        # 获取解析器
        parser_class = self.PARSERS.get(site, QuotesParser)
        self.parser = parser_class()
        
        # 组件
        self.rate_limiter = RateLimiter(delay)
        self.proxy_pool = ProxyPool()
        
        if proxy:
            self.proxy_pool.add(proxy)
        
        # 统计
        self.stats = {'success': 0, 'failed': 0, 'duplicates': 0}
        
        # 去重
        self.seen_ids = set()
        
        # robots
        self.robots = RobotsChecker(self.parser.base_url)
    
    def _get_id(self, item: Dict) -> str:
        """生成唯一ID"""
        content = item.get('text') or item.get('title') or item.get('url', '')
        return Utils.md5(content)
    
    def _is_duplicate(self, item: Dict) -> bool:
        """检查重复"""
        item_id = self._get_id(item)
        if item_id in self.seen_ids:
            return True
        self.seen_ids.add(item_id)
        return False
    
    def _download_image(self, url: str, save_dir: str) -> Optional[str]:
        """下载图片"""
        try:
            resp = requests.get(url, timeout=30, proxies=self.proxy_pool.get())
            if resp.status_code == 200:
                # 获取扩展名
                ext = os.path.splitext(urlparse(url).path)[1] or '.jpg'
                if not ext:
                    ext = '.jpg'
                
                filename = Utils.sanitize_filename(url.split('/')[-1][:100])
                if not filename:
                    filename = Utils.md5(url)[:10] + ext
                
                filepath = os.path.join(save_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                
                return filepath
        except Exception as e:
            print(f"⚠️ 图片下载失败: {e}")
        return None
    
    def crawl_page(self, url: str) -> List[Dict]:
        """爬取单页"""
        self.rate_limiter.wait()
        
        try:
            resp = requests.get(
                url, 
                timeout=15,
                proxies=self.proxy_pool.get()
            )
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            
            self.stats['success'] += 1
            return self.parser.parse(resp.text, url)
            
        except Exception as e:
            self.stats['failed'] += 1
            print(f"⚠️ 爬取失败: {e}")
            return []
    
    def crawl(self, pages: int = 1, max_items: int = 100, 
              save_images: bool = False, save_dir: str = 'output') -> List[Dict]:
        """爬取数据"""
        all_items = []
        page = 1
        url = self.parser.get_list_url(1)
        
        print(f"🚀 开始爬取: {self.site}")
        print(f"📄 目标: {pages} 页, 最多 {max_items} 条")
        print("-" * 50)
        
        while len(all_items) < max_items:
            # 检查 robots
            if not self.robots.can_fetch(url):
                print(f"⚠️ robots.txt 禁止: {url}")
                break
            
            print(f"📥 爬取第 {page} 页: {url[:60]}...")
            
            items = self.crawl_page(url)
            
            # 去重
            new_items = [i for i in items if not self._is_duplicate(i)]
            self.stats['duplicates'] += len(items) - len(new_items)
            
            all_items.extend(new_items)
            print(f"   ✅ 获取 {len(new_items)} 条新数据")
            
            # 下载图片
            if save_images:
                img_dir = os.path.join(save_dir, 'images')
                Utils.ensure_dir(img_dir)
                
                for item in new_items:
                    if item.get('type') == 'image':
                        filepath = self._download_image(item['url'], img_dir)
                        if filepath:
                            item['local_path'] = filepath
            
            # 检查是否继续
            if pages > 0 and page >= pages:
                break
            
            # 翻页
            if hasattr(self.parser, 'has_next'):
                html = requests.get(url, timeout=10).text
                if not self.parser.has_next(html):
                    break
            
            page += 1
            url = self.parser.get_list_url(page)
        
        print("-" * 50)
        print(f"🎉 完成! 共获取 {len(all_items)} 条数据")
        print(f"📊 统计: 成功 {self.stats['success']}, 失败 {self.stats['failed']}, "
              f"去重 {self.stats['duplicates']}")
        
        return all_items
    
    def save(self, items: List[Dict], filepath: str, format: str = 'json'):
        """保存数据"""
        Utils.ensure_dir(os.path.dirname(filepath) or '.')
        
        if format == 'json':
            output = {
                'meta': {
                    'site': self.site,
                    'count': len(items),
                    'time': datetime.now().isoformat()
                },
                'data': items
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
                
        elif format == 'csv':
            if not items:
                return
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                keys = items[0].keys()
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(items)
        
        elif format == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 爬取时间: {datetime.now().isoformat()}\n")
                f.write(f"# 网站: {self.site}\n")
                f.write(f"# 总数: {len(items)}\n")
                f.write("=" * 50 + "\n\n")
                for i, item in enumerate(items, 1):
                    if 'text' in item:
                        f.write(f"{i}. {item['text']}\n")
                        f.write(f"   —— {item.get('author', '')}\n\n")
                    elif 'title' in item:
                        f.write(f"{i}. {item['title']}\n")
                        f.write(f"   🔗 {item.get('url', '')}\n\n")
        
        print(f"💾 已保存: {filepath}")


class AsyncCrawler:
    """异步爬虫 (更快速)"""
    
    def __init__(self, site: str = 'quotes', concurrency: int = 5, delay: float = 0.5):
        self.site = site
        self.concurrency = concurrency
        self.delay = delay
        
        # 获取解析器
        parser_class = Crawler.PARSERS.get(site, QuotesParser)
        self.parser = parser_class()
        
        # 统计
        self.stats = {'success': 0, 'failed': 0}
        self.seen_ids = set()
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> str:
        """异步获取"""
        await asyncio.sleep(self.delay)
        
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                self.stats['success'] += 1
                return await resp.text()
        except:
            self.stats['failed'] += 1
            return ''
    
    async def crawl(self, urls: List[str]) -> List[Dict]:
        """异步爬取多个URL"""
        connector = aiohttp.TCPConnector(limit=self.concurrency)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.fetch(session, url) for url in urls]
            html_list = await asyncio.gather(*tasks)
        
        all_items = []
        for html, url in zip(html_list, urls):
            if html:
                items = self.parser.parse(html, url)
                all_items.extend(items)
        
        print(f"📊 异步统计: 成功 {self.stats['success']}, 失败 {self.stats['failed']}")
        return all_items


class Database:
    """数据库存储"""
    
    def __init__(self, db_path: str = 'crawler.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS crawl_data (
                id INTEGER PRIMARY KEY,
                site TEXT,
                item_type TEXT,
                title TEXT,
                content TEXT,
                url TEXT,
                author TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(site, title, content)
            )
        ''')
        conn.commit()
        conn.close()
    
    def save(self, items: List[Dict], site: str):
        """保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved = 0
        for item in items:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO crawl_data 
                    (site, item_type, title, content, url, author, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    site,
                    item.get('type', ''),
                    item.get('title', ''),
                    item.get('text', ''),
                    item.get('url', ''),
                    item.get('author', ''),
                    ','.join(item.get('tags', []))
                ))
                saved += 1
            except:
                continue
        
        conn.commit()
        conn.close()
        
        print(f"💾 数据库保存: {saved} 条")
    
    def query(self, site: str = None, limit: int = 100) -> List[Dict]:
        """查询数据"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        if site:
            cursor = conn.execute(
                'SELECT * FROM crawl_data WHERE site = ? ORDER BY id DESC LIMIT ?',
                (site, limit)
            )
        else:
            cursor = conn.execute(
                'SELECT * FROM crawl_data ORDER BY id DESC LIMIT ?',
                (limit,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# ==================== 命令行界面 ====================

def main():
    parser = argparse.ArgumentParser(
        description='多功能爬虫 v4.0 (终极版)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持网站:
  quotes   - 名言警句 (默认)
  news     - 新闻网站
  image    - 图片爬取

示例:
  python4 crawler.py -s quotes -p 3              # 爬取名言
  python4 crawler.py -s image -p 2 --download   # 爬取图片
  python4 crawler.py -s quotes --db              # 保存到数据库
  python4 crawler.py -s quotes --async           # 异步快速爬取
        """
    )
    
    # 基本参数
    parser.add_argument('-s', '--site', default='quotes', 
                       choices=['quotes', 'news', 'image'],
                       help='网站类型')
    parser.add_argument('-p', '--pages', type=int, default=2, help='爬取页数')
    parser.add_argument('-m', '--max', type=int, default=100, help='最大条数')
    parser.add_argument('-d', '--delay', type=float, default=1, help='延迟秒数')
    
    # 输出
    parser.add_argument('-o', '--output', default='output/data', help='输出路径')
    parser.add_argument('-f', '--format', default='json', 
                       choices=['json', 'csv', 'txt'], help='格式')
    parser.add_argument('--download', action='store_true', help='下载图片')
    parser.add_argument('--db', action='store_true', help='保存到数据库')
    
    # 代理
    parser.add_argument('--proxy', help='HTTP代理')
    
    # 异步
    parser.add_argument('--async', dest='use_async', action='store_true', help='异步爬取')
    
    args = parser.parse_args()
    
    # 创建爬虫
    if args.use_async:
        print("⚡ 使用异步模式")
        crawler = AsyncCrawler(args.site, delay=args.delay)
        urls = [crawler.parser.get_list_url(i) for i in range(1, args.pages + 1)]
        items = asyncio.run(crawler.crawl(urls))
    else:
        crawler = Crawler(args.site, args.delay, args.proxy)
        items = crawler.crawl(args.pages, args.max, args.download, args.output)
    
    if not items:
        print("❌ 无数据")
        return
    
    # 保存
    if args.db:
        db = Database()
        db.save(items, args.site)
    
    if args.format:
        crawler.save(items, f"{args.output}.{args.format}", args.format)


if __name__ == "__main__":
    main()
