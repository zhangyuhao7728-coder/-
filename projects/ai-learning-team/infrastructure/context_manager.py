"""Context Manager"""
MAX_TOKENS = 2000

def build_context(system, task_summary, step, result):
    return {"system": system, "task_summary": task_summary}
