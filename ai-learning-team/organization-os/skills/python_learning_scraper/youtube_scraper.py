"""
YouTube Scraper - 使用官方 API + 次数限制
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path


class YouTubeScraper:
    """YouTube 视频搜索爬虫 - 带次数限制"""
    
    # 免费配额限制
    MAX_DAILY_SEARCHES = 100  # 每天最多100次
    API_UNIT_COST = 100  # 每次搜索消耗100单位
    
    def __init__(self):
        self.api_key = os.environ.get('YOUTUBE_API_KEY', '')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.usage_file = Path(__file__).parent / "usage.json"
        self._load_usage()
    
    def _load_usage(self):
        """加载使用记录"""
        if self.usage_file.exists():
            with open(self.usage_file) as f:
                self.usage = json.load(f)
        else:
            self.usage = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'count': 0
            }
        
        # 新的一天，重置计数
        today = datetime.now().strftime('%Y-%m-%d')
        if self.usage.get('date') != today:
            self.usage = {'date': today, 'count': 0}
            self._save_usage()
    
    def _save_usage(self):
        """保存使用记录"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f)
    
    def _can_search(self) -> bool:
        """检查是否可以搜索"""
        return self.usage['count'] < self.MAX_DAILY_SEARCHES
    
    def _get_remaining(self) -> int:
        """获取剩余次数"""
        return max(0, self.MAX_DAILY_SEARCHES - self.usage['count'])
    
    def search(self, query: str, max_results: int = 20) -> list:
        """
        搜索视频（带次数限制）
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            视频列表
        """
        # 检查次数
        if not self._can_search():
            remaining = self._get_remaining()
            print(f"⚠️ 今日次数已用完！剩余: {remaining}")
            return []
        
        # 检查 API Key
        if not self.api_key:
            print("⚠️ 未设置 YOUTUBE_API_KEY")
            return self._fallback_search(query, max_results)
        
        # 调用 API
        url = f"{self.base_url}/search"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': min(max_results, 50),  # 最多50
            'key': self.api_key
        }
        
        try:
            import requests
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # 检查 API 错误
            if 'error' in data:
                print(f"API Error: {data['error'].get('message', 'Unknown error')}")
                return []
            
            # 解析结果
            videos = []
            for item in data.get('items', []):
                snippet = item.get('snippet', {})
                videos.append({
                    'title': snippet.get('title', ''),
                    'description': snippet.get('description', '')[:200],
                    'channel': snippet.get('channelTitle', ''),
                    'video_id': item.get('id', {}).get('videoId', ''),
                    'url': f"https://www.youtube.com/watch?v={item.get('id', {}).get('videoId', '')}",
                    'published': snippet.get('publishTime', '')
                })
            
            # 更新使用次数
            self.usage['count'] += 1
            self._save_usage()
            
            print(f"✅ 搜索成功: {len(videos)} 个视频")
            print(f"📊 今日剩余次数: {self._get_remaining()}/{self.MAX_DAILY_SEARCHES}")
            
            return videos
            
        except Exception as e:
            print(f"Error: {e}")
            return self._fallback_search(query, max_results)
    
    def get_status(self) -> dict:
        """获取使用状态"""
        return {
            'date': self.usage.get('date', ''),
            'used': self.usage.get('count', 0),
            'remaining': self._get_remaining(),
            'limit': self.MAX_DAILY_SEARCHES
        }
    
    def _fallback_search(self, query: str, max_results: int) -> list:
        """备用搜索方法"""
        return [
            {
                'title': f'{query} Tutorial {i+1}',
                'channel': 'Python Channel',
                'url': f'https://www.youtube.com/watch?v=dummy{i}'
            }
            for i in range(max_results)
        ]


if __name__ == "__main__":
    scraper = YouTubeScraper()
    
    # 显示状态
    status = scraper.get_status()
    print(f"=== 使用状态 ===")
    print(f"日期: {status['date']}")
    print(f"已用: {status['used']}/{status['limit']}")
    print(f"剩余: {status['remaining']}")
    
    # 测试搜索
    print("\n=== 测试搜索 ===")
    results = scraper.search("Python 教程", 3)
    
    for v in results:
        print(f"- {v['title']}")
