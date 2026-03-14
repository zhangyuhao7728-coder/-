#!/usr/bin/env python3
"""
内容管理系统 (CMS)
管理已发布和待发布的文章
"""
import os
import json
from datetime import datetime
from pathlib import Path

class ContentManager:
    """内容管理器"""
    
    def __init__(self, content_dir: str = None):
        self.content_dir = content_dir or 'output/published_articles'
        os.makedirs(self.content_dir, exist_ok=True)
        
        self.db_file = os.path.join(self.content_dir, 'cms_database.json')
        self.db = self.load_db()
    
    def load_db(self) -> dict:
        """加载数据库"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'articles': [],
            'categories': ['AI安全', 'AI学习', '效率提升', '踩坑记录', '经验分享'],
            'tags': [],
        }
    
    def save_db(self):
        """保存数据库"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def add_article(self, title: str, content: str = '', category: str = None, 
                   tags: list = None, status: str = 'draft') -> dict:
        """添加文章"""
        article = {
            'id': len(self.db['articles']) + 1,
            'title': title,
            'content': content,
            'category': category or '未分类',
            'tags': tags or [],
            'status': status,  # draft, published
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'published_at': None,
            'views': 0,
            'likes': 0,
        }
        
        self.db['articles'].append(article)
        self.save_db()
        
        return article
    
    def publish_article(self, article_id: int) -> bool:
        """发布文章"""
        for article in self.db['articles']:
            if article['id'] == article_id:
                article['status'] = 'published'
                article['published_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_db()
                return True
        return False
    
    def list_articles(self, status: str = None, category: str = None) -> list:
        """列出文章"""
        articles = self.db['articles']
        
        if status:
            articles = [a for a in articles if a['status'] == status]
        if category:
            articles = [a for a in articles if a['category'] == category]
        
        return articles
    
    def get_stats(self) -> dict:
        """获取统计"""
        articles = self.db['articles']
        
        total = len(articles)
        published = len([a for a in articles if a['status'] == 'published'])
        drafts = len([a for a in articles if a['status'] == 'draft'])
        
        # 分类统计
        categories = {}
        for a in articles:
            cat = a['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'total': total,
            'published': published,
            'drafts': drafts,
            'categories': categories,
        }
    
    def search(self, keyword: str) -> list:
        """搜索文章"""
        results = []
        for a in self.db['articles']:
            if keyword.lower() in a['title'].lower():
                results.append(a)
        return results

def cms_add(title: str, category: str = None) -> dict:
    """添加文章"""
    cms = ContentManager()
    return cms.add_article(title, category=category)

def cms_list(status: str = None) -> list:
    """列出文章"""
    cms = ContentManager()
    return cms.list_articles(status)

def cms_stats() -> dict:
    """统计"""
    cms = ContentManager()
    return cms.get_stats()

if __name__ == '__main__':
    cms = ContentManager()
    
    print("="*50)
    print("📚 内容管理系统")
    print("="*50)
    
    # 统计
    stats = cms.get_stats()
    print(f"\n📊 统计:")
    print(f"   总文章: {stats['total']}")
    print(f"   已发布: {stats['published']}")
    print(f"   草稿: {stats['drafts']}")
    
    if stats['categories']:
        print(f"\n📂 分类:")
        for cat, count in stats['categories'].items():
            print(f"   {cat}: {count}")
    
    # 最近文章
    articles = cms.list_articles()[-5:]
    if articles:
        print(f"\n📝 最近文章:")
        for a in articles:
            print(f"   [{a['status']}] {a['title']}")
