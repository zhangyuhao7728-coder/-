#!/usr/bin/env python3
"""
爆文分析系统 V2
分析高阅读文章的共同特征
"""
import os
import re
import json
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, List

class HotArticleAnalyzer:
    """爆文分析器"""
    
    def __init__(self, data_dir: str = 'data/hot_articles'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # 爆文特征库
        self.hot_patterns = {
            'title': {
                '数字': r'\d+[个章节步]',
                '痛点': r'[不会|如何|为什么|怎么办|竟然|原来]',
                '价值': r'[必备|技巧|方法|攻略|指南|神器]',
                '悬念': r'[？|!|...|揭秘]',
                '对比': r'[vs|对比|区别|不同]',
            },
            'opening': {
                '问题引入': r'[是不是|有没有|会不会|为什么]',
                '故事引入': r'[记得|有一次|之前|刚开始]',
                '数据引入': r'[研究|调查|数据显示|根据]',
                '热点引入': r'[最近|今天|热搜|爆了]',
            },
            'structure': {
                '问题-解决': r'[问题|原因|解决|方案|方法]',
                'what-why-how': r'[是什么|为什么|怎么办]',
                '起承转合': r'[首先|然后|接着|最后|总结]',
            },
        }
        
        self.db_file = os.path.join(data_dir, 'hot_db.json')
        self.db = self.load_db()
    
    def load_db(self) -> dict:
        """加载数据库"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'articles': [], 'patterns': {}}
    
    def save_db(self):
        """保存数据库"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)
    
    def add_article(self, article: dict):
        """添加文章"""
        article['analyzed_at'] = datetime.now().isoformat()
        self.db['articles'].append(article)
        self.save_db()
    
    def analyze_title(self, title: str) -> dict:
        """分析标题"""
        result = {
            'length': len(title),
            'has_number': bool(re.search(r'\d+', title)),
            'has_emoji': bool(re.search(r'[\U00010000-\U0010ffff]', title)),
            'has_question': '？' in title or '?' in title,
            'has_exclamation': '！' in title or '!' in title,
            'has_brackets': '【' in title or '[' in title,
            'patterns': [],
        }
        
        # 匹配模式
        for pattern_name, pattern in self.hot_patterns['title'].items():
            if re.search(pattern, title):
                result['patterns'].append(pattern_name)
        
        return result
    
    def analyze_opening(self, content: str) -> dict:
        """分析开头"""
        opening = content[:500]
        
        result = {
            'length': len(opening),
            'type': 'unknown',
            'patterns': [],
        }
        
        for pattern_name, pattern in self.hot_patterns['opening'].items():
            if re.search(pattern, opening):
                result['patterns'].append(pattern_name)
        
        if result['patterns']:
            result['type'] = result['patterns'][0]
        
        return result
    
    def analyze_structure(self, content: str) -> dict:
        """分析结构"""
        # 提取段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        # 提取章节
        headings = []
        for p in paragraphs:
            if p.startswith('#') or re.match(r'^\d+[\.、]', p):
                headings.append(p[:50])
        
        result = {
            'total_paragraphs': len(paragraphs),
            'headings': headings,
            'structure_type': 'unknown',
        }
        
        # 匹配结构
        for pattern_name, pattern in self.hot_patterns['structure'].items():
            if re.search(pattern, content):
                result['structure_type'] = pattern_name
        
        return result
    
    def analyze_rhythm(self, content: str) -> dict:
        """分析节奏"""
        # 句子长度
        sentences = re.split(r'[。！？!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {'avg_length': 0, 'rhythm': 'unknown'}
        
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        
        # 段落长度
        paragraphs = content.split('\n\n')
        avg_para = sum(len(p) for p in paragraphs) / len(paragraphs)
        
        return {
            'avg_sentence_length': int(avg_length),
            'avg_paragraph_length': int(avg_para),
            'total_sentences': len(sentences),
            'rhythm': '快' if avg_length < 25 else '中等' if avg_length < 40 else '慢',
        }
    
    def analyze_ending(self, content: str) -> dict:
        """分析结尾"""
        ending = content[-500:]
        
        result = {
            'has_call_to_action': any(k in ending for k in ['关注', '点赞', '评论', '转发']),
            'has_summary': any(k in ending for k in ['总结', '总之', '最后']),
            'has_question': '？' in ending,
            'type': 'unknown',
        }
        
        if result['has_call_to_action']:
            result['type'] = '互动型'
        elif result['has_summary']:
            result['type'] = '总结型'
        
        return result
    
    def analyze(self, article: dict) -> dict:
        """全面分析"""
        title = article.get('title', '')
        content = article.get('content', '')
        
        return {
            'title_analysis': self.analyze_title(title),
            'opening_analysis': self.analyze_opening(content),
            'structure_analysis': self.analyze_structure(content),
            'rhythm_analysis': self.analyze_rhythm(content),
            'ending_analysis': self.analyze_ending(content),
            'hot_score': self.calculate_hot_score(article),
        }
    
    def calculate_hot_score(self, article: dict) -> int:
        """计算爆文分数"""
        score = 0
        
        title = article.get('title', '')
        
        # 标题分数
        if re.search(r'\d+', title):
            score += 20
        if '？' in title or '?' in title:
            score += 15
        if any(w in title for w in ['必备', '技巧', '神器']):
            score += 15
        if '！' in title or '!' in title:
            score += 10
        
        # 内容分数
        content = article.get('content', '')
        if len(content) > 1500:
            score += 15
        if any(k in content for k in ['评论区', '评论', '关注']):
            score += 15
        if '```' in content:
            score += 10
        
        return min(score, 100)
    
    def get_template(self) -> dict:
        """获取爆文模板"""
        return {
            'title_templates': [
                'X个{topic}技巧，第X个最实用',
                '不会{topic}？3步搞定',
                '为什么你{topic}总是失败？',
                '原来{topic}这么简单！',
                '{topic} vs {topic}，选哪个？',
            ],
            'opening_templates': [
                '最近{topic}话题很火...',
                '你是不是也有这样的困扰...',
                '今天来聊聊{topic}...',
                '很多人问{topic}...',
            ],
            'structure_templates': [
                {
                    'name': '问题-解决',
                    'steps': ['问题描述', '原因分析', '解决方案', '总结']
                },
                {
                    'name': '起承转合',
                    'steps': ['引入', '背景', '发展', '高潮', '总结']
                },
            ],
            'ending_templates': [
                '有问题评论区见！',
                '觉得有用点个赞！',
                '欢迎关注，一起学习！',
                '有问题评论区交流~',
            ],
        }
    
    def get_analysis_report(self) -> dict:
        """生成分析报告"""
        if not self.db['articles']:
            return {'message': '暂无数据'}
        
        # 统计
        total = len(self.db['articles'])
        avg_score = sum(self.calculate_hot_score(a) for a in self.db['articles']) / total
        
        return {
            'total_articles': total,
            'avg_hot_score': int(avg_score),
            'template': self.get_template(),
        }

def analyze_hot(content: str, title: str = '') -> dict:
    """分析爆文特征"""
    analyzer = HotArticleAnalyzer()
    article = {'title': title, 'content': content}
    return analyzer.analyze(article)

if __name__ == '__main__':
    analyzer = HotArticleAnalyzer()
    
    print("="*50)
    print("🔥 爆文分析系统")
    print("="*50)
    
    # 获取模板
    template = analyzer.get_template()
    
    print("\n📝 标题模板:")
    for t in template['title_templates']:
        print(f"  • {t}")
    
    print("\n📖 结构模板:")
    for s in template['structure_templates']:
        print(f"  • {s['name']}: {' → '.join(s['steps'])}")
    
    print("\n👋 结尾模板:")
    for t in template['ending_templates']:
        print(f"  • {t}")
