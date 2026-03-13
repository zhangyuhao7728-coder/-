#!/usr/bin/env python3
"""
Ollama Provider - 本地模型提供者
统一接口
"""
import requests
from typing import Dict
from base import BaseProvider


class OllamaProvider(BaseProvider):
    """Ollama 本地模型"""
    
    BASE_URL = "http://localhost:11434"
    
    def __init__(self):
        self.available_models = []
        self._refresh()
    
    def _refresh(self):
        """刷新可用模型"""
        try:
            resp = requests.get(f"{self.BASE_URL}/api/tags", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                self.available_models = [m["name"] for m in data.get("models", [])]
        except:
            self.available_models = []
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return len(self.available_models) > 0
    
    def list_models(self) -> list:
        """列出可用模型"""
        return self.available_models.copy()
    
    def generate(self, model: str, prompt: str) -> Dict:
        """
        生成回复
        
        Args:
            model: 模型名称 (如 qwen2.5:7b)
            prompt: 用户输入
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        try:
            resp = requests.post(
                f"{self.BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "success": True,
                    "response": data.get("response", ""),
                    "model": model,
                    "provider": "ollama",
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {resp.status_code}",
                    "provider": "ollama",
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Timeout",
                "provider": "ollama",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "ollama",
            }


# 全局实例
_ollama = None

def get_ollama() -> OllamaProvider:
    global _ollama
    if _ollama is None:
        _ollama = OllamaProvider()
    return _ollama


# 便捷函数
def generate(model: str, prompt: str) -> Dict:
    """生成回复"""
    return get_ollama().generate(model, prompt)


# 测试
if __name__ == "__main__":
    provider = get_ollama()
    
    print("=== Ollama Provider ===\n")
    print(f"可用: {provider.is_available()}")
    print(f"模型: {provider.list_models()}")
    
    # 测试生成
    result = provider.generate("qwen2.5:latest", "你好")
    print(f"\n结果: {result['success']}")
    if result["success"]:
        print(f"回复: {result['response'][:50]}...")
