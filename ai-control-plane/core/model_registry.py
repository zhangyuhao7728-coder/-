#!/usr/bin/env python3
"""
Model Registry - 优化版 (免费 + 云模型)
优先使用免费模型，降低成本
"""
from typing import Dict, List


# 优化后的模型注册表 (免费优先)
MODEL_REGISTRY = {
    # 主模型 - 本地优先
    "main": [
        {"name": "qwen3.5:9b", "provider": "ollama", "cost": "free"},
        {"name": "deepseek-coder:6.7b", "provider": "ollama", "cost": "free"},
        {"name": "minimax/MiniMax-M2.5", "provider": "minimax", "cost": "paid"},
    ],
    
    # 通用任务 - 本地免费
    "general": [
        {"name": "qwen2.5:latest", "provider": "ollama", "cost": "free"},
        {"name": "qwen3.5:9b", "provider": "ollama", "cost": "free"},
        {"name": "volcengine/doubao-seed-code", "provider": "doubao", "cost": "quota"},
        {"name": "minimax/MiniMax-M2.5", "provider": "minimax", "cost": "paid"},
    ],
    
    # 代码任务 - 本地免费
    "code": [
        {"name": "deepseek-coder:6.7b", "provider": "ollama", "cost": "free"},
        {"name": "qwen2.5:7b", "provider": "ollama", "cost": "free"},
        {"name": "qwen3.5:9b", "provider": "ollama", "cost": "free"},
        {"name": "volcengine/doubao-seed-code", "provider": "doubao", "cost": "quota"},
    ],
    
    # 分析任务 - 本地免费
    "analysis": [
        {"name": "qwen3.5:9b", "provider": "ollama", "cost": "free"},
        {"name": "qwen2.5:14b", "provider": "ollama", "cost": "free"},
        {"name": "deepseek-coder:6.7b", "provider": "ollama", "cost": "free"},
        {"name": "minimax/MiniMax-M2.5", "provider": "minimax", "cost": "paid"},
    ],
    
    # 创意任务 - 云模型
    "creative": [
        {"name": "minimax/MiniMax-M2.5", "provider": "minimax", "cost": "paid"},
        {"name": "volcengine/doubao-seed-code", "provider": "doubao", "cost": "quota"},
        {"name": "qwen2.5:14b", "provider": "ollama", "cost": "free"},
    ],
    
    # 快速任务 - 本地最快
    "fast": [
        {"name": "qwen2.5:latest", "provider": "ollama", "cost": "free"},
        {"name": "deepseek-coder:6.7b", "provider": "ollama", "cost": "free"},
        {"name": "qwen2.5:7b", "provider": "ollama", "cost": "free"},
    ],
}


class ModelRegistry:
    """模型注册表管理器"""
    
    def __init__(self):
        self.registry = MODEL_REGISTRY
    
    def get_models(self, task_type: str) -> List[Dict]:
        return self.registry.get(task_type, self.registry["general"])
    
    def get_primary_model(self, task_type: str) -> str:
        models = self.get_models(task_type)
        return models[0]["name"] if models else "qwen2.5:latest"
    
    def get_fallback_models(self, task_type: str) -> List[str]:
        models = self.get_models(task_type)
        return [m["name"] for m in models[1:]] if len(models) > 1 else []
    
    def print_registry(self):
        print("=== Model Registry (免费优先) ===\n")
        for task, models in self.registry.items():
            print(f"{task}:")
            for m in models:
                cost_icon = "🆓" if m["cost"] == "free" else "☁️" if m["cost"] == "quota" else "💰"
                print(f"  {cost_icon} {m['name']} ({m['provider']})")
            print()


_registry = None

def get_registry() -> ModelRegistry:
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry


if __name__ == "__main__":
    reg = get_registry()
    reg.print_registry()
