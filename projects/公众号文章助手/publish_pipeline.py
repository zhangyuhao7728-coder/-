#!/usr/bin/env python3
"""
公众号文章发布流水线
终极自动化！一键生成完整公众号文章

流程：
  输入主题
  ↓
  抓取参考文章（可选）
  ↓
  分析风格（可选）
  ↓
  生成新文章
  ↓
  优化标题
  ↓
  公众号排版
  ↓
  生成封面
  ↓
  输出发布版本

用法：
  python publish_pipeline.py --topic "AI学习路线"
  python publish_pipeline.py --topic "AI安全" --style 余豪风格
"""
import os
import sys
import argparse
import json
from datetime import datetime

# 添加路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

# 导入工具
from tools.风格生成 import generate_article as generate
from tools.文章优化 import optimize_title
from formatter.markdown_to_wechat import markdown_to_wechat, wrap_html

def run_pipeline(
    topic: str,
    style: str = '余豪风格',
    article_type: str = None,
    url: str = None,
    output_dir: str = None
):
    """运行完整流水线"""
    
    print(f"\n{'='*60}")
    print("🚀 公众号文章发布流水线")
    print(f"{'='*60}")
    print(f"📌 主题: {topic}")
    print(f"🎨 风格: {style}")
    print(f"{'='*60}\n")
    
    # 步骤1: 生成文章
    print("📝 步骤1/5: 生成文章...")
    content = generate(style, topic, article_type=article_type)
    print("   ✅ 文章生成完成")
    
    # 步骤2: 优化标题
    print("\n✨ 步骤2/5: 优化标题...")
    title_result = optimize_title(topic)
    # 使用原主题作为标题（可以改进为选择优化后的标题）
    title = topic
    print(f"   📌 标题: {title}")
    print(f"   📊 评分: {title_result['score']}/100")
    print("   ✅ 标题优化完成")
    
    # 步骤3: 公众号排版
    print("\n🎨 步骤3/5: 公众号排版...")
    wechat_html = markdown_to_wechat(content)
    print("   ✅ 排版完成")
    
    # 步骤4: 生成封面
    print("\n🖼️ 步骤4/5: 生成封面...")
    # 调用生成封面
    os.system(f'python3 {SCRIPT_DIR}/tools/生成封面.py '
              f'--title "{title}" '
              f'--template default '
              f'--output "{output_dir or "output/covers"}/cover.html"')
    print("   ✅ 封面生成完成")
    
    # 步骤5: 保存文件
    print("\n💾 步骤5/5: 保存文件...")
    
    if not output_dir:
        output_dir = f"output/articles/{datetime.now().strftime('%Y-%m-%d')}"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存Markdown
    md_file = f"{output_dir}/{topic}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   📄 Markdown: {md_file}")
    
    # 保存公众号HTML
    html_file = f"{output_dir}/{topic}_公众号.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(wrap_html(wechat_html, title))
    print(f"   🌐 公众号HTML: {html_file}")
    
    # 保存手机版
    mobile_file = f"{output_dir}/{topic}_手机版.html"
    # 使用之前生成的封面作为封面
    with open(mobile_file, 'w', encoding='utf-8') as f:
        f.write(wrap_html(wechat_html, title))
    print(f"   📱 手机版: {mobile_file}")
    
    # 完成
    print(f"\n{'='*60}")
    print("✅ 流水线完成！")
    print(f"{'='*60}")
    print(f"\n📁 输出目录: {output_dir}")
    print(f"\n💡 下一步:")
    print(f"   1. 打开 {md_file} 手动修改内容")
    print(f"   2. 用浏览器打开封面截图")
    print(f"   3. 复制公众号HTML到公众号编辑器")
    
    return {
        'topic': topic,
        'title': title,
        'output_dir': output_dir,
        'files': {
            'markdown': md_file,
            'wechat': html_file,
            'mobile': mobile_file,
        }
    }

def interactive_mode():
    """交互模式"""
    print("\n" + "="*50)
    print("🚀 公众号文章发布流水线 - 交互模式")
    print("="*50 + "\n")
    
    # 1. 输入主题
    topic = input("📝 请输入文章主题: ").strip()
    if not topic:
        print("❌ 主题不能为空")
        return
    
    # 2. 选择风格
    print("\n🎨 可选风格:")
    print("   1. 余豪风格")
    print("   2. 教程类")
    print("   3. 经验类")
    print("   4. 踩坑记录")
    style_choice = input("   请选择 (1-4, 默认1): ").strip() or "1"
    
    styles = {'1': '余豪风格', '2': '教程类', '3': '经验类', '4': '踩坑记录'}
    style = styles.get(style_choice, '余豪风格')
    
    # 3. 选择文章类型
    print("\n📄 可选类型:")
    print("   1. 经验分享")
    print("   2. 技术教程")
    print("   3. 踩坑记录")
    type_choice = input("   请选择 (1-3, 默认1): ").strip() or "1"
    
    types = {'1': '经验分享', '2': '技术教程', '3': '踩坑记录'}
    article_type = types.get(type_choice, '经验分享')
    
    # 4. 是否需要参考文章
    use_reference = input("\n📥 是否抓取参考文章? (y/N): ").strip().lower() == 'y'
    url = None
    if use_reference:
        url = input("   请输入参考文章链接: ").strip()
    
    # 5. 运行流水线
    run_pipeline(topic, style, article_type, url)

def main():
    parser = argparse.ArgumentParser(description='公众号文章发布流水线')
    parser.add_argument('--topic', '-t', help='文章主题')
    parser.add_argument('--style', '-s', default='余豪风格', help='风格')
    parser.add_argument('--type', '-y', help='文章类型')
    parser.add_argument('--url', '-u', help='参考文章链接')
    parser.add_argument('--output', '-o', help='输出目录')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    
    args = parser.parse_args()
    
    if args.interactive or (not args.topic):
        interactive_mode()
    else:
        run_pipeline(
            topic=args.topic,
            style=args.style,
            article_type=args.type,
            url=args.url,
            output_dir=args.output
        )

if __name__ == '__main__':
    main()
