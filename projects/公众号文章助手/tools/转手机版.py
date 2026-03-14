#!/usr/bin/env python3
"""
Markdown转手机阅读版HTML
用法：
  python 转手机版.py input.md output.html
"""
import os
import sys
import re

def markdown_to_html(markdown_text: str) -> str:
    """Markdown转HTML（公众号手机阅读版）"""
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.8;
            padding: 16px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { font-size: 22px; color: #1a1a1a; margin-bottom: 12px; line-height: 1.4; }
        h2 { font-size: 18px; color: #2c3e50; margin: 24px 0 12px; padding-bottom: 8px; border-bottom: 2px solid #3498db; }
        h3 { font-size: 16px; color: #34495e; margin: 16px 0 8px; }
        p { margin-bottom: 12px; font-size: 15px; }
        .warning { background: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 12px 0; border-radius: 4px; }
        .danger { background: #f8d7da; border-left: 4px solid #dc3545; padding: 12px; margin: 12px 0; border-radius: 4px; }
        .success { background: #d4edda; border-left: 4px solid #28a745; padding: 12px; margin: 12px 0; border-radius: 4px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: "SF Mono", Monaco, monospace; font-size: 13px; }
        pre { background: #2d2d2d; color: #f8f8f2; padding: 12px; border-radius: 8px; overflow-x: auto; margin: 12px 0; font-size: 13px; }
        pre code { background: none; padding: 0; color: #f8f8f2; }
        ul, ol { margin: 12px 0; padding-left: 20px; }
        li { margin-bottom: 8px; font-size: 14px; }
        table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #3498db; color: white; }
        .divider { height: 1px; background: #eee; margin: 20px 0; }
        blockquote { border-left: 4px solid #3498db; padding-left: 12px; color: #666; margin: 12px 0; }
    </style>
</head>
<body>
    <div class="container">
'''
    
    lines = markdown_text.split('\n')
    in_code = False
    in_list = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            html += '</p>\n<p>'
            continue
        
        # 代码块
        if line.startswith('```'):
            if in_code:
                html += '</code></pre>\n'
                in_code = False
            else:
                html += f'<pre><code>'
                in_code = True
            continue
        
        if in_code:
            html += line + '\n'
            continue
        
        # 标题
        if line.startswith('# '):
            html += f'<h1>{line[2:]}</h1>\n'
        elif line.startswith('## '):
            html += f'<h2>{line[3:]}</h2>\n'
        elif line.startswith('### '):
            html += f'<h3>{line[4:]}</h3>\n'
        
        # 引用
        elif line.startswith('>'):
            html += f'<blockquote>{line[1:].strip()}</blockquote>\n'
        
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            html += f'<li>{line[2:]}</li>\n'
            if not in_list:
                html += '<ul>\n'
                in_list = True
        
        # 分割线
        elif line == '---':
            html += '<div class="divider"></div>\n'
        
        # 表格（简单处理）
        elif '|' in line and '---' not in line:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            html += '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>\n'
        
        # 普通段落
        else:
            # 处理加粗
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            # 处理代码
            line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
            html += f'<p>{line}</p>\n'
    
    if in_list:
        html += '</ul>\n'
    
    html += '''
    </div>
</body>
</html>'''
    
    return html

def main():
    if len(sys.argv) < 3:
        print('用法: python 转手机版.py 输入.md 输出.html')
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown = f.read()
    
    html = markdown_to_html(markdown)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ 已转换: {output_file}')

if __name__ == '__main__':
    main()
