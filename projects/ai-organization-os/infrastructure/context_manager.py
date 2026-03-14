"""
Context Manager - 上下文管理器
限制最大 2000 tokens
"""

MAX_CONTEXT_TOKENS = 2000

def build_context(system_prompt, task_summary, current_step, last_result):
    """
    构建上下文
    绝对不包含：
    - 完整历史
    - 工具日志
    - debug日志
    - task_state
    """
    context = {
        "system": system_prompt,
        "task_summary": task_summary,
        "current_step": current_step,
        "last_result": last_result
    }
    return context
