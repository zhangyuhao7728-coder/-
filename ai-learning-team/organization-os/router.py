"""
Model Router - 模型选择
支持：自动根据 Context 切换模型
"""

import json

# 加载配置
with open("openclaw.json") as f:
    config = json.load(f)


def route(agent: dict, session: dict = None) -> dict:
    """
    根据 agent 配置和 session 状态选择模型
    
    Args:
        agent: agent 配置字典
        session: session 状态字典（可选）
        
    Returns:
        模型配置 dict
    """
    router = config["model_router"]
    
    # 如果有 session，检查 context
    if session:
        used = session.get("used_tokens", 0)
        
        # Context > 120k → 切换本地模型（减轻云端压力）
        if used > 120000:
            print(f"🧠 Context high ({used}), switching to local model")
            return router.get("local", router["cloud"])
    
    # 根据 model 类型选择
    if agent.get("model") == "cloud":
        return router["cloud"]
    
    if agent.get("model") == "coder":
        return router["coder"]
    
    # 默认返回 local
    return router["local"]


# ===== 测试 =====

if __name__ == "__main__":
    print("="*50)
    print("Router Test (with Context switching)")
    print("="*50)
    
    # 测试场景
    agents = [
        {"name": "ceo", "model": "cloud"},
        {"name": "engineer", "model": "coder"},
    ]
    
    # 低 context
    session_low = {"used_tokens": 50000, "max_context": 200000}
    
    # 高 context
    session_high = {"used_tokens": 150000, "max_context": 200000}
    
    print("\n📊 Low Context (50k):")
    for agent in agents:
        model = route(agent, session_low)
        print(f"  {agent['name']} → {model['model']}")
    
    print("\n📊 High Context (150k):")
    for agent in agents:
        model = route(agent, session_high)
        print(f"  {agent['name']} → {model['model']}")
