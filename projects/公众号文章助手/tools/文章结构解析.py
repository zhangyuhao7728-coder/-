#!/usr/bin/env python3
"""
内容解析系统 V2
从HTML中提取结构化内容
"""
import os
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Dict, List, Optional

class ArticleParser:
    """文章解析器"""
    
    def __init__(self):
        self.supported_formats = ['html', 'md', 'txt']
    
    def parse_html(self, html: str, platform: str = None) -> dict:
        """解析HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        result = {
            'title': self.extract_title(soup),
            'author': self.extract_author(soup),
            'publish_date': self.extract_date(soup),
            'content': self.extract_content(soup),
            'images': self.extract_images(soup),
            'links': self.extract_links(soup),
            'code_blocks': self.extract_code_blocks(soup),
            'structure': self.analyze_structure(soup),
            'metadata': self.extract_metadata(soup),
        }
        
        return result
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """提取标题"""
        # 优先使用meta标签
        title = soup.find('meta', property='og:title')
        if title:
            return title.get('content', '')
        
        title = soup.find('meta', attrs={'name': 'title'})
        if title:
            return title.get('content', '')
        
        # 使用title标签
        if soup.title:
            return soup.title.string.strip() if soup.title.string else ''
        
        # 使用h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return ''
    
    def extract_author(self, soup: BeautifulSoup) -> str:
        """提取作者"""
        # 多种方式尝试
        authors = [
            soup.find('meta', attrs={'name': 'author'}),
            soup.find('meta', property='article:author'),
            soup.find('span', class_=re.compile('author')),
            soup.find('a', class_=re.compile('author')),
        ]
        
        for author in authors:
            if author:
                content = author.get('content', '') or author.get_text(strip=True)
                if content:
                    return content
        
        return ''
    
    def extract_date(self, soup: BeautifulSoup) -> str:
        """提取日期"""
        dates = [
            soup.find('meta', property='article:published_time'),
            soup.find('meta', attrs={'name': 'publishdate'}),
            soup.find('time', class_=re.compile('time|date')),
        ]
        
        for date in dates:
            if date:
                content = date.get('content', '') or date.get('datetime', '') or date.get_text(strip=True)
                if content:
                    return content[:10]  # 取日期部分
        
        return ''
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """提取正文"""
        # 尝试找到主要内容区域
        content_area = None
        
        selectors = [
            'article',
            'main',
            'div[class*="content"]',
            'div[class*="article"]',
            'div[id*="content"]',
            'div[id*="article"]',
            'div[class*="markdown-body"]',
            'div[class*="rich-text"]',
        ]
        
        for selector in selectors:
            content_area = soup.select_one(selector)
            if content_area:
                break
        
        if not content_area:
            content_area = soup.body
        
        # 清理脚本和样式
        for tag in content_area.find_all(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # 获取纯文本
        text = content_area.get_text(separator='\n', strip=True)
        
        # 清理多余空白
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        
        return text
    
    def extract_images(self, soup: BeautifulSoup) -> List[Dict]:
        """提取图片"""
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if src and not src.startswith('data:'):
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                })
        
        return images
    
    def extract_links(self, soup: BeautifulSoup) -> List[Dict]:
        """提取链接"""
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if href and not href.startswith('#'):
                links.append({
                    'href': href,
                    'text': a.get_text(strip=True),
                })
        
        return links[:50]  # 限制数量
    
    def extract_code_blocks(self, soup: BeautifulSoup) -> List[Dict]:
        """提取代码块"""
        code_blocks = []
        
        # pre > code
        for pre in soup.find_all('pre'):
            code = pre.find('code')
            if code:
                lang = code.get('class', [])
                lang = [l for l in lang if l.startswith('language-')]
                code_blocks.append({
                    'language': lang[0].replace('language-', '') if lang else '',
                    'code': code.get_text(),
                })
        
        return code_blocks
    
    def analyze_structure(self, soup: BeautifulSoup) -> Dict:
        """分析文章结构"""
        structure = {
            'headings': {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0},
            'paragraphs': 0,
            'lists': 0,
            'quotes': 0,
            'code_blocks': 0,
            'images': 0,
            'links': 0,
            'tables': 0,
        }
        
        # 统计标题
        for level in ['h1', 'h2', 'h3', 'h4']:
            structure['headings'][level] = len(soup.find_all(level))
        
        # 统计段落
        structure['paragraphs'] = len(soup.find_all('p'))
        
        # 统计列表
        structure['lists'] = len(soup.find_all(['ul', 'ol']))
        
        # 统计引用
        structure['quotes'] = len(soup.find_all(['blockquote', 'q']))
        
        # 统计代码块
        structure['code_blocks'] = len(soup.find_all('pre'))
        
        # 统计图片
        structure['images'] = len(soup.find_all('img'))
        
        # 统计链接
        structure['links'] = len(soup.find_all('a', href=True))
        
        # 统计表格
        structure['tables'] = len(soup.find_all('table'))
        
        return structure
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """提取元数据"""
        metadata = {}
        
        # 描述
        desc = soup.find('meta', attrs={'name': 'description'})
        if desc:
            metadata['description'] = desc.get('content', '')
        
        # 关键词
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords:
            metadata['keywords'] = keywords.get('content', '')
        
        # 标签
        tags = soup.find_all('meta', property='article:tag')
        if tags:
            metadata['tags'] = [t.get('content', '') for t in tags]
        
        return metadata
    
    def to_markdown(self, parsed: dict) -> str:
        """转换为Markdown"""
        md = []
        
        # 标题
        md.append(f"# {parsed.get('title', '无标题')}\n")
        
        # 元信息
        if parsed.get('author'):
            md.append(f"> 作者: {parsed['author']}")
        if parsed.get('publish_date'):
            md.append(f"> 发布日期: {parsed['publish_date']}")
        
        md.append("\n---\n")
        
        # 内容
        md.append(parsed.get('content', ''))
        
        return '\n'.join(md)

def parse_file(filepath: str, platform: str = None) -> dict:
    """解析文件"""
    parser = ArticleParser()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    return parser.parse_html(html, platform)

def parse_html(html: str, platform: str = None) -> dict:
    """解析HTML字符串"""
    parser = ArticleParser()
    return parser.parse_html(html, platform)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        result = parse_file(sys.argv[1])
        
        print(f"\n{'='*50}")
        print(f"📌 标题: {result.get('title', 'N/A')}")
        print(f"👤 作者: {result.get('author', 'N/A')}")
        print(f"📅 日期: {result.get('publish_date', 'N/A')}")
        
        struct = result.get('structure', {})
        print(f"\n📊 结构:")
        print(f"   段落: {struct.get('paragraphs', 0)}")
        print(f"   标题: {struct.get('headings', {})}")
        print(f"   图片: {struct.get('images', 0)}")
        print(f"   链接: {struct.get('links', 0)}")
        print(f"   代码: {struct.get('code_blocks', 0)}")
