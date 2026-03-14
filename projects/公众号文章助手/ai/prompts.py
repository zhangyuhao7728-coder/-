#!/usr/bin/env python3
"""
AI提示词模板
"""

# 文章生成提示词
ARTICLE_PROMPT = """
你是一位公众号博主，擅长写AI相关的文章。
请根据以下主题生成文章：

主题：{topic}
类型：{type}
风格：{style}

要求：
- 语言生动有趣
- 适当用emoji
- 结构清晰
- 有互动环节
"""

# 风格润色提示词
POLISH_PROMPT = """
请润色以下文章，使其更加生动有趣：

{article}

要求：
- 保持原意
- 优化表达
- 适当添加emoji
- 增加互动
"""

# 标题生成提示词
TITLE_PROMPT = """
请为以下文章生成3个吸引人的标题：

内容：{content}

要求：
- 简洁明了
- 体现价值
- 吸引点击
"""

def get_prompt(prompt_type: str, **kwargs) -> str:
    """获取提示词"""
    prompts = {
        'article': ARTICLE_PROMPT,
        'polish': POLISH_PROMPT,
        'title': TITLE_PROMPT,
    }
    template = prompts.get(prompt_type, '')
    return template.format(**kwargs)
