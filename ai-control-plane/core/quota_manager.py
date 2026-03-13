#!/usr/bin/env python3
"""
Quota Manager - 配额管理器
功能：
1. 配额限制
2. 使用量追踪
3. 超过自动跳过
"""
from typing import Dict


# 配额配置 (tokens/天)
MODEL_QUOTA = {
    "minimax/MiniMax-M2.5": 100000,  # 10万tokens
    "volcengine/doubao-seed-code": 50000,  # 5万tokens (40%配额)
}

# 当前使用量
MODEL_USAGE = {}


def update_usage(model: str, tokens: int) -> bool:
    """
    更新使用量
    
    Args:
        model: 模型名称
        tokens: 消耗的tokens
    
    Returns:
        True: 未超配额
        False: 超过配额
    """
    # 初始化
    if model not in MODEL_USAGE:
        MODEL_USAGE[model] = 0
    
    # 累加
    MODEL_USAGE[model] += tokens
    
    # 检查配额
    quota = MODEL_QUOTA.get(model, 999999)
    
    if MODEL_USAGE[model] > quota:
        print(f"  ⚠️ {model} 超过配额: {MODEL_USAGE[model]}/{quota}")
        return False
    
    return True


def get_usage(model: str) -> int:
    """获取当前使用量"""
    return MODEL_USAGE.get(model, 0)


def get_quota(model: str) -> int:
    """获取配额"""
    return MODEL_QUOTA.get(model, 999999)


def get_remaining(model: str) -> int:
    """获取剩余配额"""
    return get_quota(model) - get_usage(model)


def is_available(model: str) -> bool:
    """检查是否可用"""
    return get_remaining(model) > 0


def reset_usage(model: str = None):
    """重置使用量"""
    if model:
        MODEL_USAGE[model] = 0
    else:
        MODEL_USAGE.clear()


def get_status() -> Dict:
    """获取所有模型状态"""
    status = {}
    
    for model in MODEL_QUOTA:
        status[model] = {
            "quota": get_quota(model),
            "usage": get_usage(model),
            "remaining": get_remaining(model),
            "available": is_available(model),
        }
    
    return status


def print_status():
    """打印状态"""
    print("=== Quota Status ===\n")
    
    for model, info in get_status().items():
        icon = "✅" if info["available"] else "❌"
        pct = info["usage"] / info["quota"] * 100
        
        print(f"{icon} {model}")
        print(f"   使用: {info['usage']:,} / {info['quota']:,} ({pct:.1f}%)")
        print(f"   剩余: {info['remaining']:,}")
        print()


# ========== 带配额检查的 Router ==========

def should_use_model(model: str) -> bool:
    """
    检查模型是否应该使用
    
    如果超过配额，返回 False (Router 会自动跳过)
    """
    # 云模型需要检查配额
    if "/" in model:
        provider = model.split("/")[0]
        if provider in ["minimax", "volcengine"]:
            return is_available(model)
    
    # 本地模型无限制
    return True


# 测试
if __name__ == "__main__":
    print("=== Quota Manager 测试 ===\n")
    
    # 更新使用量
    print("1. 模拟使用:")
    update_usage("minimax/MiniMax-M2.5", 50000)
    update_usage("volcengine/doubao-seed-code", 20000)
    
    # 状态
    print_status()
    
    # 检查
    print("2. 可用性检查:")
    print(f"   minimax: {should_use_model('minimax/MiniMax-M2.5')}")
    print(f"   qwen2.5: {should_use_model('ollama/qwen2.5:7b')}")
