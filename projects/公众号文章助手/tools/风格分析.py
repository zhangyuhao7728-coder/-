#!/usr/bin/env python3
"""
风格学习系统 V2
深度分析写作风格
"""
import os
import re
import json
from collections import Counter
from datetime import datetime

class StyleAnalyzer:
    """风格分析器"""
    
    # 风格特征库
    TONE_PATTERNS = {
        '轻松': ['哈哈', '呀', '啊', '呢', '吧', '哦', '嗯', '嘿', '哇', '太棒了', '真好', '不错'],
        '专业': ['例如', '比如', '即', '以及', '通过', '基于', '实现', '通常', '一般'],
        '故事型': ['当时', '后来', '于是', '然后', '之前', '那次', '记得', '突然'],
        '科普': ['简单来说', '通俗来说', '本质是', '核心是', '关键在于'],
    }
    
    STRUCTURE_PATTERNS = {
        '问题引入型': ['什么是', '为什么', '怎么样', '如何'],
        '故事引入型': ['记得', '有一次', '之前', '刚开始'],
        '结论先行型': ['首先', '总结', '核心', '关键'],
        '对比型': ['但是', '然而', '相比', '不同', '区别'],
    }
    
    OPENING_PATTERNS = [
        '大家好', 'Hi', 'hi', '各位', '小伙伴', '朋友们', '大家好呀',
        '今天', '最近', '最近在', '刷到', '看到',
    ]
    
    CLOSING_PATTERNS = [
        '有问题评论区见', '欢迎关注', '点个赞', '有问题评论区',
        '欢迎指正', '一起学习', '一起进步', '感谢阅读', '谢谢观看',
    ]
    
    def __init__(self):
        self.style_db_path = 'style/style_database.json'
    
    def analyze(self, content: str, title: str = '') -> dict:
        """全面分析风格"""
        
        return {
            'title_analysis': self.analyze_title(title) if title else {},
            'tone_analysis': self.analyze_tone(content),
            'sentence_analysis': self.analyze_sentences(content),
            'structure_analysis': self.analyze_structure(content),
            'format_analysis': self.analyze_format(content),
            'expression_analysis': self.analyze_expressions(content),
            'emoji_analysis': self.analyze_emoji(content),
            'overall_style': self.get_overall_style(content),
        }
    
    def analyze_title(self, title: str) -> dict:
        """分析标题风格"""
        result = {
            'length': len(title),
            'has_number': bool(re.search(r'\d+', title)),
            'has_question': '？' in title or '?' in title,
            'has_emoji': bool(re.search(r'[\U00010000-\U0010ffff]', title)),
            'has_brackets': '【' in title or '[' in title or '(' in title,
            'type': self.get_title_type(title),
        }
        
        return result
    
    def get_title_type(self, title: str) -> str:
        """判断标题类型"""
        if re.search(r'^\d+[\.、]', title):
            return '数字列表型'
        elif '？' in title or '?' in title:
            return '提问型'
        elif any(w in title for w in ['教你', '教你', '技巧', '方法', '攻略']):
            return '干货型'
        elif any(w in title for w in ['原来', '竟然', '没想到', '揭秘']):
            return '震惊型'
        elif any(w in title for w in ['我的', '我是', '我如何']):
            return '个人经历型'
        else:
            return '普通型'
    
    def analyze_tone(self, content: str) -> dict:
        """分析语气风格"""
        content_lower = content.lower()
        
        scores = {}
        for tone, patterns in self.TONE_PATTERNS.items():
            score = sum(content.count(p) for p in patterns)
            scores[tone] = score
        
        # 找出主要语气
        if max(scores.values()) > 0:
            main_tone = max(scores, key=scores.get)
        else:
            main_tone = '中性'
        
        return {
            'main_tone': main_tone,
            'scores': scores,
            'has_humor': scores['轻松'] > 3,
            'has_story': scores['故事型'] > 2,
        }
    
    def analyze_sentences(self, content: str) -> dict:
        """分析句子特点"""
        # 移除代码块
        text = re.sub(r'```[\s\S]*?```', '', content)
        
        # 分割句子
        sentences = re.split(r'[。！？!?\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {'avg_length': 0, 'short_ratio': 0, 'type': '短句'}
        
        # 统计
        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        
        short_count = sum(1 for l in lengths if l < 20)
        short_ratio = short_count / len(lengths)
        
        # 判断类型
        if avg_length < 20:
            sentence_type = '短句为主'
        elif avg_length < 40:
            sentence_type = '中等句'
        else:
            sentence_type = '长句为主'
        
        return {
            'total_sentences': len(sentences),
            'avg_length': int(avg_length),
            'short_ratio': int(short_ratio * 100),
            'type': sentence_type,
            'max_length': max(lengths),
            'min_length': min(lengths),
        }
    
    def analyze_structure(self, content: str) -> dict:
        """分析文章结构"""
        lines = content.split('\n')
        
        # 提取章节标题
        headings = []
        for line in lines:
            if line.strip().startswith('#'):
                headings.append(line.strip())
        
        # 分析结构模式
        structure_type = '平铺直叙'
        for pattern, keywords in self.STRUCTURE_PATTERNS.items():
            if any(k in content for k in keywords):
                structure_type = pattern
                break
        
        return {
            'headings': headings,
            'heading_count': len(headings),
            'structure_type': structure_type,
            'has_intro': any(k in content[:500] for k in ['背景', '最近', '今天', '首先']),
            'has_summary': any(k in content[-500:] for k in ['总结', '最后', '总之', '总的来说']),
            'has_interaction': any(k in content for k in ['评论区', '评论', '点赞']),
        }
    
    def analyze_format(self, content: str) -> dict:
        """分析格式特点"""
        return {
            'has_numbering': bool(re.search(r'^\d+[\.、]', content, re.MULTILINE)),
            'has_tables': '|' in content and '---' in content,
            'has_code_blocks': '```' in content,
            'has_blockquote': '>' in content,
            'has_dividers': '---' in content,
            'has_horizontal_rules': '___' in content,
            'use_bold': '**' in content or '__' in content,
        }
    
    def analyze_expressions(self, content: str) -> dict:
        """分析常用表达"""
        # 检查开场白
        opening = None
        for pattern in self.OPENING_PATTERNS:
            if pattern in content[:300]:
                opening = pattern
                break
        
        # 检查结尾语
        closing = None
        for pattern in self.CLOSING_PATTERNS:
            if pattern in content[-300:]:
                closing = pattern
                break
        
        # 过渡词
        transitions = []
        transition_words = ['首先', '然后', '接着', '其次', '最后', '总结', '总的来说']
        for word in transition_words:
            if word in content:
                transitions.append(word)
        
        # 总结词
        summary_words = []
        for word in ['总之', '总的来说', '总结一下', '最后']:
            if word in content:
                summary_words.append(word)
        
        return {
            'opening': opening,
            'closing': closing,
            'transitions': transitions[:5],
            'summary_words': summary_words,
            'call_to_action': any(k in content for k in ['关注', '点赞', '评论', '转发']),
        }
    
    def analyze_emoji(self, content: str) -> dict:
        """分析Emoji使用"""
        # 提取emoji
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', re.U)
        emojis = emoji_pattern.findall(content)
        
        emoji_count = len(emojis)
        text_length = len(content.replace('\n', ''))
        
        # 密度
        density = emoji_count / max(text_length, 1) * 100
        
        # 常用emoji
        emoji_counter = Counter(emojis)
        common = emoji_counter.most_common(10)
        
        return {
            'count': emoji_count,
            'density': round(density, 2),
            'common': [e[0] for e in common],
            'usage_level': '大量' if density > 2 else '适中' if density > 0.5 else '少量' if emoji_count > 0 else '无',
        }
    
    def get_overall_style(self, content: str) -> dict:
        """获取整体风格"""
        tone = self.analyze_tone(content)
        sentence = self.analyze_sentences(content)
        emoji = self.analyze_emoji(content)
        structure = self.analyze_structure(content)
        
        # 综合评分
        score = 0
        features = []
        
        if tone['main_tone'] != '中性':
            features.append(tone['main_tone'])
            score += 1
        
        if sentence['type'] == '短句为主':
            features.append('短句')
            score += 1
        
        if emoji['usage_level'] == '适中':
            features.append('适度emoji')
            score += 1
        elif emoji['usage_level'] == '大量':
            features.append('多emoji')
            score += 1
        
        if structure['has_interaction']:
            features.append('互动型')
            score += 1
        
        return {
            'style_name': '+'.join(features) if features else '简洁',
            'score': score,
            'description': self.get_style_description(features),
        }
    
    def get_style_description(self, features: list) -> str:
        """风格描述"""
        descriptions = {
            '轻松': '语言轻松幽默，容易读懂',
            '故事型': '以故事开头，引发共鸣',
            '专业': '语言专业，逻辑性强',
            '短句': '短句为主，节奏快',
            '多emoji': '表情丰富，生动有趣',
            '适度emoji': '偶尔用emoji，增加趣味',
            '互动型': '引导评论互动',
        }
        
        return '，'.join([descriptions.get(f, f) for f in features]) if features else '简洁实用'
    
    def save_style(self, name: str, style: dict):
        """保存风格"""
        os.makedirs('style', exist_ok=True)
        
        # 加载现有
        db = {}
        if os.path.exists(self.style_db_path):
            with open(self.style_db_path, 'r', encoding='utf-8') as f:
                db = json.load(f)
        
        db[name] = {
            **style,
            'saved_at': datetime.now().isoformat()
        }
        
        with open(self.style_db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)

def analyze_style(content: str, title: str = '') -> dict:
    """分析风格"""
    analyzer = StyleAnalyzer()
    return analyzer.analyze(content, title)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = analyze_style(content)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法: python style_analyzer.py article.md")
