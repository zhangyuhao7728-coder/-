#!/usr/bin/env python3
"""
排版系统 V2
专业公众号排版
"""
import os
import re

class WechatFormatter:
    """微信编辑器格式化器"""
    
    # 样式配置
    STYLES = {
        'default': {
            'font': '16px',
            'color': '#333333',
            'bg_color': '#ffffff',
        },
        'dark': {
            'font': '16px',
            'color': '#e0e0e0',
            'bg_color': '#1a1a1a',
        }
    }
    
    def __init__(self, style: str = 'default'):
        self.style = self.STYLES.get(style, self.STYLES['default'])
    
    def format_title(self, text: str, level: int = 1) -> str:
        """格式化标题"""
        sizes = {
            1: '24px',
            2: '20px',
            3: '18px',
        }
        size = sizes.get(level, '18px')
        
        return f'<h{level} style="font-size:{size};font-weight:bold;margin:20px 0 10px;color:#1a1a1a">{text}</h{level}>'
    
    def format_paragraph(self, text: str) -> str:
        """格式化段落"""
        return f'<p style="margin:12px 0;line-height:1.8">{text}</p>'
    
    def format_quote(self, text: str) -> str:
        """格式化引用"""
        return f'<blockquote style="border-left:4px solid #3498db;padding:12px 16px;margin:16px 0;background:#f8f9fa;color:#666">{text}</blockquote>'
    
    def format_code(self, code: str, language: str = '') -> str:
        """格式化代码"""
        return f'<pre style="background:#2d2d2d;color:#f8f8f2;padding:15px;border-radius:8px;margin:16px 0;overflow-x:auto"><code>{code}</code></pre>'
    
    def format_list(self, items: list, ordered: bool = False) -> str:
        """格式化列表"""
        tag = 'ol' if ordered else 'ul'
        items_html = ''.join(f'<li style="margin:8px 0">{item}</li>' for item in items)
        return f'<{tag} style="margin:12px 0;padding-left:24px">{items_html}</{tag}>'
    
    def format_table(self, rows: list) -> str:
        """格式化表格"""
        if not rows:
            return ''
        
        html = '<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px">'
        
        for i, row in enumerate(rows):
            tag = 'th' if i == 0 else 'td'
            cells = ''.join(f'<{tag} style="border:1px solid #ddd;padding:10px;text-align:left">{cell}</{tag}>' for cell in row)
            html += f'<tr>{cells}</tr>'
        
        html += '</table>'
        return html
    
    def format_image(self, src: str, alt: str = '', width: str = '100%') -> str:
        """格式化图片"""
        return f'<img src="{src}" alt="{alt}" style="max-width:{width};border-radius:8px;margin:12px 0">'
    
    def format_divider(self) -> str:
        """格式化分割线"""
        return '<hr style="border:none;border-top:1px solid #eee;margin:24px 0">'
    
    def format_link(self, text: str, url: str) -> str:
        """格式化链接"""
        return f'<a href="{url}" style="color:#3498db;text-decoration:none">{text}</a>'
    
    def format_bold(self, text: str) -> str:
        """格式化加粗"""
        return f'<strong style="color:#e74c3c">{text}</strong>'
    
    def format_emoji(self, emoji: str) -> str:
        """格式化emoji"""
        return f'<span style="font-size:18px">{emoji}</span>'
    
    def wrap_html(self, content: str, title: str = '') -> str:
        """包装HTML"""
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
            font-size:16px;
            line-height:1.8;
            color:{self.style['color']};
            background:{self.style['bg_color']};
            padding:15px;
            max-width:700px;
            margin:0 auto;
        }}
        h1,h2,h3 {{color:#1a1a1a;margin:20px 0 10px}}
        h1 {{font-size:24px}}
        h2 {{font-size:20px}}
        h3 {{font-size:18px}}
        p {{margin:12px 0}}
        a {{color:#3498db}}
        pre {{background:#2d2d2d;color:#f8f8f2;padding:15px;border-radius:8px;overflow-x:auto}}
        blockquote {{border-left:4px solid #3498db;padding:12px;margin:16px 0;background:#f8f9fa}}
        img {{max-width:100%;border-radius:8px}}
        table {{width:100%;border-collapse:collapse}}
        th,td {{border:1px solid #ddd;padding:10px;text-align:left}}
    </style>
</head>
<body>
{content}
</body>
</html>'''
        return html
    
    def from_markdown(self, md: str) -> str:
        """从Markdown转换"""
        html = []
        lines = md.split('\n')
        in_code = False
        code_lines = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if in_code:
                    code_lines.append('')
                else:
                    html.append('<p></p>')
                continue
            
            # 代码块
            if line.startswith('```'):
                if in_code:
                    html.append(self.format_code('\n'.join(code_lines)))
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                    code_lines = []
                continue
            
            if in_code:
                code_lines.append(line)
                continue
            
            # 标题
            if line.startswith('# '):
                html.append(self.format_title(line[2:], 1))
            elif line.startswith('## '):
                html.append(self.format_title(line[3:], 2))
            elif line.startswith('### '):
                html.append(self.format_title(line[4:], 3))
            
            # 分割线
            elif line == '---':
                html.append(self.format_divider())
            
            # 引用
            elif line.startswith('> '):
                html.append(self.format_quote(line[2:]))
            
            # 无序列表
            elif line.startswith('- ') or line.startswith('* '):
                html.append(f'<li style="margin:8px 0">{line[2:]}</li>')
            
            # 加粗
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            
            # 行内代码
            line = re.sub(r'`(.+?)`', r'<code style="background:#f4f4f4;padding:2px 6px;border-radius:3px">\1</code>', line)
            
            # 链接
            line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:#3498db">\1</a>', line)
            
            # 段落
            html.append(self.format_paragraph(line))
        
        # 处理列表
        final_html = []
        in_list = False
        list_items = []
        
        for line in html:
            if line.startswith('<li'):
                if not in_list:
                    in_list = True
                list_items.append(line)
            else:
                if in_list:
                    final_html.append(f'<ul style="margin:12px 0;padding-left:24px">{"".join(list_items)}</ul>')
                    list_items = []
                    in_list = False
                final_html.append(line)
        
        if in_list:
            final_html.append(f'<ul style="margin:12px 0;padding-left:24px">{"".join(list_items)}</ul>')
        
        return '\n'.join(final_html)

def format_wechat(md_file: str, output_file: str = None) -> str:
    """格式化微信文章"""
    with open(md_file, 'r', encoding='utf-8') as f:
        md = f.read()
    
    formatter = WechatFormatter()
    content = formatter.from_markdown(md)
    
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', md, re.MULTILINE)
    title = title_match.group(1) if title_match else '文章'
    
    html = formatter.wrap_html(content, title)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    return html

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        output = sys.argv[2] if len(sys.argv) > 2 else None
        result = format_wechat(sys.argv[1], output)
        
        if output:
            print(f"✅ 已保存: {output}")
        else:
            print(result)
