#!/usr/bin/env python3
"""
Fallback Manager - 失败自动切换管理器
功能：
1. 异常捕获
2. 自动切换模型
3. 配额检测与切换
"""
import os
import requests
from typing import Dict, List


# ========== Provider 实现 ==========

class OllamaProvider:
    """Ollama 本地模型"""
    
    BASE_URL = "http://localhost:11434"
    
    def generate(self, model: str, prompt: str) -> Dict:
        try:
            resp = requests.post(
                f"{self.BASE_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {"success": True, "response": resp.json().get("response", "")}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}", "provider": "ollama"}
        except Exception as e:
            return {"success": False, "error": str(e), "provider": "ollama"}


class MiniMaxProvider:
    """MiniMax 云模型"""
    
    BASE_URL = "https://api.minimax.chat/v1"
    
    def generate(self, model: str, prompt: str) -> Dict:
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key", "provider": "minimax"}
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {"success": True, "response": resp.json()["choices"][0]["message"]["content"]}
            elif resp.status_code == 429:
                # Quota 用完
                return {"success": False, "error": "QUOTA_EXCEEDED", "provider": "minimax", "quota": True}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}", "provider": "minimax"}
        except Exception as e:
            return {"success": False, "error": str(e), "provider": "minimax"}


class DoubaoProvider:
    """Doubao 火山引擎"""
    
    BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
    
    def generate(self, model: str, prompt: str) -> Dict:
        api_key = os.environ.get("VOLCENGINE_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key", "provider": "doubao"}
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {"success": True, "response": resp.json()["choices"][0]["message"]["content"]}
            elif resp.status_code == 429:
                return {"success": False, "error": "QUOTA_EXCEEDED", "provider": "doubao", "quota": True}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}", "provider": "doubao"}
        except Exception as e:
            return {"success": False, "error": str(e), "provider": "doubao"}


# ========== Provider 实例 ==========
ollama = OllamaProvider()
minimax = MiniMaxProvider()
doubao = DoubaoProvider()


# ========== Fallback Manager ==========

class FallbackManager:
    """Fallback 管理器"""
    
    # 配额阈值 (百分比)
    QUOTA_WARNING = 80
    QUOTA_CRITICAL = 90
    
    def __init__(self):
        self.providers = {
            "ollama": ollama,
            "minimax": minimax,
            "doubao": doubao,
        }
        
        # 配额状态
        self.quota_status = {
            "minimax": 0,
            "doubao": 0,
        }
        
        # 统计
        self.stats = {
            "total_calls": 0,
            "successful": 0,
            "fallback_calls": 0,
            "quota_switches": 0,
        }
    
    def try_model(self, model_info: Dict, prompt: str) -> Dict:
        """
        尝试调用模型
        
        Args:
            model_info: {"name": "xxx", "provider": "ollama/minimax/doubao"}
            prompt: 用户输入
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        self.stats["total_calls"] += 1
        
        name = model_info["name"]
        provider_name = model_info["provider"]
        
        # 获取provider
        provider = self.providers.get(provider_name)
        if not provider:
            return {"success": False, "error": f"Unknown provider: {provider_name}"}
        
        # 调用
        result = provider.generate(name, prompt)
        
        # 成功
        if result["success"]:
            self.stats["successful"] += 1
            return result
        
        # 检查是否是配额问题
        if result.get("quota"):
            self.stats["quota_switches"] += 1
            print(f"  ⚠️ {provider_name} 配额用完，标记需要切换")
        
        return result
    
    def route_with_fallback(self, models: List[Dict], prompt: str) -> Dict:
        """
        带Fallback的路由
        
        Args:
            models: 模型列表 [{"name": "...", "provider": "..."}]
            prompt: 用户输入
        
        Returns:
            {"success": True/False, "response": "...", "fallback_count": N}
        """
        fallback_count = 0
        
        for model_info in models:
            result = self.try_model(model_info, prompt)
            
            if result["success"]:
                result["fallback_count"] = fallback_count
                return result
            
            # 失败，尝试下一个
            fallback_count += 1
            self.stats["fallback_calls"] += 1
            print(f"  → 切换到备用模型: {model_info['name']}")
        
        # 所有都失败
        return {
            "success": False,
            "error": "All models failed",
            "fallback_count": fallback_count
        }
    
    def get_stats(self) -> Dict:
        return self.stats.copy()


# 全局实例
_fallback_manager = None

def get_fallback_manager() -> FallbackManager:
    global _fallback_manager
    if _fallback_manager is None:
        _fallback_manager = FallbackManager()
    return _fallback_manager


def try_model(model_info: Dict, prompt: str) -> Dict:
    """便捷函数"""
    return get_fallback_manager().try_model(model_info, prompt)


# 测试
if __name__ == "__main__":
    mgr = get_fallback_manager()
    
    print("=== Fallback Manager 测试 ===\n")
    
    # 测试单个模型
    print("【测试 Ollama】")
    result = mgr.try_model({"name": "qwen2.5:7b", "provider": "ollama"}, "你好")
    print(f"结果: {result}")
    
    print(f"\n统计: {mgr.get_stats()}")
