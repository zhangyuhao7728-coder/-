#!/usr/bin/env python3
"""
MiniMax Provider - MiniMax 云模型
统一接口
"""
import os
import requests
from typing import Dict
from base import BaseProvider


class MiniMaxProvider(BaseProvider):
    """MiniMax 云模型"""
    
    BASE_URL = "https://api.minimax.chat/v1"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return bool(self.api_key)
    
    def generate(self, model: str, prompt: str) -> Dict:
        """
        生成回复
        
        Args:
            model: 模型名称 (如 MiniMax-M2.5)
            prompt: 用户输入
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "No API key",
                "provider": "minimax",
            }
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "success": True,
                    "response": data["choices"][0]["message"]["content"],
                    "model": model,
                    "provider": "minimax",
                }
            elif resp.status_code == 401:
                return {
                    "success": False,
                    "error": "Invalid API key",
                    "provider": "minimax",
                }
            elif resp.status_code == 429:
                # 配额用完
                return {
                    "success": False,
                    "error": "QUOTA_EXCEEDED",
                    "provider": "minimax",
                    "quota": True,
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {resp.status_code}",
                    "provider": "minimax",
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Timeout",
                "provider": "minimax",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "minimax",
            }


# 全局实例
_minimax = None

def get_minimax() -> MiniMaxProvider:
    global _minimax
    if _minimax is None:
        _minimax = MiniMaxProvider()
    return _minimax


# 便捷函数
def generate(model: str, prompt: str) -> Dict:
    """生成回复"""
    return get_minimax().generate(model, prompt)


# 测试
if __name__ == "__main__":
    provider = get_minimax()
    
    print("=== MiniMax Provider ===\n")
    print(f"可用: {provider.is_available()}")
    
    if provider.is_available():
        result = provider.generate("MiniMax-M2.5", "你好")
        print(f"结果: {result['success']}")
        if result["success"]:
            print(f"回复: {result['response'][:50]}...")
