#!/usr/bin/env python3
"""
内容采集系统 V2
支持多平台采集
"""
import os
import sys
import re
import time
import requests
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

class ContentCrawler:
    """多平台内容采集器"""
    
    # 请求头
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    # 支持的平台
    PLATFORMS = {
        'weixin': {'name': '微信公众号', 'domain': 'weixin.qq.com'},
        'zhihu': {'name': '知乎', 'domain': 'zhihu.com'},
        'juejin': {'name': '掘金', 'domain': 'juejin.cn'},
        'csdn': {'name': 'CSDN', 'domain': 'csdn.net'},
        'jianshu': {'name': '简书', 'domain': 'jianshu.com'},
        'xiaohongshu': {'name': '小红书', 'domain': 'xiaohongshu.com'},
        'bilibili': {'name': 'B站', 'domain': 'bilibili.com'},
        'github': {'name': 'GitHub', 'domain': 'github.com'},
    }
    
    def __init__(self, output_dir: str = 'data/raw_articles'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def detect_platform(self, url: str) -> str:
        """检测平台"""
        domain = urlparse(url).netloc.lower()
        
        for platform, info in self.PLATFORMS.items():
            if info['domain'] in domain:
                return platform
        
        return 'unknown'
    
    def download(self, url: str) -> dict:
        """下载网页"""
        print(f"📥 下载中: {url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return {
                'success': True,
                'url': url,
                'platform': self.detect_platform(url),
                'content': response.text,
                'status_code': response.status_code,
                'timestamp': datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                'success': False,
                'url': url,
                'error': str(e),
            }
    
    def save_html(self, url: str, content: str) -> str:
        """保存HTML"""
        platform = self.detect_platform(url)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{platform}_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def batch_download(self, urls: list, delay: float = 1.0) -> list:
        """批量下载"""
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] {url}")
            
            result = self.download(url)
            
            if result['success']:
                filepath = self.save_html(url, result['content'])
                result['filepath'] = filepath
                print(f"✅ 已保存: {filepath}")
            else:
                print(f"❌ 失败: {result.get('error')}")
            
            results.append(result)
            
            if delay > 0 and i < len(urls):
                time.sleep(delay)
        
        return results

class PlatformCrawler:
    """各平台专用采集器"""
    
    @staticmethod
    def weixin(html: str, url: str) -> dict:
        """微信公众号解析"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title = soup.title.string if soup.title else ''
        if not title:
            title_tag = soup.find('meta', attrs={'name': 'description'})
            title = title_tag.get('content', '') if title_tag else ''
        
        # 提取正文
        content_div = soup.find('div', id='js_content')
        content = content_div.get_text(separator='\n', strip=True) if content_div else ''
        
        # 提取作者
        author = ''
        author_tag = soup.find('meta', attrs={'name': 'author'})
        if author_tag:
            author = author_tag.get('content', '')
        
        return {
            'platform': 'weixin',
            'title': title.strip(),
            'author': author,
            'content': content,
            'url': url,
            'raw_html': html[:10000],  # 保存前10000字符
        }
    
    @staticmethod
    def zhihu(html: str, url: str) -> dict:
        """知乎解析"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # 标题
        title = soup.find('h1')
        title = title.get_text(strip=True) if title else ''
        
        # 正文
        article = soup.find('article') or soup.find('div', class_='RichText')
        content = article.get_text(separator='\n', strip=True) if article else ''
        
        return {
            'platform': 'zhihu',
            'title': title,
            'content': content,
            'url': url,
        }
    
    @staticmethod
    def juejin(html: str, url: str) -> dict:
        """掘金解析"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('h1')
        title = title.get_text(strip=True) if title else ''
        
        article = soup.find('article') or soup.find('div', class_='markdown-body')
        content = article.get_text(separator='\n', strip=True) if article else ''
        
        return {
            'platform': 'juejin',
            'title': title,
            'content': content,
            'url': url,
        }
    
    @staticmethod
    def csdn(html: str, url: str) -> dict:
        """CSDN解析"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.find('h1', class_='title-article')
        title = title.get_text(strip=True) if title else ''
        
        article = soup.find('article', class_='markdown-body')
        content = article.get_text(separator='\n', strip=True) if article else ''
        
        return {
            'platform': 'csdn',
            'title': title,
            'content': content,
            'url': url,
        }

def crawl(url: str, output_dir: str = 'data/raw_articles') -> dict:
    """采集内容"""
    crawler = ContentCrawler(output_dir)
    
    # 下载
    result = crawler.download(url)
    if not result['success']:
        return result
    
    # 保存
    filepath = crawler.save_html(url, result['content'])
    result['filepath'] = filepath
    
    # 解析
    platform = crawler.detect_platform(url)
    
    parse_funcs = {
        'weixin': PlatformCrawler.weixin,
        'zhihu': PlatformCrawler.zhihu,
        'juejin': PlatformCrawler.juejin,
        'csdn': PlatformCrawler.csdn,
    }
    
    parse_func = parse_funcs.get(platform)
    if parse_func:
        parsed = parse_func(result['content'], url)
        result['parsed'] = parsed
    
    return result

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='内容采集系统')
    parser.add_argument('--url', '-u', help='采集URL')
    parser.add_argument('--batch', '-b', nargs='+', help='批量采集')
    parser.add_argument('--output', '-o', default='data/raw_articles', help='输出目录')
    
    args = parser.parse_args()
    
    crawler = ContentCrawler(args.output)
    
    if args.url:
        result = crawl(args.url, args.output)
        print(f"\n{'='*50}")
        print(f"平台: {result.get('platform')}")
        print(f"保存: {result.get('filepath')}")
        if 'parsed' in result:
            print(f"标题: {result['parsed'].get('title', 'N/A')}")
    
    elif args.batch:
        results = crawler.batch_download(args.batch)
        print(f"\n完成: {len([r for r in results if r['success']])}/{len(results)}")
