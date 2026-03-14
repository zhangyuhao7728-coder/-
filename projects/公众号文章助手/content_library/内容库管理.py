#!/usr/bin/env python3
"""内容库管理系统"""
import os
import json
from datetime import datetime

class ContentLibrary:
    def __init__(self, lib_dir='content_library'):
        self.lib_dir = lib_dir
        self.db_file = f'{lib_dir}/library.json'
        self.library = self.load_library()
    
    def load_library(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'articles': [], 'topics': [], 'tags': []}
    
    def save_library(self):
        os.makedirs(self.lib_dir, exist_ok=True)
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.library, f, ensure_ascii=False, indent=2)
    
    def add_article(self, title, content, tags):
        self.library['articles'].append({
            'title': title,
            'content': content,
            'tags': tags,
            'created_at': datetime.now().isoformat()
        })
        for tag in tags:
            if tag not in self.library['tags']:
                self.library['tags'].append(tag)
        self.save_library()
    
    def search_by_tag(self, tag):
        return [a for a in self.library['articles'] if tag in a.get('tags', [])]
    
    def list_all(self):
        return self.library['articles']
    
    def stats(self):
        return {
            'total': len(self.library['articles']),
            'tags': len(self.library['tags'])
        }

if __name__ == '__main__':
    lib = ContentLibrary()
    
    print("="*40)
    print("📚 内容库管理系统")
    print("="*40)
    
    stats = lib.stats()
    print(f"\n📊 统计:")
    print(f"   文章数: {stats['total']}")
    print(f"   标签数: {stats['tags']}")
    
    print(f"\n📝 最近文章:")
    for a in lib.list_all()[-5:]:
        print(f"   • {a['title']}")
