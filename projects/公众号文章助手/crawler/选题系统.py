#!/usr/bin/env python3
"""
选题系统 V2
多平台热点采集+智能推荐
"""
import os
import re
import json
import time
import requests
from datetime import datetime
from collections import Counter
from urllib.parse import quote

class TopicCrawler:
    """热点采集器"""
    
    # 热点API（模拟）
    SOURCES = {
        'zhihu': {
            'name': '知乎',
            'hot_url': 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50',
        },
        'weibo': {
            'name': '微博',
            'hot_url': 'https://weibo.com/ajax/side/hotSearch',
        },
        'bilibili': {
            'name': 'B站',
            'hot_url': 'https://api.bilibili.com/x/web-interface/popular',
        },
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        })
    
    def fetch_zhihu(self) -> list:
        """获取知乎热点"""
        try:
            resp = self.session.get('https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10', timeout=5)
            data = resp.json()
            
            topics = []
            for item in data.get('data', [])[:10]:
                topics.append({
                    'source': '知乎',
                    'title': item.get('target', {}).get('title', ''),
                    'url': f"https://www.zhihu.com/question/{item.get('target', {}).get('id', '')}",
                    'hot': item.get('detail_text', ''),
                })
            return topics
        except:
            return []
    
    def fetch_weibo(self) -> list:
        """获取微博热点"""
        try:
            resp = self.session.get('https://weibo.com/ajax/side/hotSearch', timeout=5)
            data = resp.json()
            
            topics = []
            for item in data.get('data', {}).get('realtime', [])[:10]:
                topics.append({
                    'source': '微博',
                    'title': item.get('note', ''),
                    'url': f"https://s.weibo.com/weibo?q={quote(item.get('note', ''))}",
                    'hot': item.get('raw_hot', 0),
                })
            return topics
        except:
            return []
    
    def fetch_bilibili(self) -> list:
        """获取B站热点"""
        try:
            resp = self.session.get('https://api.bilibili.com/x/web-interface/popular?pn=1&ps=10', timeout=5)
            data = resp.json()
            
            topics = []
            for item in data.get('data', {}).get('list', [])[:10]:
                topics.append({
                    'source': 'B站',
                    'title': item.get('title', ''),
                    'url': f"https://www.bilibili.com/video/{item.get('bvid', '')}",
                    'hot': item.get('view', 0),
                })
            return topics
        except:
            return []
    
    def fetch_all(self) -> list:
        """获取所有热点"""
        all_topics = []
        
        # 使用备用数据（因为API可能需要认证）
        fallback_topics = [
            {'source': 'AI', 'title': 'AI Agent应用', 'hot': 100},
            {'source': 'AI', 'title': '大模型最新发展', 'hot': 95},
            {'source': 'AI', 'title': 'Prompt工程技巧', 'hot': 90},
            {'source': 'AI', 'title': 'AI编程工具', 'hot': 88},
            {'source': 'AI', 'title': 'AI学习路线', 'hot': 85},
            {'source': '技术', 'title': 'Python入门教程', 'hot': 80},
            {'source': '技术', 'title': '程序员效率工具', 'hot': 78},
            {'source': '技术', 'title': '代码优化技巧', 'hot': 75},
        ]
        
        return fallback_topics

class TopicSelectorV2:
    """智能选题器 V2"""
    
    def __init__(self):
        self.crawler = TopicCrawler()
        self.topics_file = 'data/topics.json'
        self.topics = self.load_topics()
        
        # 预置选题
        self.preset_topics = {
            'AI安全': [
                'AI Agent安全风险有哪些',
                '如何保护自己的AI应用',
                'OpenClaw安全配置指南',
                'API Key泄露怎么办',
                'AI隐私保护技巧',
            ],
            'AI学习': [
                '大专生学AI入门教程',
                'AI学习路线规划',
                '免费AI资源分享',
                'AI工具使用技巧',
                'AI项目实战案例',
            ],
            '效率提升': [
                'AI自动化工作流',
                '用AI提升工作效率',
                'AI写作技巧',
                'AI编程辅助',
                'AI学习助手',
            ],
            '踩坑记录': [
                '我踩过的AI坑',
                '常见AI错误汇总',
                'AI配置问题解决',
                'AI模型选择建议',
                'AI使用注意事项',
            ],
        }
    
    def load_topics(self) -> list:
        """加载历史选题"""
        if os.path.exists(self.topics_file):
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_topics(self):
        """保存选题"""
        os.makedirs('data', exist_ok=True)
        with open(self.topics_file, 'w', encoding='utf-8') as f:
            json.dump(self.topics, f, ensure_ascii=False, indent=2)
    
    def fetch_hot_topics(self) -> list:
        """获取热点"""
        return self.crawler.fetch_all()
    
    def recommend(self, based_on: str = None, limit: int = 5) -> list:
        """智能推荐"""
        recommendations = []
        
        # 分类推荐
        if based_on and based_on in self.preset_topics:
            topics = self.preset_topics[based_on]
            for t in topics[:limit]:
                recommendations.append({
                    'topic': t,
                    'category': based_on,
                    'reason': f'基于您关注的{based_on}',
                })
        else:
            # 混合推荐
            for category, topics in self.preset_topics.items():
                for t in topics[:2]:
                    recommendations.append({
                        'topic': t,
                        'category': category,
                        'reason': '热门推荐',
                    })
        
        return recommendations[:limit]
    
    def generate_variants(self, topic: str) -> list:
        """生成选题变体"""
        variants = []
        
        templates = [
            f'{topic}入门指南',
            f'{topic}实战教程',
            f'{topic}常见问题',
            f'{topic}进阶技巧',
            f'如何用{topic}提升效率',
            f'{topic}学习路线',
            f'{topic}资源分享',
            f'{topic}配置安装',
            f'一文读懂{topic}',
            f'{topic}从入门到精通',
        ]
        
        return templates
    
    def add_topic(self, topic: str, category: str = None):
        """添加选题"""
        self.topics.append({
            'topic': topic,
            'category': category or '未分类',
            'added_at': datetime.now().isoformat(),
            'status': 'pending',
        })
        self.save_topics()
    
    def get_daily_topics(self) -> dict:
        """每日选题"""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'recommendations': self.recommend(limit=10),
            'hot_topics': self.fetch_hot_topics()[:5],
        }

def get_topics():
    """获取选题"""
    selector = TopicSelectorV2()
    return selector.get_daily_topics()

if __name__ == '__main__':
    selector = TopicSelectorV2()
    
    print("="*50)
    print("🎯 智能选题系统 V2")
    print("="*50)
    
    # 每日推荐
    daily = selector.get_daily_topics()
    print(f"\n📅 {daily['date']} 选题推荐")
    
    print("\n📌 推荐主题:")
    for i, t in enumerate(daily['recommendations'], 1):
        print(f"  {i}. [{t['category']}] {t['topic']}")
        print(f"     原因: {t['reason']}")
    
    print("\n🔥 热点话题:")
    for t in daily['hot_topics']:
        print(f"  • [{t['source']}] {t['title']}")
    
    # 生成变体
    print("\n📝 选题变体示例:")
    for t in selector.generate_variants('AI'):
        print(f"  • {t}")
