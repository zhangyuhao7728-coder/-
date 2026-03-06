"""
Planner Agent
"""

from typing import Dict


def handle(message: Dict) -> Dict:
    """处理 Planner 任务"""
    content = message.get("content", "")
    
    print(f"[Planner] 收到任务: {content}")
    print("[Planner] 制定计划中...")
    
    # 生成计划
    response = {
        "agent": "planner",
        "status": "completed",
        "message": f"[Planner] 计划已制定: {content}",
        "plan": [
            "1. 分析需求",
            "2. 拆解任务",
            "3. 分配优先级",
            "4. 设置里程碑"
        ]
    }
    
    print(f"[Planner] 计划: {response['plan']}")
    return response
