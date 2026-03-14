#!/usr/bin/env python3
"""
SEO优化系统 V2
提升文章搜索排名
"""
import os
import re
import json
from datetime import datetime
from collections import Counter

class SEOOptimizer:
    """SEO优化器"""
    
    def __init__(self):
        self.keywords_file = 'data/keywords.json'
        self.keywords = self.load_keywords()
    
    def load_keywords(self) -> dict:
        """加载关键词库"""
        if os.path.exists(self.keywords_file):
            with open(self.keywords_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'ai': ['AI', '人工智能', '大模型', 'GPT'],
            'python': ['Python', '编程', '代码', '开发'],
            '安全': ['安全', '防护', '风险', '隐私'],
        }
    
    def extract_keywords(self, text: str, top_n: int = 10) -> list:
        """提取关键词"""
        # 简单实现：统计词频
        # 实际应该用jieba分词
        
        # 移除标点
        text = re.sub(r'[^\w]', ' ', text)
        words = text.split()
        
        # 过滤短词
        words = [w for w in words if len(w) >= 2]
        
        # 统计
        counter = Counter(words)
        
        return counter.most_common(top_n)
    
    def analyze_title(self, title: str) -> dict:
        """分析标题SEO"""
        result = {
            'length': len(title),
            'score': 0,
            'issues': [],
            'suggestions': [],
        }
        
        # 长度检查
        if 15 <= len(title) <= 30:
            result['score'] += 30
        elif len(title) < 15:
            result['issues'].append('标题太短')
            result['suggestions'].append('建议15-30字')
        else:
            result['issues'].append('标题太长')
            result['suggestions'].append('建议控制在30字内')
        
        # 关键词检查
        has_keyword = False
        for category, keywords in self.keywords.items():
            for kw in keywords:
                if kw in title:
                    has_keyword = True
                    result['score'] += 20
                    break
        
        if not has_keyword:
            result['issues'].append('缺少关键词')
            result['suggestions'].append('添加核心关键词')
        
        # 数字检查
        if re.search(r'\d+', title):
            result['score'] += 15
        else:
            result['suggestions'].append('可添加数字吸引点击')
        
        # 符号检查
        if '？' in title or '!' in title:
            result['score'] += 10
        
        # 悬念词
        suspense_words = ['竟然', '原来', '揭秘', '必看']
        if any(w in title for w in suspense_words):
            result['score'] += 10
        
        return result
    
    def analyze_content(self, content: str) -> dict:
        """分析内容SEO"""
        result = {
            'word_count': len(content.replace('\n', '')),
            'keyword_density': 0,
            'issues': [],
            'suggestions': [],
        }
        
        # 字数
        if result['word_count'] < 1000:
            result['issues'].append('内容太少')
            result['suggestions'].append('建议1500字以上')
        elif result['word_count'] > 4000:
            result['issues'].append('内容太长')
            result['suggestions'].append('建议精简到3000字内')
        
        # 关键词密度
        all_keywords = []
        for kws in self.keywords.values():
            all_keywords.extend(kws)
        
        total_words = result['word_count']
        keyword_count = sum(content.count(kw) for kw in all_keywords)
        
        if total_words > 0:
            density = keyword_count / total_words * 100
            result['keyword_density'] = round(density, 2)
            
            # 理想密度2-8%
            if density < 2:
                result['issues'].append('关键词密度过低')
                result['suggestions'].append('建议2-8%')
            elif density > 8:
                result['issues'].append('关键词密度过高')
                result['suggestions'].append('可能被判定为作弊')
        
        # 段落检查
        paragraphs = content.split('\n\n')
        if len(paragraphs) < 5:
            result['issues'].append('段落太少')
            result['suggestions'].append('增加段落更易阅读')
        
        return result
    
    def optimize_title(self, title: str, keyword: str = None) -> list:
        """优化标题"""
        optimized = []
        
        # 原始标题
        optimized.append(title)
        
        # 添加关键词变体
        if keyword:
            if not keyword in title:
                optimized.append(f'{keyword}: {title}')
            optimized.append(f'{title}（必看）')
            optimized.append(f'关于{title}，看这篇就够了')
            optimized.append(f'{title}入门到精通')
        
        # 数字变体
        if not re.search(r'\d+', title):
            optimized.insert(1, f'5个{title}技巧')
            optimized.insert(2, f'3分钟了解{title}')
        
        # 问题变体
        if '？' not in title and '?' not in title:
            optimized.append(f'{title}？一篇搞定')
        
        return optimized[:5]
    
    def generate_meta(self, title: str, content: str = '', 
                    max_desc: int = 120) -> dict:
        """生成Meta信息"""
        # 描述
        desc = content[:200].replace('\n', ' ').strip()
        if len(desc) > max_desc:
            desc = desc[:max_desc] + '...'
        
        return {
            'title': title,
            'description': desc,
            'keywords': [k for kws in self.keywords.values() for k in kws][:5],
        }

def optimize_seo(title: str = None, content: str = None) -> dict:
    """SEO优化"""
    optimizer = SEOOptimizer()
    
    result = {}
    
    if title:
        result['title_analysis'] = optimizer.analyze_title(title)
        result['title_variants'] = optimizer.optimize_title(title)
    
    if content:
        result['content_analysis'] = optimizer.analyze_content(content)
    
    return result

if __name__ == '__main__':
    optimizer = SEOOptimizer()
    
    print("="*50)
    print("🔍 SEO优化系统")
    print("="*50)
    
    # 测试标题分析
    title = "AI安全入门指南"
    analysis = optimizer.analyze_title(title)
    
    print(f"\n📌 标题: {title}")
    print(f"📊 SEO评分: {analysis['score']}/100")
    print(f"📝 问题: {', '.join(analysis['issues']) if analysis['issues'] else '无'}")
    
    # 优化标题
    print(f"\n✨ 优化标题:")
    for t in optimizer.optimize_title(title, 'AI'):
        print(f"  • {t}")
    
    # Meta
    content = "这是一篇关于AI安全的文章..."
    meta = optimizer.generate_meta(title, content)
    print(f"\n📝 Meta:")
    print(f"  标题: {meta['title']}")
    print(f"  描述: {meta['description']}")
