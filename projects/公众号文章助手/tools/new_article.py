#!/usr/bin/env python3
"""
新建公众号文章
用法：
  python new_article.py --type 教程类 --title "我的文章标题"
  python new_article.py --type 经验类 --title "我的经验"
  python new_article.py --type 踩坑记录 --title "问题排查"
"""
import os
import sys
import argparse
from datetime import datetime

# 配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, 'templates')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# 模板文件映射
TEMPLATE_MAP = {
    '教程类': '教程类.md',
    '经验类': '经验类.md',
    '踩坑记录': '踩坑记录.md',
}

def get_template(template_type: str) -> str:
    """获取模板内容"""
    if template_type not in TEMPLATE_MAP:
        print(f"❌ 未知模板类型: {template_type}")
        print(f"可用类型: {', '.join(TEMPLATE_MAP.keys())}")
        sys.exit(1)
    
    template_path = os.path.join(TEMPLATES_DIR, TEMPLATE_MAP[template_type])
    
    if not os.path.exists(template_path):
        print(f"❌ 模板文件不存在: {template_path}")
        sys.exit(1)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def create_article(title: str, template_type: str) -> str:
    """创建新文章"""
    # 生成文件名
    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_title = ''.join(c for c in title if c.isalnum() or c in ' -_').strip()
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 获取模板
    template = get_template(template_type)
    
    # 替换标题
    content = template.replace('标题', title)
    
    # 添加日期
    content = content.replace(
        '> 一句话说明这篇文章解决什么问题',
        f'> {datetime.now().strftime("%Y年%m月%d日")}'
    )
    
    # 写入文件
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='新建公众号文章')
    parser.add_argument('--type', '-t', required=True, 
                       choices=list(TEMPLATE_MAP.keys()),
                       help='文章类型')
    parser.add_argument('--title', required=True,
                       help='文章标题')
    parser.add_argument('--open', '-o', action='store_true',
                       help='创建后打开文件')
    
    args = parser.parse_args()
    
    print(f"📝 创建文章: {args.title}")
    print(f"📂 类型: {args.type}")
    
    filepath = create_article(args.title, args.type)
    
    print(f"✅ 已创建: {filepath}")
    
    if args.open:
        os.system(f'open "{filepath}"')

if __name__ == '__main__':
    main()
