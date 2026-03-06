"""
Python Learning Scraper - Skill 主入口
可以被 Agent 调用
"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from youtube_scraper import YouTubeScraper
from wechat_scraper import WeChatScraper
from note_generator import NoteGenerator


class PythonLearningScraper:
    """Python 学习爬虫 Skill"""
    
    def __init__(self):
        self.youtube = YouTubeScraper()
        self.wechat = WeChatScraper()
        self.notes = NoteGenerator()
    
    def search_youtube(self, query: str = "Python", max_results: int = 20) -> dict:
        """搜索 YouTube 视频"""
        videos = self.youtube.search(query, max_results)
        note_path = self.notes.generate_youtube_notes(videos, query)
        
        return {
            'status': 'success',
            'videos': videos,
            'count': len(videos),
            'note': note_path
        }
    
    def fetch_wechat(self, urls: list) -> dict:
        """抓取微信公众号文章"""
        articles = self.wechat.fetch_multiple(urls)
        note_path = self.notes.generate_wechat_notes(articles, "AI")
        
        return {
            'status': 'success',
            'articles': articles,
            'count': len(articles),
            'note': note_path
        }
    
    def list_notes(self) -> list:
        """列出所有笔记"""
        return self.notes.list_notes()


# ===== Agent 调用接口 =====

def execute(task: str, params: dict = None) -> dict:
    """Agent 调用接口"""
    scraper = PythonLearningScraper()
    
    if params is None:
        params = {}
    
    if task == "youtube_search":
        query = params.get("query", "Python")
        max_results = params.get("max_results", 20)
        return scraper.search_youtube(query, max_results)
    
    elif task == "wechat_fetch":
        urls = params.get("urls", [])
        return scraper.fetch_wechat(urls)
    
    elif task == "list_notes":
        return {'notes': scraper.list_notes()}
    
    else:
        return {'status': 'error', 'message': f'Unknown task: {task}'}


# ===== 测试 =====

if __name__ == "__main__":
    scraper = PythonLearningScraper()
    
    print("="*50)
    print("Testing YouTube Search")
    print("="*50)
    
    result = scraper.search_youtube("Python", 3)
    print(f"Status: {result['status']}")
    print(f"Videos found: {result['count']}")
    
    print("\n" + "="*50)
    print("Notes:")
    print("="*50)
    for note in scraper.list_notes():
        print(f"  - {note}")
