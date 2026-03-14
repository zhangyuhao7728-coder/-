#!/usr/bin/env python3
"""
风格提取器 - 从参考文章中提取写作风格
用法：
  python tools/风格分析.py --file article.md
  python tools/风格分析.py --file article.md --output my_style
"""
import os
import sys
import re
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
STYLE_DB = os.path.join(PROJECT_DIR, 'style', 'style_database.json')

# 高频表达词库
OPENING_PATTERNS = [
    "大家好", "Hi", "hi", "各位", "小伙伴", "朋友们",
    "最近", "今天", "今天想", "最近在", "刷到",
]

CLOSING_PATTERNS = [
    "有问题评论区见", "欢迎关注", "点个赞", "有问题评论区",
    "欢迎指正", "一起学习", "一起进步", "感谢阅读",
]

TRANSITION_PATTERNS = [
    "接下来", "下面", "首先", "然后", "最后", "总结一下",
    "总的来说", "总的来说", "那么", "所以",
]

QUESTION_PATTERNS = [
    "是不是", "有没有", "会不会", "要不要", "为什么",
    "怎么做", "是什么", "怎么办", "到底是",
]

def extract_structure(md_text: str) -> dict:
    """提取文章结构"""
    lines = md_text.split('\n')
    structure = []
    current_h1 = None
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('# '):
            if current_h1:
                structure.append(current_h1)
            current_h1 = {'type': 'h1', 'title': line[2:], 'subsections': []}
        elif line.startswith('## ') and current_h1:
            current_h1['subsections'].append(line[3:])
        elif line.startswith('## ') and not current_h1:
            structure.append({'type': 'h2', 'title': line[3:]})
        elif line.startswith('### ') and current_h1:
            current_h1['subsections'].append(line[4:])
    
    if current_h1:
        structure.append(current_h1)
    
    # 简化结构
    simple_structure = []
    for s in structure:
        if s.get('subsections'):
            simple_structure.append(s['title'])
            simple_structure.extend(s['subsections'][:3])
        else:
            simple_structure.append(s['title'])
    
    return simple_structure[:10]  # 最多10个

def detect_structure_type(structure: list) -> str:
    """判断结构类型"""
    if not structure:
        return "未知"
    
    # 检查是否有特定模式
    has_story = any(s for s in structure if any(k in s for k in ['背景', '故事', '经历', '之前']))
    has_problem = any(s for s in structure if any(k in s for k in ['问题', '为什么', '是什么', '坑']))
    has_solution = any(s for s in structure if any(k in s for k in ['解决', '方法', '方案', '步骤']))
    has_summary = any(s for s in structure if any(k in s for k in ['总结', '最后', '结论']))
    
    if has_story and has_problem and has_solution:
        return "故事引入型"
    elif has_problem and has_solution:
        return "问题解决型"
    elif has_solution:
        return "教程步骤型"
    else:
        return "经验分享型"

def analyze_tone(md_text: str) -> dict:
    """分析语气"""
    text = md_text.lower()
    
    # 轻松词汇
    casual_words = ['哈哈', '呀', '啊', '呢', '吧', '哦', '嗯', '嘿', '哇']
    casual_count = sum(text.count(w) for w in casual_words)
    
    # 专业词汇
    professional_words = ['例如', '比如', '即', '以及', '通过', '基于', '实现']
    professional_count = sum(text.count(w) for w in professional_words)
    
    # 故事词汇
    story_words = ['当时', '后来', '于是', '然后', '之前', '那次', '那次']
    story_count = sum(text.count(w) for w in story_words)
    
    # 判断语气
    if casual_count > professional_count:
        tone = "轻松"
    elif story_count > casual_count:
        tone = "故事型"
    else:
        tone = "专业"
    
    return {
        "tone": tone,
        "casual_score": casual_count,
        "professional_score": professional_count,
        "story_score": story_count,
    }

def analyze_sentence(md_text: str) -> dict:
    """分析句子特点"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', md_text)
    
    # 统计句子
    sentences = re.split(r'[。！？!?\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {"length": "short", "avg_length": 0}
    
    # 平均长度
    avg_length = sum(len(s) for s in sentences) / len(sentences)
    
    # 短句比例
    short_sentences = sum(1 for s in sentences if len(s) < 20)
    short_ratio = short_sentences / len(sentences)
    
    if avg_length < 20:
        length_style = "短句"
    elif avg_length < 40:
        length_style = "中等"
    else:
        length_style = "长句"
    
    return {
        "length": length_style,
        "avg_length": int(avg_length),
        "short_ratio": int(short_ratio * 100),
    }

def analyze_emoji(md_text: str) -> dict:
    """分析emoji使用"""
    # 提取emoji
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', re.U)
    emojis = emoji_pattern.findall(md_text)
    
    emoji_count = len(emojis)
    text_length = len(md_text.replace('\n', ''))
    
    # 密度
    density = emoji_count / max(text_length, 1) * 100
    
    # 常用emoji
    from collections import Counter
    common = Counter(emojis).most_common(5)
    
    if emoji_count == 0:
        usage = "无"
    elif density > 2:
        usage = "大量"
    elif density > 0.5:
        usage = "适中"
    else:
        usage = "少量"
    
    return {
        "usage": usage,
        "count": emoji_count,
        "density": round(density, 2),
        "common": [e[0] for e in common],
    }

def analyze_format(md_text: str) -> dict:
    """分析格式特点"""
    has_numbering = bool(re.search(r'^\d+[\.、]', md_text, re.MULTILINE))
    has_tables = '|' in md_text and '---' in md_text
    has_code = '```' in md_text
    has_blockquote = '>' in md_text
    
    return {
        "use_numbering": has_numbering,
        "use_tables": has_tables,
        "use_code_blocks": has_code,
        "use_blockquote": has_blockquote,
    }

def extract_high_frequency(md_text: str) -> dict:
    """提取高频表达"""
    # 检查开场
    opening = None
    for pattern in OPENING_PATTERNS:
        if pattern in md_text[:200]:
            opening = pattern
            break
    
    # 检查结尾
    closing = None
    for pattern in CLOSING_PATTERNS:
        if pattern in md_text[-200:]:
            closing = pattern
            break
    
    # 检查过渡词
    transitions = []
    for pattern in TRANSITION_PATTERNS:
        if pattern in md_text:
            transitions.append(pattern)
    
    return {
        "opening": opening,
        "closing": closing,
        "transitions": transitions[:5],
    }

def extract_style(md_text: str) -> dict:
    """提取完整风格"""
    structure = extract_structure(md_text)
    
    return {
        "structure": structure,
        "structure_type": detect_structure_type(structure),
        "tone": analyze_tone(md_text),
        "sentence": analyze_sentence(md_text),
        "emoji": analyze_emoji(md_text),
        "format": analyze_format(md_text),
        "expressions": extract_high_frequency(md_text),
    }

def save_style(name: str, style: dict):
    """保存风格到数据库"""
    # 读取现有
    if os.path.exists(STYLE_DB):
        with open(STYLE_DB, 'r', encoding='utf-8') as f:
            db = json.load(f)
    else:
        db = {}
    
    # 添加新风格
    db[name] = style
    
    # 保存
    os.makedirs(os.path.dirname(STYLE_DB), exist_ok=True)
    with open(STYLE_DB, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已保存风格: {name}")

def load_style(name: str) -> dict:
    """加载风格"""
    if os.path.exists(STYLE_DB):
        with open(STYLE_DB, 'r', encoding='utf-8') as f:
            db = json.load(f)
            return db.get(name, {})
    return {}

def main():
    parser = argparse.ArgumentParser(description='风格分析工具')
    parser.add_argument('--file', '-f', help='文章文件')
    parser.add_argument('--output', '-o', help='保存风格名称')
    parser.add_argument('--preview', '-p', action='store_true', help='预览')
    parser.add_argument('--name', '-n', default='自定义', help='风格名称')
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print("🎨 风格分析工具")
    print(f"{'='*50}\n")
    
    if args.file:
        # 读取文章
        with open(args.file, 'r', encoding='utf-8') as f:
            md_text = f.read()
        
        # 分析风格
        style = extract_style(md_text)
        
        # 预览
        if args.preview:
            print(f"📐 结构类型: {style['structure_type']}")
            print(f"🗣️ 语气: {style['tone']['tone']}")
            print(f"📏 句子: {style['sentence']['length']} (平均{style['sentence']['avg_length']}字)")
            print(f"😀 Emoji: {style['emoji']['usage']} ({style['emoji']['count']}个)")
            print(f"📝 格式: ", end="")
            fmt = style['format']
            parts = []
            if fmt['use_numbering']: parts.append("编号")
            if fmt['use_tables']: parts.append("表格")
            if fmt['use_code_blocks']: parts.append("代码")
            print(", ".join(parts) if parts else "无")
            
            expr = style['expressions']
            print(f"\n💬 开场: {expr['opening'] or '无固定'}")
            print(f"👋 结尾: {expr['closing'] or '无固定'}")
        
        # 保存
        if args.output:
            # 简化风格数据
            simple_style = {
                "tone": style['tone']['tone'],
                "sentence_length": style['sentence']['length'],
                "emoji": style['emoji']['usage'] != "无",
                "structure": style['structure'][:6],
                "opening": expr['opening'],
                "closing": expr['closing'],
            }
            save_style(args.output, simple_style)
        
        print(f"\n✅ 分析完成!")
    
    else:
        # 列出已有风格
        styles = load_style('')
        if styles:
            print("已有风格:")
            for name in styles:
                print(f"  - {name}")
        else:
            print("暂无保存的风格")

if __name__ == '__main__':
    main()
