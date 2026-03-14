#!/usr/bin/env python3
"""
文章结构解析工具
用法：
  python tools/文章结构解析.py --file article.md
  python tools/文章结构解析.py --file article.md --style
"""
import os
import sys
import re
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PARSED_DIR = os.path.join(PROJECT_DIR, 'data', 'parsed_articles')

def extract_structure(md_text: str) -> dict:
    """提取文章结构"""
    lines = md_text.split('\n')
    
    sections = []
    current_section = None
    content_lines = []
    
    for line in lines:
        line = line.strip()
        
        # 标题
        if line.startswith('# '):
            if current_section:
                current_section['content'] = '\n'.join(content_lines).strip()
                sections.append(current_section)
            current_section = {'level': 1, 'title': line[2:], 'content': ''}
            content_lines = []
        elif line.startswith('## '):
            if current_section and content_lines:
                current_section['content'] = '\n'.join(content_lines).strip()
                sections.append(current_section)
            current_section = {'level': 2, 'title': line[3:], 'content': ''}
            content_lines = []
        elif line.startswith('### '):
            if current_section and content_lines:
                current_section['content'] = '\n'.join(content_lines).strip()
                sections.append(current_section)
            current_section = {'level': 3, 'title': line[4:], 'content': ''}
            content_lines = []
        elif line and current_section:
            content_lines.append(line)
    
    # 最后一个section
    if current_section:
        current_section['content'] = '\n'.join(content_lines).strip()
        sections.append(current_section)
    
    return sections

def extract_intro(md_text: str) -> str:
    """提取开场部分"""
    lines = md_text.split('\n')
    intro_lines = []
    in_intro = True
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            in_intro = False
        elif in_intro and line:
            intro_lines.append(line)
        
        if len(intro_lines) > 5:
            break
    
    return '\n'.join(intro_lines)

def analyze_style(md_text: str) -> dict:
    """分析文章风格"""
    # 统计
    lines = md_text.split('\n')
    total_lines = len([l for l in lines if l.strip()])
    total_chars = len(md_text)
    total_words = len(md_text.replace('\n', ''))
    
    # 段落长度
    paragraphs = [p.strip() for p in md_text.split('\n\n') if p.strip()]
    avg_para_length = sum(len(p) for p in paragraphs) / max(len(paragraphs), 1)
    
    # emoji统计
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', re.U)
    emoji_count = len(emoji_pattern.findall(md_text))
    
    # 句子统计
    sentences = re.split(r'[。！？.!?]', md_text)
    avg_sentence_length = total_words / max(len(sentences), 1)
    
    # 特点判断
    if avg_para_length < 50:
        para_style = "short"
    elif avg_para_length < 150:
        para_style = "medium"
    else:
        para_style = "long"
    
    if emoji_count / max(total_words, 1) > 0.02:
        emoji_usage = "high"
    elif emoji_count / max(total_words, 1) > 0.005:
        emoji_usage = "moderate"
    else:
        emoji_usage = "low"
    
    return {
        "total_lines": total_lines,
        "total_chars": total_chars,
        "total_words": total_words,
        "avg_paragraph_length": int(avg_para_length),
        "paragraph_style": para_style,
        "emoji_count": emoji_count,
        "emoji_usage": emoji_usage,
        "avg_sentence_length": int(avg_sentence_length),
        "has_code_blocks": "```" in md_text,
        "has_tables": "|" in md_text and "---" in md_text,
    }

def detect_template_type(md_text: str, structure: list) -> str:
    """判断文章类型"""
    text = md_text.lower()
    
    # 关键词匹配
    if any(k in text for k in ['教程', '使用', '安装', '配置', '步骤', '如何']):
        return "教程类"
    elif any(k in text for k in ['踩坑', '问题', '错误', '解决', '排查', 'bug']):
        return "踩坑记录"
    elif any(k in text for k in ['经验', '心得', '感悟', '复盘', '分享']):
        return "经验类"
    else:
        return "经验类"  # 默认

def parse_article(md_file: str, analyze_style_flag: bool = True) -> dict:
    """解析文章"""
    # 读取文件
    with open(md_file, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "无标题"
    
    # 提取结构
    sections = extract_structure(md_text)
    
    # 提取开场
    intro = extract_intro(md_text)
    
    # 构建结果
    result = {
        "title": title,
        "intro": intro[:200],  # 限制长度
        "sections_count": len(sections),
        "sections": [
            {
                "level": s['level'],
                "title": s['title'],
                "content_length": len(s['content'])
            }
            for s in sections[:10]  # 最多10个
        ],
        "template_type": detect_template_type(md_text, sections)
    }
    
    # 风格分析
    if analyze_style_flag:
        result["style"] = analyze_style(md_text)
    
    return result

def main():
    parser = argparse.ArgumentParser(description='文章结构解析')
    parser.add_argument('--file', '-f', required=True, help='文章文件')
    parser.add_argument('--style', '-s', action='store_true', help='包含风格分析')
    parser.add_argument('--output', '-o', help='输出JSON文件')
    parser.add_argument('--preview', '-p', action='store_true', help='预览结果')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)
    
    print(f"\n{'='*40}")
    print("📊 文章结构解析")
    print(f"{'='*40}\n")
    
    # 解析
    result = parse_article(args.file, args.style)
    
    # 输出
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存到: {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 预览
    if args.preview:
        print(f"\n{'='*40}")
        print(f"📌 标题: {result['title']}")
        print(f"📝 类型: {result['template_type']}")
        print(f"📑 章节数: {result['sections_count']}")
        if 'style' in result:
            s = result['style']
            print(f"📏 平均段落: {s['avg_paragraph_length']}字")
            print(f"😀 Emoji: {s['emoji_count']}个 ({s['emoji_usage']})")
            print(f"📝 段落风格: {s['paragraph_style']}")

if __name__ == '__main__':
    main()
