# -*- coding: utf-8 -*-
"""
多功能爬虫程序 v5.0 (高效稳定版)
优化重点：速度更快、资源消耗更低、运行更稳定

性能优化：
1. 多线程并行爬取
2. 连接池复用
3. 智能重试+退避
4. 内存优化
5. 成本控制（减少无效请求）
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
import sqlite3
from datetime import datetime
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
import re
from typing import List, Dict, Optional, Set


# ==================== 工具类 ====================

class Utils:
    """工具类"""
    
    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return filename[:200] if len(filename) > 200 else filename
    
    @staticmethod
    def ensure_dir(path: str):
        os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def get_domain(url: str) -> str:
        return urlparse(url).netloc


# ==================== 线程安全组件 ====================

class ThreadSafeCounter:
    """线程安全计数器"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._counts = {'success': 0, 'failed': 0, 'duplicate': 0}
    
    def increment(self, key: str, value: int = 1):
        with self._lock:
            self._counts[key] = self._counts.get(key, 0) + value
    
    def get(self, key: str) -> int:
        with self._lock:
            return self._counts.get(key, 0)
    
    def get_all(self) -> Dict:
        with self._lock:
            return self._counts.copy()


class ThreadSafeSet:
    """线程安全集合（用于去重）"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._set = set()
    
    def add(self, item: str) -> bool:
        with self._lock:
            if item in self._set:
                return False
            self._set.add(item)
            return True
    
    def __len__(self):
        with self._lock:
            return len(self._set)


# ==================== 网络组件 ====================

class SessionPool:
    """会话池 - 复用连接"""
    
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self.sessions = []
        self._lock = threading.Lock()
        
        # 预创建会话
        for _ in range(min(3, max_size)):
            self.sessions.append(self._create_session())
    
    def _create_session(self) -> requests.Session:
        """创建新会话"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice([
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        })
        # 连接池配置
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=5,
            pool_maxsize=10,
            max_retries=0
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def get_session(self) -> requests.Session:
        """获取会话"""
        with self._lock:
            if self.sessions:
                return self.sessions.pop(0)
        return self._create_session()
    
    def return_session(self, session: requests.Session):
        """归还会话"""
        with self._lock:
            if len(self.sessions) < self.max_size:
                self.sessions.append(session)


class RateLimiter:
    """令牌桶限速器"""
    
    def __init__(self, rate: float = 1):
        self.rate = rate  # 每秒请求数
        self.tokens = rate
        self.max_tokens = rate
        self.last_update = time.time()
        self._lock = threading.Lock()
    
    def acquire(self, tokens: int = 1) -> bool:
        """获取令牌"""
        with self._lock:
            now = time.time()
            # 补充令牌
            self.tokens = min(self.max_tokens, 
                            self.tokens + (now - self.last_update) * self.rate)
            self.last_update = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_and_acquire(self, tokens: int = 1):
        """等待并获取令牌"""
        while not self.acquire(tokens):
            time.sleep(0.1)


# ==================== 网站解析器 ====================

class BaseParser:
    """解析器基类"""
    
    name = "base"
    
    def __init__(self):
        pass
    
    def parse(self, html: str, url: str) -> List[Dict]:
        raise NotImplementedError
    
    def get_list_url(self, page: int) -> str:
        raise NotImplementedError


class QuotesParser(BaseParser):
    """名言解析器"""
    
    name = "quotes"
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
    """新闻解析器"""
    
    name = "news"
    base_url = "https://news.163.com"
    
    def get_list_url(self, page: int = 1) -> str:
        return self.base_url + "/"
    
    def parse(self, html: str, url: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        items = []
        
        for item in soup.select('.news_title a, .item_top a')[:15]:
            try:
                title = item.get_text(strip=True)
                link = urljoin(url, item.get('href', ''))
                
                if title and link and len(title) > 5:
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


# ==================== 高效爬虫 ====================

class FastCrawler:
    """高效爬虫 - 多线程 + 连接池"""
    
    PARSERS = {
        'quotes': QuotesParser,
        'news': NewsParser,
    }
    
    def __init__(self, site: str = 'quotes', 
                 workers: int = 3,      # 并发数
                 delay: float = 0.5,    # 请求间隔
                 retry: int = 3):        # 重试次数
        
        self.site = site
        self.workers = min(workers, 5)   # 最多5个线程
        self.retry = retry
        
        # 获取解析器
        parser_class = self.PARSERS.get(site, QuotesParser)
        self.parser = parser_class()
        
        # 组件
        self.session_pool = SessionPool(max_size=self.workers)
        self.rate_limiter = RateLimiter(rate=1/delay if delay > 0 else 100)
        
        # 统计
        self.stats = ThreadSafeCounter()
        self.seen_ids = ThreadSafeSet()
        
        # 成本控制
        self.max_requests = 100  # 最大请求数
        self.request_count = 0
        self._lock = threading.Lock()
    
    def _get_id(self, item: Dict) -> str:
        """生成唯一ID"""
        content = item.get('text') or item.get('title') or item.get('url', '')
        return Utils.md5(content)
    
    def _is_duplicate(self, item: Dict) -> bool:
        """检查重复"""
        item_id = self._get_id(item)
        return not self.seen_ids.add(item_id)
    
    def fetch(self, url: str) -> Optional[str]:
        """获取页面 - 带重试"""
        # 成本控制
        with self._lock:
            if self.request_count >= self.max_requests:
                return None
            self.request_count += 1
        
        # 限速
        self.rate_limiter.wait_and_acquire()
        
        session = self.session_pool.get_session()
        
        for attempt in range(self.retry):
            try:
                resp = session.get(url, timeout=10)
                
                if resp.status_code == 200:
                    resp.encoding = 'utf-8'
                    self.stats.increment('success')
                    return resp.text
                
                elif resp.status_code == 429:
                    # 被限流，等待更久
                    wait_time = (attempt + 1) * 2
                    print(f"⚠️ 被限流，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                elif resp.status_code >= 500:
                    # 服务器错误，重试
                    time.sleep(1)
                    
            except requests.exceptions.Timeout:
                time.sleep(1)
            except requests.exceptions.ConnectionError:
                time.sleep(1)
            except Exception as e:
                break
        
        self.stats.increment('failed')
        self.session_pool.return_session(session)
        return None
    
    def crawl_page(self, url: str) -> List[Dict]:
        """爬取单页"""
        html = self.fetch(url)
        
        if not html:
            return []
        
        items = self.parser.parse(html, url)
        
        # 去重
        unique_items = []
        for item in items:
            if not self._is_duplicate(item):
                unique_items.append(item)
            else:
                self.stats.increment('duplicate')
        
        return unique_items
    
    def crawl(self, pages: int = 3, max_items: int = 100) -> List[Dict]:
        """多线程爬取"""
        all_items = []
        pages_to_crawl = list(range(1, pages + 1))
        
        print(f"🚀 开始高效爬取: {self.site}")
        print(f"⚙️ 并发数: {self.workers}, 目标: {pages} 页, 最多 {max_items} 条")
        print("-" * 50)
        
        start_time = time.time()
        
        # 多线程爬取
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            # 提交任务
            future_to_page = {}
            for page in pages_to_crawl:
                url = self.parser.get_list_url(page)
                future = executor.submit(self.crawl_page, url)
                future_to_page[future] = page
            
            # 收集结果
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    items = future.result()
                    all_items.extend(items)
                    
                    if items:
                        print(f"✅ 第 {page} 页: 获取 {len(items)} 条")
                    else:
                        print(f"⚠️ 第 {page} 页: 无数据")
                    
                    # 检查数量
                    if len(all_items) >= max_items:
                        # 取消剩余任务
                        for f in future_to_page:
                            f.cancel()
                        break
                        
                except Exception as e:
                    print(f"❌ 第 {page} 页失败: {e}")
        
        elapsed = time.time() - start_time
        stats = self.stats.get_all()
        
        print("-" * 50)
        print(f"🎉 完成! 获取 {len(all_items)} 条数据")
        print(f"⏱️ 耗时: {elapsed:.2f}秒")
        print(f"📊 统计: 成功 {stats.get('success', 0)}, "
              f"失败 {stats.get('failed', 0)}, "
              f"去重 {stats.get('duplicate', 0)}")
        
        return all_items[:max_items]
    
    def save(self, items: List[Dict], filepath: str, format: str = 'json'):
        """保存数据"""
        Utils.ensure_dir(os.path.dirname(filepath) or '.')
        
        if format == 'json':
            output = {
                'meta': {
                    'site': self.site,
                    'count': len(items),
                    'time': datetime.now().isoformat(),
                    'workers': self.workers
                },
                'data': items
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
                
        elif format == 'csv':
            if not items:
                return
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                keys = list(items[0].keys())
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(items)
        
        elif format == 'txt':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 爬取: {self.site}\n")
                f.write(f"# 时间: {datetime.now().isoformat()}\n")
                f.write(f"# 总数: {len(items)}\n")
                f.write("=" * 50 + "\n\n")
                for i, item in enumerate(items, 1):
                    if 'text' in item:
                        f.write(f"{i}. {item['text']}\n")
                        f.write(f"   —— {item.get('author', '')}\n\n")
        
        print(f"💾 已保存: {filepath}")


class Database:
    """数据库存储"""
    
    def __init__(self, db_path: str = 'crawler.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
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
                UNIQUE(site, content)
            )
        ''')
        conn.commit()
        conn.close()
    
    def save(self, items: List[Dict], site: str):
        if not items:
            return
            
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


# ==================== 命令行 ====================

def main():
    parser = argparse.ArgumentParser(
        description='高效爬虫 v5.0 (多线程版)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 crawler.py -s quotes -p 5           # 爬5页，3线程
  python3 crawler.py -s quotes -p 10 -w 5     # 5线程更快
  python3 crawler.py -s quotes --db            # 保存数据库
  python3 crawler.py -s quotes -f csv         # CSV格式
        """
    )
    
    parser.add_argument('-s', '--site', default='quotes', 
                       choices=['quotes', 'news'],
                       help='网站')
    parser.add_argument('-p', '--pages', type=int, default=3, help='页数')
    parser.add_argument('-m', '--max', type=int, default=100, help='最大条数')
    parser.add_argument('-w', '--workers', type=int, default=3, help='并发数(1-5)')
    parser.add_argument('-d', '--delay', type=float, default=0.5, help='请求间隔')
    parser.add_argument('-r', '--retry', type=int, default=3, help='重试次数')
    
    parser.add_argument('-o', '--output', default='output/data', help='输出路径')
    parser.add_argument('-f', '--format', default='json', 
                       choices=['json', 'csv', 'txt'], help='格式')
    parser.add_argument('--db', action='store_true', help='保存数据库')
    
    args = parser.parse_args()
    
    # 创建爬虫
    crawler = FastCrawler(
        site=args.site,
        workers=args.workers,
        delay=args.delay,
        retry=args.retry
    )
    
    # 爬取
    items = crawler.crawl(args.pages, args.max)
    
    if not items:
        print("❌ 无数据")
        return
    
    # 保存
    if args.db:
        db = Database()
        db.save(items, args.site)
    
    crawler.save(items, f"{args.output}.{args.format}", args.format)


if __name__ == "__main__":
    main()
