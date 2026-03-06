"""
Researcher Agent
"""

from typing import Dict


def handle(message: Dict) -> Dict:
    """处理 Researcher 任务"""
    content = message.get("content", "")
    
    print(f"[Researcher] 收到调研任务: {content}")
    print("[Researcher] 搜索信息中...")
    
    # 模拟调研
    response = {
        "agent": "researcher",
        "status": "completed",
        "message": f"[Researcher] 调研完成: {content}",
        "findings": [
            "来源1: xxx",
            "来源2: xxx",
            "来源3: xxx"
        ]
    }
    
    print(f"[Researcher] 找到 {len(response['findings'])} 条信息")
    return response
