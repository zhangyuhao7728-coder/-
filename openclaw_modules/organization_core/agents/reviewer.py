"""
Reviewer Agent
"""

from typing import Dict


def handle(message: Dict) -> Dict:
    """处理 Reviewer 任务"""
    content = message.get("content", "")
    
    print(f"[Reviewer] 收到审查任务: {content}")
    print("[Reviewer] 审查代码中...")
    
    # 模拟审查
    response = {
        "agent": "reviewer",
        "status": "completed",
        "message": f"[Reviewer] 审查完成: {content}",
        "review": {
            "code_quality": "良好",
            "security": "通过",
            "performance": "可优化",
            "suggestions": [
                "建议1: xxx",
                "建议2: xxx"
            ]
        }
    }
    
    print(f"[Reviewer] 审查建议: {len(response['review']['suggestions'])} 条")
    return response
