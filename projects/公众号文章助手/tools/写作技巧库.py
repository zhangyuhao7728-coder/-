#!/usr/bin/env python3
"""
写作技巧库 - 从优秀文章中学习写作技巧
基于对爆款文章的分析提取
"""
import json
import os
from datetime import datetime
from typing import Dict, List

class WritingTechniqueLibrary:
    """写作技巧库"""
    
    def __init__(self):
        self.db_file = 'data/写作技巧库.json'
        self.db = self.load_db()
    
    def load_db(self) -> dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'techniques': [],
            'structures': [],
            'title_templates': [],
            'learned_from': []
        }
    
    def save_db(self):
        os.makedirs('data', exist_ok=True)
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def add_technique(self, technique: dict):
        """添加技巧"""
        technique['added_at'] = datetime.now().isoformat()
        self.db['techniques'].append(technique)
        self.save_db()
    
    def add_structure(self, structure: dict):
        """添加结构模板"""
        structure['added_at'] = datetime.now().isoformat()
        self.db['structures'].append(structure)
        self.save_db()
    
    def add_title_template(self, template: str, source: str):
        """添加标题模板"""
        self.db['title_templates'].append({
            'template': template,
            'source': source,
            'added_at': datetime.now().isoformat()
        })
        self.save_db()
    
    def learn_from_article(self, article_analysis: dict):
        """从文章分析中学习"""
        source = article_analysis.get('source', '未知')
        
        # 提取标题模板
        for title in article_analysis.get('title_templates', []):
            self.add_title_template(title, source)
        
        # 提取写作技巧
        for tech in article_analysis.get('techniques', []):
            self.add_technique({
                'name': tech.get('name'),
                'description': tech.get('description'),
                'example': tech.get('example'),
                'source': source
            })
        
        # 提取结构模板
        for struct in article_analysis.get('structures', []):
            self.add_structure({
                'name': struct.get('name'),
                'steps': struct.get('steps'),
                'description': struct.get('description'),
                'source': source
            })
        
        # 记录学习来源
        self.db['learned_from'].append({
            'source': source,
            'title': article_analysis.get('title'),
            'date': datetime.now().isoformat()
        })
        self.save_db()
    
    def get_title_templates(self) -> List[str]:
        return [t['template'] for t in self.db.get('title_templates', [])]
    
    def get_techniques(self) -> List[dict]:
        return self.db.get('techniques', [])
    
    def get_structures(self) -> List[dict]:
        return self.db.get('structures', [])
    
    def generate_title(self, topic: str, style: str = '数字+痛点') -> List[str]:
        """根据模板生成标题"""
        templates = self.get_title_templates()
        
        if not templates:
            # 默认模板
            templates = [
                f'{topic}必看！X个必须知道的坑',
                f'关于{topic}，国家都发声了',
                f'X分钟学会{topic}',
                f'小白入门{topic}，看这一篇就够了',
            ]
        
        # 简单替换
        titles = []
        for t in templates[:5]:
            titles.append(t.replace('{topic}', topic))
        
        return titles
    
    def get_structure(self, article_type: str = '科普') -> dict:
        """获取文章结构"""
        structures = {
            '科普': [
                {'step': 1, 'name': '引入', 'desc': '从热点/故事切入'},
                {'step': 2, 'name': '问题', 'desc': '说明是什么问题'},
                {'step': 3, 'name': '原因', 'desc': '用通俗语言解释'},
                {'step': 4, 'name': '影响', 'desc': '说明后果'},
                {'step': 5, 'name': '解决方案', 'desc': '给出具体建议'},
                {'step': 6, 'name': '总结', 'desc': '回顾+行动建议'},
            ],
            '经验分享': [
                {'step': 1, 'name': '背景', 'desc': '为什么写这篇文章'},
                {'step': 2, 'name': '经历', 'desc': '真实故事'},
                {'step': 3, 'name': '踩坑', 'desc': '遇到的问题'},
                {'step': 4, 'name': '解决', 'desc': '如何解决'},
                {'step': 5, 'name': '总结', 'desc': '学到的经验'},
            ],
            '教程': [
                {'step': 1, 'name': '背景', 'desc': '为什么学这个'},
                {'step': 2, 'name': '准备', 'desc': '需要什么'},
                {'step': 3, 'name': '步骤', 'desc': '具体操作'},
                {'step': 4, 'name': '注意', 'desc': '常见问题'},
                {'step': 5, 'name': '总结', 'desc': '要点回顾'},
            ]
        }
        
        return {
            'type': article_type,
            'structure': structures.get(article_type, structures['科普'])
        }
    
    def report(self) -> dict:
        """生成学习报告"""
        return {
            'total_techniques': len(self.db.get('techniques', [])),
            'total_structures': len(self.db.get('structures', [])),
            'total_templates': len(self.db.get('title_templates', [])),
            'learned_from': self.db.get('learned_from', []),
            'title_templates': self.get_title_templates()[:10],
        }

# 从已分析文章学习
def learn_from_橙文章():
    """从阿橙文章学习"""
    library = WritingTechniqueLibrary()
    
    analysis = {
        'source': '开发者阿橙',
        'title': '28w+Star背后：OpenClaw用户必须知道的4个安全坑',
        'title_templates': [
            '28w+Star背后：{topic}必须知道的X个坑',
            '{X}必看！{topic}的X个风险',
            '关于{topic}，我朋友亲身经历了...',
        ],
        'techniques': [
            {'name': '数字开头', 'description': '用具体数字吸引眼球', 'example': '28w+Star'},
            {'name': '故事引入', 'description': '用真实故事引起共鸣', 'example': '朋友删邮件崩溃'},
            {'name': '生活比喻', 'description': '用生活化比喻解释技术', 'example': '把钥匙交给陌生人'},
            {'name': '数据支撑', 'description': '用数据增加可信度', 'example': '6%插件是伪装者'},
            {'name': '专家背书', 'description': '引用权威观点', 'example': '奇安信专家说'},
            {'name': '亲身分享', 'description': '用第一人称分享经验', 'example': '我就这么干了'},
            {'name': '解决方案', 'description': '给出具体可操作建议', 'example': '用旧电脑隔离'},
            {'name': '结尾升华', 'description': '总结+情感升华', 'example': '睡个安稳觉'},
        ],
        'structures': [
            {
                'name': '问题引入式',
                'steps': ['热点引入', '故事呈现', '问题分析', '原因解释', '解决方案', '总结建议'],
                'description': '用故事引出问题，再给出解决方案'
            }
        ]
    }
    
    library.learn_from_article(analysis)
    return library.report()

if __name__ == '__main__':
    print("="*50)
    print("📚 写作技巧库")
    print("="*50)
    
    # 学习阿橙的文章
    report = learn_from_橙文章()
    
    print(f"\n📊 学习报告:")
    print(f"   技巧数: {report['total_techniques']}")
    print(f"   结构数: {report['total_structures']}")
    print(f"   标题模板: {report['total_templates']}")
    
    print(f"\n📝 标题模板:")
    for t in report['title_templates'][:5]:
        print(f"   • {t}")
    
    print(f"\n✅ 学习来源:")
    for s in report['learned_from']:
        print(f"   • {s['source']}: {s['title']}")
