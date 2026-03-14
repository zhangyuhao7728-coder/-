#!/usr/bin/env python3
"""
公众号Markdown排版工具
功能：Markdown → 公众号HTML格式
用法：
  python formatter/markdown_to_wechat.py input.md output.html
  python formatter/markdown_to_wechat.py input.md --preview
"""
import os
import sys
import re
import argparse

# 公众号样式配置
WECHAT_STYLE = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        font-size: 16px;
        line-height: 1.8;
        color: #333;
        padding: 0 15px;
    }
    h1 {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        color: #1a1a1a;
    }
    h2 {
        font-size: 20px;
        font-weight: bold;
        margin: 24px 0 12px;
        color: #2c3e50;
        border-left: 4px solid #3498db;
        padding-left: 12px;
    }
    h3 {
        font-size: 18px;
        font-weight: bold;
        margin: 16px 0 8px;
        color: #34495e;
    }
    p {
        margin: 12px 0;
        text-align: justify;
    }
    strong {
        color: #e74c3c;
    }
    code {
        background: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: "SF Mono", Monaco, Consolas, monospace;
        font-size: 14px;
        color: #e74c3c;
    }
    pre {
        background: #2d2d2d;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 16px 0;
    }
    pre code {
        background: none;
        padding: 0;
        color: #f8f8f2;
    }
    ul, ol {
        margin: 12px 0;
        padding-left: 24px;
    }
    li {
        margin: 8px 0;
    }
    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 16px;
        margin: 16px 0;
        color: #666;
        background: #f8f9fa;
        padding: 12px 16px;
    }
    a {
        color: #3498db;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin: 12px 0;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 14px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }
    th {
        background: #3498db;
        color: white;
    }
    hr {
        border: none;
        border-top: 1px solid #eee;
        margin: 24px 0;
    }
    .emoji {
        font-size: 18px;
    }
    .warning {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px 16px;
        margin: 16px 0;
    }
    .success {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px 16px;
        margin: 16px 0;
    }
    .danger {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 12px 16px;
        margin: 16px 0;
    }
</style>
"""

def markdown_to_wechat(md_text: str) -> str:
    """Markdown转公众号HTML"""
    html = md_text
    
    # 转义HTML特殊字符（但保留markdown符号）
    html = html.replace('&', '&amp;')
    
    # 代码块（先处理，避免被其他规则影响）
    def replace_code_block(m):
        lang = m.group(1) or ''
        code = m.group(2)
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    
    html = re.sub(r'```(\w*)\n([\s\S]*?)```', replace_code_block, html)
    
    # 行内代码
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # 标题
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 加粗
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # 删除线
    html = re.sub(r'~~(.+?)~~', r'<del>\1</del>', html)
    
    # 链接
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # 图片
    html = re.sub(r'!\[(.*?)\]\((.+?)\)', r'<img src="\2" alt="\1">', html)
    
    # 分割线
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)
    
    # 引用块
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # 无序列表
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\* (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 有序列表
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # 表格（简单处理）
    def replace_table(m):
        lines = m.group(0).split('\n')
        html = '<table>'
        for i, line in enumerate(lines):
            if '---' in line:
                continue
            cells = [c.strip() for c in line.split('|')[1:-1] if c.strip()]
            if not cells:
                continue
            tag = 'th' if i == 0 else 'td'
            html += '<tr>' + ''.join(f'<{tag}>{c}</{tag}>' for c in cells) + '</tr>'
        html += '</table>'
        return html
    
    html = re.sub(r'(\|.+\|.+\n)+', replace_table, html)
    
    # 处理连续的空行
    html = re.sub(r'\n{3,}', '\n\n', html)
    
    # 包裹段落
    lines = html.split('\n')
    result_lines = []
    in_list = False
    in_table = False
    in_blockquote = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            if in_table:
                result_lines.append('</table>')
                in_table = False
            if in_blockquote:
                in_blockquote = False
            continue
        
        # 检查列表开始
        if line.startswith('<li>'):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(line)
        
        # 检查表格开始
        elif line.startswith('<table>'):
            in_table = True
            result_lines.append(line)
        
        # 检查引用开始
        elif line.startswith('<blockquote>'):
            in_blockquote = True
            result_lines.append(line)
        
        # 标题和代码块单独一行
        elif line.startswith('<h') or line.startswith('<pre>') or line.startswith('<hr'):
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
        
        # 普通段落
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            if in_table:
                result_lines.append('</table>')
                in_table = False
            result_lines.append(f'<p>{line}</p>')
    
    # 关闭未关闭的标签
    if in_list:
        result_lines.append('</ul>')
    if in_table:
        result_lines.append('</table>')
    
    html = '\n'.join(result_lines)
    
    # 清理空段落
    html = re.sub(r'<p></p>', '', html)
    
    return html

def wrap_html(content: str, title: str = '') -> str:
    """包装成完整HTML"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {WECHAT_STYLE}
</head>
<body>
{content}
</body>
</html>"""

def main():
    parser = argparse.ArgumentParser(description='公众号Markdown排版工具')
    parser.add_argument('input', help='输入Markdown文件')
    parser.add_argument('output', nargs='?', help='输出HTML文件')
    parser.add_argument('--preview', '-p', action='store_true', help='预览模式')
    parser.add_argument('--title', '-t', default='文章', help='页面标题')
    
    args = parser.parse_args()
    
    # 读取输入
    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)
    
    with open(args.input, 'r', encoding='utf-8') as f:
        md = f.read()
    
    # 转换
    html = markdown_to_wechat(md)
    full_html = wrap_html(html, args.title)
    
    # 输出
    if args.preview:
        # 保存临时文件并打开
        temp_file = '/tmp/wechat_preview.html'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        os.system(f'open {temp_file}')
        print(f"✅ 预览已打开: {temp_file}")
    
    elif args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✅ 已保存: {args.output}")
    
    else:
        print(full_html)

if __name__ == '__main__':
    main()
