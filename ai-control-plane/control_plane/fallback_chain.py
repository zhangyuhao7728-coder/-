#!/usr/bin/env python3
"""
Fallback Chain - 自动重试 + Fallback链
功能：
1. 失败自动切换
2. 完整Fallback链
3. 最多重试次数
"""
from typing import Dict, List, Optional


class FallbackChain:
    """Fallback 链"""
    
    # 默认Fallback链 (优先级从高到低)
    DEFAULT_CHAIN = [
        "minimax/MiniMax-M2.5",           # 1. 首选 (质量最高)
        "volcengine/doubao-seed-code",    # 2. 备用 (配额)
        "qwen3.5:9b",                    # 3. 本地强模型
        "deepseek-coder:6.7b",           # 4. 代码专用
        "qwen2.5:latest",                # 5. 本地快速
    ]
    
    # 任务类型专属链
    TASK_CHAINS = {
        "code": [
            "deepseek-coder:6.7b",       # 代码首选
            "qwen3.5:9b",
            "qwen2.5:7b",
            "minimax/MiniMax-M2.5",      # 备选
        ],
        "analysis": [
            "qwen3.5:9b",                # 分析首选
            "minimax/MiniMax-M2.5",
            "volcengine/doubao-seed-code",
        ],
        "creative": [
            "minimax/MiniMax-M2.5",      # 创意首选
            "qwen2.5:14b",
            "qwen3.5:9b",
        ],
        "fast": [
            "qwen2.5:latest",            # 快速首选
            "qwen2.5:7b",
            "deepseek-coder:6.7b",
        ],
    }
    
    def __init__(self):
        # 当前链
        self.chain = self.DEFAULT_CHAIN.copy()
        
        # 统计
        self.stats = {
            "total_attempts": 0,
            "successful": 0,
            "fallback_count": 0,
            "failed": 0,
        }
        
        # 历史
        self.history = []
    
    def get_chain(self, task_type: str = None) -> List[str]:
        """获取Fallback链"""
        if task_type and task_type in self.TASK_CHAINS:
            return self.TASK_CHAINS[task_type].copy()
        return self.chain.copy()
    
    def set_chain(self, chain: List[str]):
        """设置自定义链"""
        self.chain = chain
    
    def try_model(self, model: str, prompt: str, task_type: str = "general") -> Dict:
        """
        尝试调用模型
        
        Args:
            model: 模型名
            prompt: 用户输入
            task_type: 任务类型
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        self.stats["total_attempts"] += 1
        
        # 模拟调用 (实际应该调用provider)
        result = self._call_model(model, prompt)
        
        # 记录
        self.history.append({
            "model": model,
            "success": result["success"],
            "error": result.get("error"),
            "task_type": task_type,
        })
        
        return result
    
    def _call_model(self, model: str, prompt: str) -> Dict:
        """
        调用模型 (实际实现需要provider)
        
        简化版：模拟调用
        """
        import random
        
        # 模拟成功率 (本地模型成功率低，云模型成功率高)
        if "minimax" in model or "doubao" in model:
            # 云模型
            success_rate = 0.95
        else:
            # 本地模型
            success_rate = 0.90
        
        if random.random() < success_rate:
            return {
                "success": True,
                "response": f"[{model}] 处理: {prompt[:20]}...",
                "model": model,
            }
        else:
            return {
                "success": False,
                "error": f"Mock error for {model}",
                "model": model,
            }
    
    def route_with_fallback(self, prompt: str, task_type: str = "general") -> Dict:
        """
        完整路由 + Fallback
        
        Args:
            prompt: 用户输入
            task_type: 任务类型
        
        Returns:
            {"success": True/False, "response": "...", "model": "...", "attempts": N}
        """
        chain = self.get_chain(task_type)
        
        attempts = 0
        last_error = None
        
        for model in chain:
            attempts += 1
            self.stats["fallback_count"] += 1
            
            print(f"  → 尝试: {model}")
            
            result = self.try_model(model, prompt, task_type)
            
            if result["success"]:
                self.stats["successful"] += 1
                return {
                    "success": True,
                    "response": result["response"],
                    "model": model,
                    "attempts": attempts,
                }
            
            last_error = result.get("error")
            print(f"    ⚠️ 失败: {last_error}")
        
        # 全部失败
        self.stats["failed"] += 1
        
        return {
            "success": False,
            "error": f"All models failed. Last error: {last_error}",
            "attempts": attempts,
        }
    
    def retry_failed(self, prompt: str, failed_models: List[str], task_type: str = "general") -> Dict:
        """
        重试失败的模型
        
        Args:
            prompt: 用户输入
            failed_models: 失败的模型列表
            task_type: 任务类型
        
        Returns:
            {"success": True/False, "response": "...", "model": "...", "attempts": N}
        """
        # 从链中排除失败的模型
        chain = [m for m in self.get_chain(task_type) if m not in failed_models]
        
        # 如果还有可用的
        if chain:
            # 临时设置链并重试
            original = self.chain
            self.chain = chain
            
            result = self.route_with_fallback(prompt, task_type)
            
            self.chain = original
            return result
        
        return {
            "success": False,
            "error": "No available models after excluding failed ones",
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        total = self.stats["total_attempts"]
        success_rate = (self.stats["successful"] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2),
        }
    
    def print_chain(self):
        """打印链"""
        print("=== Fallback Chain ===\n")
        
        for i, model in enumerate(self.chain, 1):
            print(f"  {i}. {model}")
        
        print("\n任务专属链:")
        for task, chain in self.TASK_CHAINS.items():
            print(f"  {task}: {' → '.join(chain[:3])}")


# 全局实例
_fallback = None

def get_fallback_chain() -> FallbackChain:
    global _fallback
    if _fallback is None:
        _fallback = FallbackChain()
    return _fallback


# 测试
if __name__ == "__main__":
    fb = get_fallback_chain()
    
    print("=== Fallback Chain 测试 ===\n")
    
    # 打印链
    fb.print_chain()
    
    print("\n【测试路由】")
    result = fb.route_with_fallback("写一个Python函数", "code")
    
    print(f"\n结果:")
    print(f"  成功: {result['success']}")
    print(f"  模型: {result.get('model', 'N/A')}")
    print(f"  尝试: {result.get('attempts', 0)}次")
    print(f"  回复: {result.get('response', result.get('error'))[:50]}...")
    
    print(f"\n统计: {fb.get_stats()}")
