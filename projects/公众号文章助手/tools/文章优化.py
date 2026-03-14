#!/usr/bin/env python3
"""
文章质量优化工具
功能：
- 优化标题
- 提升阅读性
- 提高公众号推荐概率
用法：
  python tools/文章优化.py --file article.md
  python tools/文章优化.py --title "原标题"
"""
import os
import sys
import re
import argparse

# 优质标题特征
TITLE_PATTERNS = {
    '数字': ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '1', '2', '3', '4', '5'],
    '痛点': ['不会', '不敢', '不知道', '如何', '怎么办', '为什么', '总是', '又'],
    '价值': ['技巧', '方法', '攻略', '指南', '教程', '神器', '必备', '终极'],
    '情绪': ['竟然', '原来', '终于', '秒', '简单', '轻松', '绝了', '炸裂'],
}

def generate_title_variants(topic: str) -> list:
    """生成多种标题风格"""
    titles = []
    
    # 数字型
    titles.append(f"5个{topic}技巧，第3个最实用")
    titles.append(f"3分钟学会{topic}，新手必看")
    titles.append(f"{topic}的7个正确方式")
    
    # 痛点型
    titles.append(f"不会{topic}？3步搞定")
    titles.append(f"{topic}常见问题合集")
    titles.append(f"为什么你{topic}总是失败？")
    
    # 价值型
    titles.append(f"{topic}完整指南")
    titles.append(f"{topic}必备神器")
    titles.append(f"最强{topic}攻略")
    
    # 情绪型
    titles.append(f"原来{topic}这么简单！")
    titles.append(f"竟然{topic}，后悔没早知道")
    titles.append(f"{topic}，绝了！")
    
    # 个人IP型
    titles.append(f"我是如何搞定{topic}的")
    titles.append(f"一个{topic}，让我xxx")
    titles.append(f"{topic}，小白也能学会")
    
    return titles

def optimize_title(title: str) -> dict:
    """优化标题"""
    result = {
        'original': title,
        'score': 0,
        'issues': [],
        'suggestions': [],
    }
    
    # 评分
    length = len(title)
    if 15 <= length <= 30:
        result['score'] += 30
    elif length < 15:
        result['score'] += 10
        result['issues'].append('标题太短')
    else:
        result['score'] += 10
        result['issues'].append('标题太长')
    
    # 检查特征
    has_number = any(p in title for p in TITLE_PATTERNS['数字'])
    has_pain = any(p in title for p in TITLE_PATTERNS['痛点'])
    has_value = any(p in title for p in TITLE_PATTERNS['价值'])
    has_emotion = any(p in title for p in TITLE_PATTERNS['情绪'])
    
    if has_number:
        result['score'] += 20
    else:
        result['suggestions'].append('添加数字更吸引人')
    
    if has_pain:
        result['score'] += 20
    else:
        result['suggestions'].append('添加痛点词（如：不会/如何/为什么）')
    
    if has_value:
        result['score'] += 15
    else:
        result['suggestions'].append('添加价值词（如：技巧/方法/神器）')
    
    if has_emotion:
        result['score'] += 15
    else:
        result['suggestions'].append('添加情绪词（如：竟然/原来/绝了）')
    
    # 检查符号
    if '？' in title or '!' in title:
        result['score'] += 10
    else:
        result['suggestions'].append('添加标点增加悬念（？/!）')
    
    if '【' in title or '[' in title:
        result['score'] += 10
    else:
        result['suggestions'].append('添加括号增加特色（【】）')
    
    return result

def improve_readability(text: str) -> dict:
    """提升阅读性"""
    lines = text.split('\n')
    
    # 统计
    avg_length = sum(len(l) for l in lines) / max(len(lines), 1)
    long_paras = sum(1 for l in lines if len(l) > 200)
    
    suggestions = []
    
    # 段落长度建议
    if avg_length > 100:
        suggestions.append(f"平均段落太长({int(avg_length)}字)，建议拆短")
    
    if long_paras > 3:
        suggestions.append(f"{long_paras}个段落过长，建议拆分成小段")
    
    # 建议
    if not suggestions:
        suggestions.append("阅读性良好")
    
    return {
        'avg_length': int(avg_length),
        'long_paragraphs': long_paras,
        'suggestions': suggestions
    }

def check_recommendation(text: str) -> dict:
    """检查公众号推荐概率"""
    score = 0
    suggestions = []
    
    # 1. 原创性
    if '原创' in text[:200] or '原创' in text[-200:]:
        score += 20
    else:
        suggestions.append('添加原创声明')
    
    # 2. 互动引导
    互动词 = ['评论区', '评论', '点赞', '关注', '转发']
    if any(w in text for w in 互动词):
        score += 15
    else:
        suggestions.append('添加互动引导')
    
    # 3. 干货内容
    代码词 = ['代码', '命令', '步骤', '方法', '技巧']
    if any(w in text for w in 代码词):
        score += 20
    else:
        suggestions.append('添加干货内容')
    
    # 4. 配图建议
    if '![' in text:
        score += 15
    else:
        suggestions.append('添加图片')
    
    # 5. 字数
    word_count = len(text.replace('\n', ''))
    if 1500 <= word_count <= 3500:
        score += 20
    elif word_count < 1000:
        score += 5
        suggestions.append('字数偏少，建议1500字以上')
    else:
        score += 10
        suggestions.append('字数偏多，建议精简')
    
    # 6. 热点关联
    热点词 = ['最新', '2026', '今年', '最近']
    if any(w in text for w in 热点词):
        score += 10
    else:
        suggestions.append('可适当添加时间词')
    
    return {
        'score': score,
        'level': '高' if score >= 70 else '中' if score >= 50 else '低',
        'suggestions': suggestions
    }

def optimize_article(file_path: str = None, text: str = None) -> dict:
    """优化文章"""
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1) if title_match else ''
    
    # 优化
    result = {
        'title_analysis': optimize_title(title) if title else None,
        'title_variants': generate_title_variants(title.replace(' ', '')) if title else [],
        'readability': improve_readability(text),
        'recommendation': check_recommendation(text),
    }
    
    return result

def main():
    parser = argparse.ArgumentParser(description='文章质量优化')
    parser.add_argument('--file', '-f', help='文章文件')
    parser.add_argument('--title', '-t', help='优化标题')
    parser.add_argument('--text', help='文章内容')
    parser.add_argument('--variants', '-v', action='store_true', help='生成标题变体')
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print("📝 文章质量优化")
    print(f"{'='*50}\n")
    
    if args.title:
        # 优化标题
        result = optimize_title(args.title)
        print(f"📌 原标题: {result['original']}")
        print(f"📊 评分: {result['score']}/100")
        
        if result['issues']:
            print(f"\n⚠️ 问题:")
            for issue in result['issues']:
                print(f"   - {issue}")
        
        if result['suggestions']:
            print(f"\n💡 建议:")
            for s in result['suggestions']:
                print(f"   - {s}")
        
        if args.variants:
            print(f"\n📝 标题变体:")
            variants = generate_title_variants(args.title.replace(' ', ''))
            for i, v in enumerate(variants[:8], 1):
                print(f"   {i}. {v}")
    
    elif args.file:
        # 优化整篇文章
        result = optimize_article(file_path=args.file)
        
        if result['title_analysis']:
            ta = result['title_analysis']
            print(f"📌 标题: {ta['original']}")
            print(f"📊 标题评分: {ta['score']}/100\n")
        
        # 阅读性
        print(f"📖 阅读性:")
        rb = result['readability']
        print(f"   平均段落: {rb['avg_length']}字")
        for s in rb['suggestions']:
            print(f"   - {s}")
        
        # 推荐概率
        print(f"\n📈 推荐概率:")
        rec = result['recommendation']
        print(f"   评分: {rec['score']}/100 ({rec['level']}质量)")
        for s in rec['suggestions']:
            print(f"   - {s}")
        
        # 标题变体
        if args.variants and result['title_analysis']:
            print(f"\n📝 优化标题:")
            for i, v in enumerate(result['title_variants'][:5], 1):
                print(f"   {i}. {v}")
    
    else:
        print("用法:")
        print("  python tools/文章优化.py --title '原标题'")
        print("  python tools/文章优化.py --file article.md")
        print("  python tools/文章优化.py --file article.md --variants")

if __name__ == '__main__':
    main()
