"""LLM Router"""
def route_llm(task):
    t = task.get("estimated_tokens", 0)
    return "qwen2.5:7b" if t < 1500 else "MiniMax-M2.5"
