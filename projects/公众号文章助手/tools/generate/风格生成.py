#!/usr/bin/env python3
"""
AI写作系统 V2
基于爆文模型生成文章
"""
import os
import json
from datetime import datetime
from typing import Dict, List

class AIWriter:
    """AI写作器"""
    
    def __init__(self):
        self.style_db_path = 'style/style_database.json'
        self.styles = self.load_styles()
    
    def load_styles(self) -> dict:
        """加载风格"""
        if os.path.exists(self.style_db_path):
            with open(self.style_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def generate_structure(self, topic: str, article_type: str = '经验分享') -> dict:
        """生成文章结构"""
        
        # 根据文章类型生成结构
        structures = {
            '教程': [
                {'type': 'intro', 'title': '背景介绍', 'desc': '为什么学习这个'},
                {'type': 'step', 'title': '环境准备', 'desc': '需要什么条件'},
                {'type': 'step', 'title': '基础概念', 'desc': '核心知识点'},
                {'type': 'step', 'title': '实战操作', 'desc': '手把手演示'},
                {'type': 'summary', 'title': '总结', 'desc': '回顾要点'},
            ],
            '经验分享': [
                {'type': 'intro', 'title': '故事引入', 'desc': '发生了什么'},
                {'type': 'content', 'title': '问题描述', 'desc': '具体是什么情况'},
                {'type': 'content', 'title': '解决过程', 'desc': '我是怎么做的'},
                {'type': 'content', 'title': '经验总结', 'desc': '学到了什么'},
                {'type': 'ending', 'title': '互动引导', 'desc': '欢迎评论'},
            ],
            '踩坑记录': [
                {'type': 'intro', 'title': '问题背景', 'desc': '什么场景下出现'},
                {'type': 'content', 'title': '错误现象', 'desc': '具体报错信息'},
                {'type': 'content', 'title': '排查过程', 'desc': '尝试了哪些方法'},
                {'type': 'content', 'title': '解决方案', 'desc': '最终怎么解决'},
                {'type': 'summary', 'title': '经验教训', 'desc': '以后要注意什么'},
            ],
            '安全科普': [
                {'type': 'intro', 'title': '背景', 'desc': '为什么要注意'},
                {'type': 'content', 'title': '风险说明', 'desc': '具体有哪些风险'},
                {'type': 'content', 'title': '防护方案', 'desc': '如何保护自己'},
                {'type': 'content', 'title': '具体操作', 'desc': '一步步怎么做'},
                {'type': 'ending', 'title': '总结', 'desc': '要点回顾'},
            ],
        }
        
        return structures.get(article_type, structures['经验分享'])
    
    def generate_opening(self, topic: str, style: dict = None) -> str:
        """生成开头"""
        style = style or {}
        tone = style.get('tone', '轻松')
        
        openings = {
            '轻松': f'大家好！今天想和大家聊聊{topic}...',
            '专业': f'本文将详细介绍{topic}的相关内容...',
            '故事型': f'最近在研究{topic}，过程中有一些心得...',
        }
        
        return openings.get(tone, openings['轻松'])
    
    def generate_title(self, topic: str, style: dict = None) -> List[str]:
        """生成标题"""
        titles = [
            f'5分钟学会{topic}',
            f'{topic}入门指南',
            f'关于{topic}，你需要知道这些',
            f'一文读懂{topic}',
            f'{topic}完全指南',
        ]
        
        return titles
    
    def generate_article(self, topic: str, style_name: str = '余豪风格', 
                         article_type: str = '经验分享') -> dict:
        """生成完整文章"""
        
        # 获取风格
        style = self.styles.get(style_name, {})
        
        # 生成结构
        structure = self.generate_structure(topic, article_type)
        
        # 生成标题
        titles = self.generate_title(topic, style)
        
        # 生成开头
        opening = self.generate_opening(topic, style)
        
        article = {
            'title': titles[0],
            'titles': titles,
            'topic': topic,
            'style': style_name,
            'type': article_type,
            'opening': opening,
            'structure': structure,
            'created_at': datetime.now().isoformat(),
        }
        
        return article
    
    def generate_prompt(self, article: dict) -> str:
        """生成LLM提示词"""
        topic = article['topic']
        structure = article['structure']
        
        # 构建结构描述
        structure_desc = '\n'.join([
            f"{i+1}. {s['title']}：{s['desc']}"
            for i, s in enumerate(structure)
        ])
        
        prompt = f"""请根据以下要求写一篇公众号文章：

主题：{topic}

文章结构：
{structure_desc}

要求：
1. 语言生动有趣，接地气
2. 适当使用emoji
3. 开头要吸引人
4. 结构清晰，层次分明
5. 结尾要有互动引导
6. 字数1500-2500字

请开始写作："""
        
        return prompt

def write_article(topic: str, style: str = '余豪风格', 
                  article_type: str = '经验分享') -> dict:
    """生成文章"""
    writer = AIWriter()
    return writer.generate_article(topic, style, article_type)

if __name__ == '__main__':
    writer = AIWriter()
    
    print("="*50)
    print("✍️ AI写作系统")
    print("="*50)
    
    # 生成示例
    article = writer.generate_article('AI安全', '余豪风格', '安全科普')
    
    print(f"\n📌 标题: {article['title']}")
    print(f"\n📝 标题选项:")
    for t in article['titles']:
        print(f"  • {t}")
    
    print(f"\n📖 文章结构:")
    for i, s in enumerate(article['structure'], 1):
        print(f"  {i}. {s['title']}: {s['desc']}")
    
    print(f"\n📝 LLM提示词:")
    print(writer.generate_prompt(article)[:200] + "...")
