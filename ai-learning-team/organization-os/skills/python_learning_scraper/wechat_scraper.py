"""
WeChat Scraper - 微信公众号文章抓取
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import re


class WeChatScraper:
    """微信公众号文章爬虫"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        }
    
    def fetch(self, url: str) -> dict:
        """
        抓取文章
        
        Args:
            url: 文章 URL
            
        Returns:
            文章数据
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题
            title = soup.title.string if soup.title else ''
            if not title:
                title = soup.find('h1')
                title = title.get_text() if title else ''
            
            # 提取作者
            author = ''
            author_elem = soup.find('a', id='js_author_name')
            if author_elem:
                author = author_elem.get_text()
            
            # 提取发布日期
            date = ''
            date_elem = soup.find('em', id='js_publish_time')
            if date_elem:
                date = date_elem.get_text()
            
            # 提取正文内容
            content = ''
            article = soup.find('div', id='js_content')
            if article:
                # 移除不需要的标签
                for tag in article.find_all(['script', 'style', 'iframe']):
                    tag.decompose()
                content = article.get_text(separator='\n', strip=True)
            
            # 提取封面图
            cover = ''
            cover_elem = soup.find('img', {'data-croporisrc': True})
            if cover_elem:
                cover = cover_elem.get('data-croporisrc', '')
            
            return {
                'status': 'success',
                'title': title.strip(),
                'author': author.strip(),
                'date': date.strip(),
                'content': content[:5000],  # 限制长度
                'cover': cover,
                'url': url
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'url': url
            }
    
    def fetch_multiple(self, urls: list) -> list:
        """
        批量抓取
        
        Args:
            urls: URL 列表
            
        Returns:
            文章列表
        """
        results = []
        for url in urls:
            result = self.fetch(url)
            results.append(result)
        return results


if __name__ == "__main__":
    scraper = WeChatScraper()
    # 测试（需要真实 URL）
    # result = scraper.fetch("https://mp.weixin.qq.com/s/xxx")
    # print(result)
    print("WeChat Scraper ready!")
