#!/usr/bin/env python3
"""
Health Monitor - 模型健康监控
功能：
1. 自动检测模型状态
2. 失败自动移出
3. 自动恢复检测
"""
import time
from typing import Dict, List, Callable


class HealthMonitor:
    """模型健康监控器"""
    
    def __init__(self):
        # 模型健康状态
        self.models = {}
        
        # 健康检查函数
        self.check_funcs = {}
        
        # 配置
        self.max_failures = 3  # 连续失败3次移出
        self.check_interval = 60  # 检查间隔(秒)
        
        # 状态
        self.status = {}
        self.fail_count = {}
        self.last_check = {}
    
    # ========== 注册模型 ==========
    
    def register(self, model: str, check_func: Callable = None):
        """
        注册模型
        
        Args:
            model: 模型名称
            check_func: 检查函数 (可选)
        """
        self.models[model] = {
            "name": model,
            "healthy": True,
            "autocheck": check_func is not None,
        }
        
        self.check_funcs[model] = check_func
        self.fail_count[model] = 0
        self.status[model] = "unknown"
    
    def register_with_endpoint(self, model: str, endpoint: str, expected_status: int = 200):
        """注册带端点的模型"""
        import requests
        
        def check():
            try:
                r = requests.get(endpoint, timeout=5)
                return r.status_code == expected_status
            except:
                return False
        
        self.register(model, check)
    
    # ========== 健康检查 ==========
    
    def check(self, model: str) -> bool:
        """
        检查单个模型
        
        Returns:
            True: 健康
            False: 不健康
        """
        if model not in self.models:
            return False
        
        # 简单检查: 本地模型检查Ollama
        if model in ["qwen2.5:latest", "qwen2.5:7b", "qwen3.5:9b", "deepseek-coder:6.7b"]:
            return self._check_ollama()
        
        # 云模型需要API key
        if "minimax" in model:
            return self._check_minimax()
        
        if "doubao" in model:
            return self._check_doubao()
        
        # 默认健康
        return True
    
    def _check_ollama(self) -> bool:
        """检查Ollama"""
        import requests
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            return r.status_code == 200
        except:
            return False
    
    def _check_minimax(self) -> bool:
        """检查MiniMax"""
        import os
        import requests
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            return False
        
        try:
            r = requests.get(
                "https://api.minimax.chat/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            return r.status_code == 200
        except:
            return False
    
    def _check_doubao(self) -> bool:
        """检查Doubao"""
        import os
        import requests
        
        api_key = os.environ.get("VOLCENGINE_API_KEY", "")
        if not api_key:
            return False
        
        try:
            r = requests.get(
                "https://ark.cn-beijing.volces.com/api/v3/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            return r.status_code == 200
        except:
            return False
    
    # ========== 状态管理 ==========
    
    def mark_healthy(self, model: str):
        """标记健康"""
        self.models[model]["healthy"] = True
        self.fail_count[model] = 0
        self.status[model] = "healthy"
    
    def mark_unhealthy(self, model: str):
        """标记不健康"""
        self.fail_count[model] = self.fail_count.get(model, 0) + 1
        
        # 连续失败超过阈值，标记为不可用
        if self.fail_count[model] >= self.max_failures:
            self.models[model]["healthy"] = False
            self.status[model] = "unavailable"
            print(f"⚠️ {model} 连续{self.fail_count[model]}次失败，移出可用列表")
        else:
            self.status[model] = "degraded"
            print(f"⚠️ {model} 检查失败 ({self.fail_count[model]}/{self.max_failures})")
    
    # ========== 自动检查 ==========
    
    def check_all(self) -> Dict:
        """检查所有模型"""
        results = {}
        
        for model in self.models:
            healthy = self.check(model)
            
            if healthy:
                self.mark_healthy(model)
            else:
                self.mark_unhealthy(model)
            
            results[model] = self.status[model]
        
        return results
    
    def get_healthy_models(self) -> List[str]:
        """获取健康模型列表"""
        return [m for m, info in self.models.items() if info["healthy"]]
    
    def get_available_models(self, preferred_models: List[str]) -> List[str]:
        """从首选列表中获取可用的"""
        return [m for m in preferred_models if self.models.get(m, {}).get("healthy", False)]
    
    # ========== 状态显示 ==========
    
    def print_status(self):
        """打印状态"""
        print("=== Health Monitor ===\n")
        
        for model, info in self.models.items():
            status = self.status.get(model, "unknown")
            
            if status == "healthy":
                icon = "✅"
            elif status == "degraded":
                icon = "⚠️"
            elif status == "unavailable":
                icon = "❌"
            else:
                icon = "❓"
            
            fail_info = f" ({self.fail_count.get(model, 0)}次)" if self.fail_count.get(model, 0) > 0 else ""
            
            print(f"{icon} {model}: {status}{fail_info}")
    
    def get_stats(self) -> Dict:
        """获取统计"""
        healthy = sum(1 for s in self.status.values() if s == "healthy")
        total = len(self.models)
        
        return {
            "total": total,
            "healthy": healthy,
            "unhealthy": total - healthy,
            "models": self.status.copy(),
        }


# 全局实例
_monitor = None

def get_health_monitor() -> HealthMonitor:
    global _monitor
    if _monitor is None:
        _monitor = HealthMonitor()
        
        # 注册默认模型
        _monitor.register("qwen2.5:latest")
        _monitor.register("qwen2.5:7b")
        _monitor.register("qwen3.5:9b")
        _monitor.register("deepseek-coder:6.7b")
        _monitor.register("minimax/MiniMax-M2.5")
        _monitor.register("volcengine/doubao-seed-code")
    
    return _monitor


def check_ollama() -> bool:
    """检查Ollama"""
    return get_health_monitor()._check_ollama()


# 测试
if __name__ == "__main__":
    monitor = get_health_monitor()
    
    print("=== Health Monitor 测试 ===\n")
    
    # 检查
    monitor.check_all()
    monitor.print_status()
    
    # 获取可用
    print(f"\n可用模型: {monitor.get_healthy_models()}")
