#!/usr/bin/env python3
"""Skill管理器"""
import os
import json
import subprocess

class SkillManager:
    def __init__(self):
        self.skills_dir = os.path.expanduser('~/.openclaw/skills/')
        self.db_file = 'data/Skill库.json'
        self.library = self.load_library()
    
    def load_library(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'skills': []}
    
    def save_library(self):
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.library, f, ensure_ascii=False, indent=2)
    
    def scan_skills(self):
        """扫描Skills目录"""
        skills = []
        if os.path.exists(self.skills_dir):
            for f in os.listdir(self.skills_dir):
                if f.endswith('.yaml'):
                    path = os.path.join(self.skills_dir, f)
                    skills.append({
                        'name': f.replace('.yaml', ''),
                        'file': f,
                        'path': path,
                        'size': os.path.getsize(path)
                    })
        return skills
    
    def list_skills(self):
        """列出所有Skills"""
        skills = self.scan_skills()
        
        print("="*60)
        print("🛠️ Skill管理器")
        print("="*60)
        print(f"\n📦 已安装: {len(skills)}个\n")
        
        categories = {
            'production': [],
            'learning': [],
            'system': [],
            'other': []
        }
        
        for s in skills:
            name = s['name'].lower()
            if any(k in name for k in ['文章', '写作', '生成']):
                categories['production'].append(s)
            elif any(k in name for k in ['学习', '算法', 'python', 'ai']):
                categories['learning'].append(s)
            elif any(k in name for k in ['安全', '监控', '检查']):
                categories['system'].append(s)
            else:
                categories['other'].append(s)
        
        for cat, items in categories.items():
            if items:
                cat_name = {'production': '📝 内容生产', 'learning': '📚 AI学习', 'system': '🔧 系统工具', 'other': '📦 其他'}
                print(f"【{cat_name.get(cat, cat)}】")
                for s in items:
                    print(f"  • {s['name']}")
                print()
    
    def add_skill(self, name, description, category):
        """添加Skill到库"""
        self.library['skills'].append({
            'name': name,
            'description': description,
            'category': category,
            'added_at': '2026-03-14'
        })
        self.save_library()
    
    def search_skills(self, keyword):
        """搜索Skills"""
        results = []
        for s in self.library.get('skills', []):
            if keyword.lower() in s.get('name', '').lower():
                results.append(s)
        return results

if __name__ == '__main__':
    manager = SkillManager()
    manager.list_skills()
