"""
Engineer Agent
根据任务自动调用合适的模型
"""

from typing import Dict, Any


def handle(message: Dict) -> Dict:
    """
    处理 Engineer 任务
    
    自动使用 Model Router 选择的模型
    """
    content = message.get("content", "")
    task_id = message.get("task_id")
    model = message.get("model", "qwen2.5:14b")  # 从 metadata 获取模型
    
    print(f"[Engineer] 收到开发任务: {content}")
    print(f"[Engineer] 使用模型: {model}")
    print("[Engineer] 编写代码中...")
    
    # 模拟代码生成
    code_example = f"""
# 示例代码 (模型: {model})
def solution():
    # Your implementation here
    pass
"""
    
    response = {
        "agent": "engineer",
        "status": "completed",
        "message": f"[Engineer] 代码已编写: {content}",
        "model_used": model,
        "code": code_example
    }
    
    print(f"[Engineer] 代码编写完成, 使用模型: {model}")
    return response
