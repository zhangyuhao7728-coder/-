"""
LLM Health Monitor
后台健康检查 - 每60秒检测本地模型健康状态
"""

import threading
import time
from typing import Dict


class LLMHealthMonitor:
    """LLM 健康监控器"""
    
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.providers: Dict[str, dict] = {}
        self.running = False
        self.thread = None
    
    def register_provider(self, name: str, provider, test_message: str = "1+1="):
        """注册 LLM 提供商"""
        self.providers[name] = {
            "provider": provider,
            "test_message": test_message,
            "healthy": True,
            "last_check": None,
            "consecutive_failures": 0
        }
    
    def start(self):
        """启动监控线程"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print(f"✅ LLM Health Monitor started (interval: {self.check_interval}s)")
    
    def stop(self):
        """停止监控"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("🔴 LLM Health Monitor stopped")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.running:
            for name, info in self.providers.items():
                self._check_provider(name, info)
            
            time.sleep(self.check_interval)
    
    def _check_provider(self, name: str, info: dict):
        """检查单个提供商"""
        provider = info["provider"]
        test_msg = info["test_message"]
        
        try:
            start = time.time()
            provider.generate([{"role": "user", "content": test_msg}])
            elapsed = time.time() - start
            
            # 成功
            info["healthy"] = True
            info["last_check"] = time.time()
            info["consecutive_failures"] = 0
            
            print(f"✅ {name} healthy (response time: {elapsed:.2f}s)")
            
        except Exception as e:
            info["consecutive_failures"] += 1
            
            # 连续3次失败标记为不健康
            if info["consecutive_failures"] >= 3:
                info["healthy"] = False
                print(f"❌ {name} marked UNHEALTHY (consecutive failures: {info['consecutive_failures']})")
            else:
                print(f"⚠️ {name} check failed ({info['consecutive_failures']}/3): {e}")
    
    def is_healthy(self, name: str) -> bool:
        """检查提供商是否健康"""
        if name not in self.providers:
            return True  # 未注册的默认健康
        return self.providers[name]["healthy"]
    
    def get_status(self) -> dict:
        """获取所有提供商状态"""
        status = {}
        for name, info in self.providers.items():
            status[name] = {
                "healthy": info["healthy"],
                "last_check": info["last_check"],
                "failures": info["consecutive_failures"]
            }
        return status
    
    def force_check(self, name: str = None):
        """强制检查"""
        if name:
            if name in self.providers:
                self._check_provider(name, self.providers[name])
        else:
            for n, i in self.providers.items():
                self._check_provider(n, i)


# 全局实例
_health_monitor = None


def get_health_monitor(check_interval: int = 60) -> LLMHealthMonitor:
    """获取健康监控器实例"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = LLMHealthMonitor(check_interval)
    return _health_monitor
