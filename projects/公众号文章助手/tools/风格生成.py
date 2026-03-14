#!/usr/bin/env python3
"""
风格模仿写作工具
用法：
  python tools/风格生成.py --style 余豪风格 --topic "AI安全"
  python tools/风格生成.py --style 教程类 --topic "Python入门"
"""
import os
import sys
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
STYLE_DB = os.path.join(PROJECT_DIR, 'style', 'style_database.json')

# 加载风格数据库
def load_style(name: str) -> dict:
    """加载指定风格"""
    if not os.path.exists(STYLE_DB):
        print("❌ 风格数据库不存在")
        return {}
    
    with open(STYLE_DB, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 跳过说明字段
    if name in db and not name.startswith('_'):
        return db[name]
    
    # 查找相似
    for key in db:
        if not key.startswith('_') and name in key:
            return db[key]
    
    return db.get('默认风格', {})

def build_prompt(style: dict, topic: str, article_type: str = None) -> str:
    """构建写作提示词"""
    
    tone = style.get('tone', '专业')
    sentence = style.get('sentence_length', '中等')
    use_emoji = style.get('emoji', True)
    structure = style.get('structure', [])
    opening = style.get('opening', '大家好')
    closing = style.get('closing', '有问题评论区见')
    
    # 构建结构提示
    structure_prompt = ""
    if structure:
        structure_prompt = "文章结构：\n"
        for i, s in enumerate(structure, 1):
            structure_prompt += f"{i}. {s}\n"
    
    # 构建风格提示
    style_prompt = f"""
写作风格要求：
- 语气：{tone}
- 句子长度：{sentence}
- 使用emoji：{"是" if use_emoji else "否"}
- 开场白：{opening}
- 结尾语：{closing}
"""
    
    # 构建完整prompt
    prompt = f"""你是一位公众号博主，擅长写AI相关的文章。

{structure_prompt}
{style_prompt}

请根据以下主题写一篇{article_type or '文章'}：

主题：{topic}

要求：
1. 语言生动有趣，接地气
2. 适当使用emoji增加趣味
3. 结构清晰，层次分明
4. 有互动环节，引导评论
5. 开头要吸引人，结尾要有号召力
6. 字数控制在1500-2500字

文章类型：{article_type or '经验分享类'}

请开始写作："""
    
    return prompt

def call_llm(prompt: str) -> str:
    """调用LLM生成文章"""
    print("🤖 正在调用AI生成文章...")
    print("⚠️  LLM调用功能待配置")
    print("\n生成的Prompt：")
    print("="*50)
    print(prompt[:500] + "...")
    print("="*50)
    
    # 这里可以集成实际的LLM调用
    # 暂时返回示例
    return f"""
# {prompt.split('主题：')[1].split('\\n')[0]}

> 这是一个AI生成的文章示例
> 实际使用需要配置LLM

---

## 开场

大家好！今天想和大家聊聊...

## 内容

（AI生成的内容会在这里）

---

## 结尾

{closing}

---
"""
    
    # 实际LLM调用示例（需要配置）：
    # from ai.llm_router import chat
    # return await chat(prompt)

def format_article(content: str, topic: str, style: dict) -> str:
    """格式化文章"""
    
    opening = style.get('opening', '大家好')
    closing = style.get('closing', '有问题评论区见')
    
    # 添加标题
    title = f"# {topic}\n"
    
    # 添加开场
    intro = f"\n> 主题：{topic}\n\n"
    
    # 添加结尾互动
    ending = f"\n\n---\n\n{closing}\n"
    
    return title + intro + content + ending

def generate_article(style_name: str, topic: str, output: str = None, article_type: str = None):
    """生成文章"""
    
    print(f"\n{'='*50}")
    print("🎨 风格模仿写作")
    print(f"{'='*50}\n")
    
    # 加载风格
    print(f"📂 加载风格: {style_name}")
    style = load_style(style_name)
    
    if not style:
        print(f"❌ 未找到风格: {style_name}")
        # 列出可用风格
        if os.path.exists(STYLE_DB):
            with open(STYLE_DB, 'r', encoding='utf-8') as f:
                db = json.load(f)
            print("\n可用风格：")
            for key in db:
                if not key.startswith('_'):
                    print(f"  - {key}")
        return
    
    print(f"✅ 风格特点：{style.get('tone', '未知')} | {style.get('sentence_length', '未知')}句 | Emoji: {'是' if style.get('emoji') else '否'}")
    
    # 构建prompt
    print(f"\n📝 主题: {topic}")
    prompt = build_prompt(style, topic, article_type)
    
    # 生成内容
    content = call_llm(prompt)
    
    # 格式化
    formatted = format_article(content, topic, style)
    
    # 输出
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(formatted)
        print(f"\n✅ 已保存到: {output}")
    else:
        print("\n" + "="*50)
        print("📄 生成的文章：")
        print("="*50)
        print(formatted)
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description='风格模仿写作')
    parser.add_argument('--style', '-s', default='余豪风格', help='风格名称')
    parser.add_argument('--topic', '-t', required=True, help='文章主题')
    parser.add_argument('--type', '-y', help='文章类型')
    parser.add_argument('--output', '-o', help='输出文件')
    
    args = parser.parse_args()
    
    generate_article(args.style, args.topic, args.output, args.type)

if __name__ == '__main__':
    main()
