#!/usr/bin/env python3
"""
Model Router - 完整版
集成：Registry + Fallback + Quota
"""
from model_registry import MODEL_REGISTRY
from fallback_manager import get_fallback_manager
from quota_manager import update_usage, should_use_model, get_status


def estimate_tokens(text: str) -> int:
    """估算token数量 (简单估算: 1 token ≈ 4 字符)"""
    return len(text) // 4


def route(task_type: str, prompt: str) -> dict:
    """
    核心路由函数
    
    自动处理:
    1. 任务类型识别
    2. 配额检查
    3. Fallback自动切换
    
    Args:
        task_type: 任务类型 (code/general/analysis/fast)
        prompt: 用户输入
    
    Returns:
        {"success": True/False, "response": "...", "model": "..."}
    """
    # 获取模型列表
    models = MODEL_REGISTRY.get(task_type, MODEL_REGISTRY["general"])
    
    fallback_mgr = get_fallback_manager()
    fallback_count = 0
    
    for model_info in models:
        model_name = model_info["name"]
        
        # 1. 配额检查
        if not should_use_model(model_name):
            print(f"  ⏭️ 跳过 {model_name} (配额不足)")
            fallback_count += 1
            continue
        
        # 2. 调用模型
        print(f"  → 尝试 {model_name}...")
        result = fallback_mgr.try_model(model_info, prompt)
        
        if result["success"]:
            # 3. 更新配额使用
            tokens = estimate_tokens(prompt) + estimate_tokens(result["response"])
            update_usage(model_name, tokens)
            
            return {
                "success": True,
                "response": result["response"],
                "model": model_name,
                "fallback_count": fallback_count,
            }
        
        # 4. 失败，继续下一个
        fallback_count += 1
        print(f"  ⚠️ {model_name} 失败: {result.get('error')}")
    
    # 所有模型都失败
    return {
        "success": False,
        "error": "All models failed",
    }


def route_code(prompt: str) -> str:
    """代码任务"""
    result = route("code", prompt)
    if result["success"]:
        return result["response"]
    raise Exception(result.get("error", "Failed"))


def route_analysis(prompt: str) -> str:
    """分析任务"""
    result = route("analysis", prompt)
    if result["success"]:
        return result["response"]
    raise Exception(result.get("error", "Failed"))


def route_fast(prompt: str) -> str:
    """快速任务"""
    result = route("fast", prompt)
    if result["success"]:
        return result["response"]
    raise Exception(result.get("error", "Failed"))


# 测试
if __name__ == "__main__":
    print("=== Model Router 完整版测试 ===\n")
    
    # 查看配额状态
    from quota_manager import print_status
    print_status()
    
    # 测试路由
    print("\n【测试路由】")
    result = route("code", "写一个Python加法函数")
    
    print(f"\n结果:")
    print(f"  成功: {result['success']}")
    print(f"  模型: {result.get('model', 'N/A')}")
    print(f"  切换: {result.get('fallback_count', 0)}次")
    if result['success']:
        print(f"  回复: {result['response'][:80]}...")
