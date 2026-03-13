#!/usr/bin/env python3
"""
Load Balancer - 模型负载均衡器
功能：
1. 负载统计
2. 最小负载选择
3. 自动分流
"""
from typing import Dict, List
from datetime import datetime


class LoadBalancer:
    """模型负载均衡器"""
    
    # 模型负载统计
    MODEL_LOAD = {
        "qwen2.5:latest": 0,
        "qwen2.5:7b": 0,
        "qwen3.5:9b": 0,
        "deepseek-coder:6.7b": 0,
        "minimax/MiniMax-M2.5": 0,
        "volcengine/doubao-seed-code": 0,
    }
    
    # 模型最大负载
    MAX_LOAD = {
        "ollama": 5,      # 本地模型最大并发
        "minimax": 10,    # 云模型更大
        "doubao": 10,
    }
    
    def __init__(self):
        self.load = self.MODEL_LOAD.copy()
        self.history = []
        self.total_requests = 0
    
    def select_least_loaded(self, models: List[str]) -> str:
        """
        选择负载最低的模型
        
        Args:
            models: 可用模型列表
        
        Returns:
            负载最低的模型名
        """
        # 过滤掉负载高的模型
        available = [m for m in models if self.load.get(m, 0) < self.get_max_load(m)]
        
        if not available:
            # 所有模型都满负载，返回负载最低的
            available = models
        
        # 选择负载最低的
        selected = min(available, key=lambda m: self.load.get(m, 0))
        
        return selected
    
    def get_max_load(self, model: str) -> int:
        """获取模型最大负载"""
        if "ollama" in model or model in ["qwen2.5:latest", "qwen3.5:9b", "deepseek-coder:6.7b"]:
            return self.MAX_LOAD["ollama"]
        elif "minimax" in model:
            return self.MAX_LOAD["minimax"]
        else:
            return self.MAX_LOAD["doubao"]
    
    def record_request(self, model: str):
        """记录请求"""
        self.load[model] = self.load.get(model, 0) + 1
        self.total_requests += 1
        
        self.history.append({
            "model": model,
            "action": "request",
            "time": datetime.now().isoformat(),
        })
        
        # 保留最近100条
        self.history = self.history[-100:]
    
    def record_complete(self, model: str):
        """记录完成"""
        self.load[model] = max(0, self.load.get(model, 0) - 1)
        
        self.history.append({
            "model": model,
            "action": "complete",
            "time": datetime.now().isoformat(),
        })
    
    def record_error(self, model: str):
        """记录错误"""
        # 错误不算完全卸载，稍微减少
        self.load[model] = max(0, self.load.get(model, 0) - 0.5)
    
    def get_load(self, model: str) -> int:
        """获取模型当前负载"""
        return self.load.get(model, 0)
    
    def get_load_percentage(self, model: str) -> float:
        """获取负载百分比"""
        max_load = self.get_max_load(model)
        current = self.get_load(model)
        return (current / max_load) * 100 if max_load > 0 else 0
    
    def is_available(self, model: str) -> bool:
        """检查模型是否可用"""
        return self.get_load(model) < self.get_max_load(model)
    
    def get_available_models(self, models: List[str]) -> List[str]:
        """获取可用模型列表"""
        return [m for m in models if self.is_available(m)]
    
    def balance(self, models: List[str]) -> str:
        """
        负载均衡选择
        
        综合考虑:
        1. 当前负载
        2. 模型能力
        3. 成本
        """
        # 首先过滤不可用的
        available = self.get_available_models(models)
        
        if not available:
            # 返回负载最低的
            return self.select_least_loaded(models)
        
        # 选择负载最低的
        return self.select_least_loaded(available)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "total_requests": self.total_requests,
            "load": self.load.copy(),
            "models": {
                m: {
                    "current": self.load.get(m, 0),
                    "max": self.get_max_load(m),
                    "percentage": self.get_load_percentage(m),
                    "available": self.is_available(m),
                }
                for m in self.load.keys()
            }
        }
    
    def print_status(self):
        """打印状态"""
        print("=== Load Balancer ===\n")
        
        for model, info in self.get_stats()["models"].items():
            icon = "✅" if info["available"] else "❌"
            bar = "█" * int(info["percentage"] / 10) + "░" * (10 - int(info["percentage"] / 10))
            
            print(f"{icon} {model}")
            print(f"   负载: [{bar}] {info['percentage']:.0f}% ({info['current']}/{info['max']})")


# 全局实例
_balancer = None

def get_load_balancer() -> LoadBalancer:
    global _balancer
    if _balancer is None:
        _balancer = LoadBalancer()
    return _balancer


def select_least_loaded(models: List[str]) -> str:
    """选择负载最低的模型"""
    return get_load_balancer().select_least_loaded(models)


# 测试
if __name__ == "__main__":
    balancer = get_load_balancer()
    
    print("=== Load Balancer 测试 ===\n")
    
    # 模拟请求
    models = ["qwen2.5:latest", "qwen3.5:9b", "deepseek-coder:6.7b"]
    
    for i in range(5):
        model = balancer.balance(models)
        print(f"请求 {i+1} -> {model}")
        balancer.record_request(model)
    
    print()
    balancer.print_status()
