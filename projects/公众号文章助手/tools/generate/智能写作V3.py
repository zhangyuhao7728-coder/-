#!/usr/bin/env python3
"""
智能写作系统 V3 - 基于学习到的写作技巧
使用爆款文章分析出的技巧生成内容
"""
import os
import json
from datetime import datetime
from typing import Dict, List

class SmartWriter:
    """智能写作者 - V3"""
    
    def __init__(self):
        self.tech_lib_file = 'data/写作技巧库.json'
        self.tech_lib = self.load_tech_lib()
    
    def load_tech_lib(self) -> dict:
        if os.path.exists(self.tech_lib_file):
            with open(self.tech_lib_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'techniques': [], 'structures': [], 'title_templates': []}
    
    def generate_title_v2(self, topic: str, style: str = '数字+痛点') -> List[str]:
        """生成标题 V2 - 基于学习到的模板"""
        
        # 从技巧库获取模板
        templates = [t['template'] for t in self.tech_lib.get('title_templates', [])]
        
        # 如果没有，使用默认模板
        if not templates:
            templates = [
                f'🔥 {topic}必看！X个必须知道的坑',
                f'⚠️ 关于{topic}，国家都发声了',
                f'📚 X分钟学会{topic}',
                f'🦞"养虾人"必看！{topic}安全指南',
                f'🔒 {topic}小白入门，看这一篇就够了',
            ]
        
        # 生成变体
        titles = []
        for t in templates[:8]:
            t = t.replace('{topic}', topic)
            t = t.replace('{X}', str(hash(topic) % 9 + 1))  # 随机数字
            titles.append(t)
        
        # 添加数字变体
        titles.insert(0, f'5分钟了解{topic}')
        titles.insert(1, f'3个{topic}必须知道的风险')
        
        return titles[:8]
    
    def generate_intro(self, topic: str, style: str = '故事') -> str:
        """生成开头 - 基于学习到的技巧"""
        
        intros = {
            '故事': [
                f'大家好，最近{topic}这个话题很火...',
                f'今天想和大家聊聊{topic}...',
                f'最近我身边发生了一件事...',
            ],
            '热点': [
                f'最近科技圈没人能躲过{topic}吧?',
                f'{topic}最近火遍全网...',
                f'关于{topic}，国家都发声了...',
            ],
            '问题': [
                f'你是不是也在用{topic}?',
                f'关于{topic}，你了解多少?',
                f'{topic}到底安不安全?',
            ]
        }
        
        return intros.get(style, intros['故事'])
    
    def generate_body(self, topic: str, structure: str = '问题-解决') -> List[dict]:
        """生成正文结构 - 基于学习到的结构"""
        
        structures = {
            '问题-解决': [
                {'title': f'{topic}是什么?', 'desc': '用通俗语言解释'},
                {'title': '有什么风险?', 'desc': '说明具体风险'},
                {'title': '为什么会有风险?', 'desc': '解释原因'},
                {'title': '如何防范?', 'desc': '给出具体方案'},
                {'title': '总结', 'desc': '回顾要点'},
            ],
            '起承转合': [
                {'title': '引入', 'desc': '从热点/故事切入'},
                {'title': '背景', 'desc': '说明背景'},
                {'title': '发展', 'desc': '展开分析'},
                {'title': '高潮', 'desc': '核心要点'},
                {'title': '总结', 'desc': '行动建议'},
            ],
            '三段式': [
                {'title': '是什么', 'desc': '概念解释'},
                {'title': '为什么', 'desc': '原因分析'},
                {'title': '怎么办', 'desc': '解决方案'},
            ]
        }
        
        return structures.get(structure, structures['问题-解决'])
    
    def apply_technique(self, content: str, technique: str) -> str:
        """应用写作技巧"""
        
        techniques = {
            '加数字': lambda c: c.replace('很多', '28万+').replace('一些', '6%').replace('大量', '20万台'),
            '加故事': lambda c: c + '\n\n我朋友就遇到过这种情况...',
            '加比喻': lambda c: c + '\n\n这就像...',
            '加数据': lambda c: c + '\n\n据工信部监测数据显示...',
            '加专家': lambda c: c + '\n\n专家表示：...',
        }
        
        if technique in techniques:
            return techniques[technique](content)
        return content
    
    def generate_ending(self, topic: str, style: str = '行动') -> str:
        """生成结尾 - 基于学习到的技巧"""
        
        endings = {
            '行动': [
                f'希望这篇文章能帮到你。使用{topic}时，一定要记住：安全第一，谨慎操作！',
                f'如果你觉得有用，点个赞再走？有问题评论区见~',
            ],
            '升华': [
                f'技术在进步，安全意识也要跟上。在享受{topic}带来便利的同时，别忘了保护好自己。',
                f'AI让生活更美好，但安全永远是底线。共勉~',
            ],
            '互动': [
                f'关于{topic}，你有什么经历?欢迎评论区分享~',
                f'有问题评论区见，我是余豪，一名AI小白 🚀',
            ]
        }
        
        return endings.get(style, endings['行动'])
    
    def generate_article_v2(self, topic: str, article_type: str = '科普') -> dict:
        """生成完整文章 V2 - 使用学习到的技巧"""
        
        # 生成标题
        titles = self.generate_title_v2(topic)
        
        # 生成开头
        intro = self.generate_intro(topic, '热点')
        
        # 生成结构
        body = self.generate_body(topic, '问题-解决')
        
        # 生成结尾
        ending = self.generate_ending(topic, '行动')
        
        return {
            'topic': topic,
            'type': article_type,
            'titles': titles,
            'title': titles[0],
            'intro': intro,
            'body': body,
            'ending': ending,
            'created_at': datetime.now().isoformat(),
            'techniques_used': [
                '数字开头',
                '热点引入',
                '结构化正文',
                '行动建议结尾',
            ]
        }

def write_article_v2(topic: str, article_type: str = '科普') -> dict:
    """智能写作 V2"""
    writer = SmartWriter()
    return writer.generate_article_v2(topic, article_type)

if __name__ == '__main__':
    writer = SmartWriter()
    
    print("="*50)
    print("✍️ 智能写作系统 V3")
    print("="*50)
    
    # 生成示例
    article = writer.generate_article_v2('OpenClaw安全', '科普')
    
    print(f"\n📌 标题: {article['title']}")
    print(f"\n📝 标题选项:")
    for t in article['titles']:
        print(f"  • {t}")
    
    print(f"\n📖 开场: {article['intro']}")
    
    print(f"\n📑 文章结构:")
    for i, s in enumerate(article['body'], 1):
        print(f"  {i}. {s['title']}: {s['desc']}")
    
    print(f"\n👋 结尾: {article['ending']}")
    
    print(f"\n✅ 使用技巧: {', '.join(article['techniques_used'])}")
