#!/usr/bin/env python3
"""
文章总结工具
用法：
  python 文章总结.py input.md
"""
import os
import sys
import re
from datetime import datetime

def extract_title(markdown: str) -> str:
    """提取标题"""
    match = re.search(r'^#\s+(.+)$', markdown, re.MULTILINE)
    return match.group(1) if match else '无标题'

def extract_sections(markdown: str) -> dict:
    """提取文章结构"""
    sections = []
    
    for line in markdown.split('\n'):
        if line.startswith('## '):
            sections.append(('h2', line[3:].strip()))
        elif line.startswith('### '):
            sections.append(('h3', line[4:].strip()))
    
    return sections

def count_words(markdown: str) -> int:
    """统计字数"""
    # 移除代码块
    text = re.sub(r'```[\s\S]*?```', '', markdown)
    # 移除链接
    text = re.sub(r'\[.+?\]\(.+?\)', '', text)
    # 移除图片
    text = re.sub(r'!\[.+?\]\(.+?\)', '', text)
    # 移除特殊字符
    text = re.sub(r'[#*>`|\-]', '', text)
    # 统计
    words = len(text.replace('\n', ''))
    return words

def generate_summary(markdown: str) -> str:
    """生成文章总结"""
    title = extract_title(markdown)
    sections = extract_sections(markdown)
    words = count_words(markdown)
    
    # 预估阅读时间（每分钟200字）
    read_time = max(1, words // 200)
    
    summary = f'''
📊 文章总结
============

标题: {title}
字数: ~{words} 字
预计阅读: {read_time} 分钟

📑 文章结构:
'''
    
    for level, content in sections:
        if level == 'h2':
            summary += f'\n## {content}\n'
        else:
            summary += f'   - {content}\n'
    
    return summary

def main():
    if len(sys.argv) < 2:
        print('用法: python 文章总结.py input.md')
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    summary = generate_summary(markdown)
    print(summary)

if __name__ == '__main__':
    main()
