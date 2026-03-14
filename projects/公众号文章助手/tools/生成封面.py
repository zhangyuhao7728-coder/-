#!/usr/bin/env python3
"""
公众号封面生成工具
用法：
  python tools/生成封面.py --title "文章标题"
  python tools/生成封面.py --title "标题" --template tech
  python tools/生成封面.py --title "标题" --output output/covers/cover.html
"""
import os
import sys
import argparse

# 封面模板
TEMPLATES = {
    'default': {
        'name': '默认风格',
        'bg': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        'title_color': '#ffffff',
        'accent_color': '#3498db',
    },
    'tech': {
        'name': '科技风',
        'bg': 'linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
        'title_color': '#00d4ff',
        'accent_color': '#00d4ff',
    },
    'warm': {
        'name': '温暖风',
        'bg': 'linear-gradient(180deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)',
        'title_color': '#ffffff',
        'accent_color': '#ff6b6b',
    },
    'dark': {
        'name': '暗黑风',
        'bg': 'linear-gradient(180deg, #232526 0%, #414345 100%)',
        'title_color': '#ffffff',
        'accent_color': '#f39c12',
    },
    'blue': {
        'name': '简洁蓝',
        'bg': 'linear-gradient(180deg, #1e3c72 0%, #2a5298 100%)',
        'title_color': '#ffffff',
        'accent_color': '#3498db',
    },
    'green': {
        'name': '清新绿',
        'bg': 'linear-gradient(180deg, #134e5e 0%, #71b280 100%)',
        'title_color': '#ffffff',
        'accent_color': '#71b280',
    },
}

def generate_cover(
    title: str,
    subtitle: str = '',
    tags: list = None,
    template: str = 'default',
    output: str = 'cover.html'
):
    """生成封面"""
    
    if template not in TEMPLATES:
        template = 'default'
    
    t = TEMPLATES[template]
    
    # 生成标签HTML
    tags_html = ''
    if tags:
        tags_html = '<div class="tags">'
        for tag in tags:
            tags_html += f'<span class="tag">{tag}</span>'
        tags_html += '</div>'
    
    # 分割长标题
    if '\n' in title:
        title_parts = title.split('\n')
        title_html = ''.join(f'<div>{p}</div>' for p in title_parts)
    else:
        title_html = f'<div>{title}</div>'
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>封面</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            width: 800px;
            height: 1200px;
            background: {t['bg']};
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        /* 装饰圆圈 */
        body::before {{
            content: '';
            position: absolute;
            top: -100px;
            right: -100px;
            width: 400px;
            height: 400px;
            background: rgba(255,255,255,0.05);
            border-radius: 50%;
        }}
        body::after {{
            content: '';
            position: absolute;
            bottom: -150px;
            left: -150px;
            width: 500px;
            height: 500px;
            background: rgba(255,255,255,0.03);
            border-radius: 50%;
        }}
        
        .logo {{
            position: absolute;
            top: 40px;
            left: 40px;
            font-size: 50px;
        }}
        
        .content {{
            z-index: 1;
            padding: 40px;
        }}
        
        .title {{
            font-size: 48px;
            font-weight: bold;
            color: {t['title_color']};
            line-height: 1.3;
            margin-bottom: 16px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            font-size: 24px;
            color: rgba(255,255,255,0.8);
            margin-bottom: 24px;
        }}
        
        .divider {{
            width: 100px;
            height: 3px;
            background: {t['accent_color']};
            margin: 20px auto;
            border-radius: 2px;
        }}
        
        .tags {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 24px;
        }}
        
        .tag {{
            background: rgba(255,255,255,0.15);
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 16px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .author {{
            position: absolute;
            bottom: 50px;
            font-size: 20px;
            color: rgba(255,255,255,0.6);
        }}
        
        .icon {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 200px;
            opacity: 0.1;
        }}
    </style>
</head>
<body>
    <div class="logo">🦞</div>
    <div class="content">
        <div class="title">{title_html}</div>
        <div class="subtitle">{subtitle}</div>
        <div class="divider"></div>
        {tags_html}
    </div>
    <div class="author">我是余豪 🚀</div>
</body>
</html>'''
    
    # 保存
    os.makedirs(os.path.dirname(output) if os.path.dirname(output) else '.', exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'✅ 封面已生成: {output}')
    return output

def list_templates():
    """列出可用模板"""
    print("\n📋 可用模板：")
    for key, t in TEMPLATES.items():
        print(f"  {key:10} - {t['name']}")
    print()

def main():
    parser = argparse.ArgumentParser(description='生成公众号封面')
    parser.add_argument('--title', '-t', required=True, help='封面标题（支持换行）')
    parser.add_argument('--subtitle', '-s', default='', help='副标题')
    parser.add_argument('--tags', nargs='+', default=['AI', '学习'], help='标签')
    parser.add_argument('--template', '-m', default='default', help='模板风格')
    parser.add_argument('--output', '-o', default='output/covers/cover.html', help='输出文件')
    parser.add_argument('--list', '-l', action='store_true', help='列出可用模板')
    
    args = parser.parse_args()
    
    if args.list:
        list_templates()
        return
    
    # 生成
    generate_cover(
        title=args.title,
        subtitle=args.subtitle,
        tags=args.tags,
        template=args.template,
        output=args.output
    )
    
    print(f"\n💡 提示：用浏览器打开 {args.output} 后截图")
    print(f"   建议分辨率：800x1200 或 900x1280")

if __name__ == '__main__':
    main()
