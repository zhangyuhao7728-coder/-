#!/usr/bin/env python3
"""
🧠 模型路由器
根据任务类型自动选择合适的AI模型
"""

# 模型配置
MODELS = {
    # 本地模型 (免费、快速)
    "qwen3.5": {
        "name": "qwen3.5:9b",
        "type": "local",
        "provider": "ollama",
        "url": "http://localhost:11434",
        "use_for": ["analysis", "review", "complex"]
    },
    "qwen2.5": {
        "name": "qwen2.5:latest",
        "type": "local", 
        "provider": "ollama",
        "url": "http://localhost:11434",
        "use_for": ["simple", "quick", "translate"]
    },
    "deepseek-coder": {
        "name": "deepseek-coder:6.7b",
        "type": "local",
        "provider": "ollama",
        "url": "http://localhost:11434",
        "use_for": ["code", "debug"]
    },
    
    # 云端模型 (高质量)
    "minimax_m25": {
        "name": "MiniMax-M2.5",
        "type": "cloud",
        "provider": "minimax",
        "url": "https://api.minimax.io/anthropic",
        "use_for": ["high_quality", "reasoning"]
    }
}

# 路由规则
ROUTING_RULES = {
    # 代码相关 → deepseek-coder
    "code": "deepseek-coder",
    "debug": "deepseek-coder",
    "debugger": "deepseek-coder",
    
    # 分析/审查 → qwen3.5
    "analysis": "qwen3.5",
    "review": "qwen3.5",
    "reviewer": "qwen3.5",
    
    # 简单任务 → qwen2.5
    "simple": "qwen2.5",
    "quick": "qwen2.5",
    "translate": "qwen2.5",
    
    # 高质量需求 → 云端
    "high_quality": "minimax_m25",
    "reasoning": "minimax_m25",
    
    # 默认
    "default": "qwen3.5"
}

def route_model(task, prompt):
    """根据任务类型路由到合适的模型"""
    
    # 查找匹配的模型
    model_key = ROUTING_RULES.get(task, ROUTING_RULES["default"])
    model_config = MODELS[model_key]
    
    print(f"🧠 路由: {task} → {model_config['name']}")
    
    # 调用模型
    return call_model(model_key, prompt, model_config)

def call_model(model_key, prompt, config):
    """调用模型"""
    # 这里应该调用实际的API
    # 暂时返回模拟结果
    return {
        "model": config["name"],
        "result": f"[{config['name']}] {prompt[:50]}...",
        "type": config["type"]
    }

def get_model_info(task=None):
    """获取模型信息"""
    if task:
        model_key = ROUTING_RULES.get(task, "default")
        return MODELS[model_key]
    return MODELS

# 测试
if __name__ == "__main__":
    print("=== 模型路由器测试 ===\n")
    
    tasks = ["code", "analysis", "simple", "review", "high_quality"]
    
    for task in tasks:
        result = route_model(task, f"测试{task}任务")
        print(f"任务: {task} → 模型: {result['model']}\n")
