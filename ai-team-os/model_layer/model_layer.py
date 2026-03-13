#!/usr/bin/env python3
"""
Model Layer - 模型层
统一接口各种模型
"""
import os
import requests
from typing import Dict, List


class ModelLayer:
    """模型层"""
    
    def __init__(self):
        # Provider实例
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """初始化Provider"""
        self.providers = {
            "ollama": OllamaProvider(),
            "minimax": MiniMaxProvider(),
            "doubao": DoubaoProvider(),
        }
    
    def call(self, model: str, prompt: str) -> Dict:
        """
        统一调用接口
        
        Args:
            model: 模型名
            prompt: 输入
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        # 判断provider
        if "/" in model:
            provider_name = model.split("/")[0]
        elif "qwen" in model or "deepseek" in model:
            provider_name = "ollama"
        elif "minimax" in model:
            provider_name = "minimax"
        else:
            provider_name = "ollama"
        
        # 调用
        provider = self.providers.get(provider_name)
        if provider:
            return provider.generate(model, prompt)
        
        return {"success": False, "error": f"Unknown provider: {provider_name}"}
    
    def get_available_models(self) -> List[str]:
        """获取可用模型"""
        models = []
        
        # Ollama
        ollama_models = self.providers["ollama"].list_models()
        models.extend(ollama_models)
        
        return models


class OllamaProvider:
    """Ollama Provider"""
    
    BASE_URL = "http://localhost:11434"
    
    def list_models(self) -> List[str]:
        try:
            resp = requests.get(f"{self.BASE_URL}/api/tags", timeout=5)
            if resp.status_code == 200:
                return [m["name"] for m in resp.json().get("models", [])]
        except:
            pass
        return []
    
    def generate(self, model: str, prompt: str) -> Dict:
        try:
            resp = requests.post(
                f"{self.BASE_URL}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json().get("response", ""),
                    "model": model,
                    "provider": "ollama",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Failed"}


class MiniMaxProvider:
    """MiniMax Provider"""
    
    BASE_URL = "https://api.minimax.chat/v1"
    
    def generate(self, model: str, prompt: str) -> Dict:
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key"}
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json()["choices"][0]["message"]["content"],
                    "model": model,
                    "provider": "minimax",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Failed"}


class DoubaoProvider:
    """Doubao Provider"""
    
    BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
    
    def generate(self, model: str, prompt: str) -> Dict:
        api_key = os.environ.get("VOLCENGINE_API_KEY", "")
        if not api_key:
            return {"success": False, "error": "No API key"}
        
        try:
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}]},
                timeout=60
            )
            
            if resp.status_code == 200:
                return {
                    "success": True,
                    "response": resp.json()["choices"][0]["message"]["content"],
                    "model": model,
                    "provider": "doubao",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Failed"}


# 全局实例
_layer = None

def get_model_layer() -> ModelLayer:
    global _layer
    if _layer is None:
        _layer = ModelLayer()
    return _layer


def call_model(model: str, prompt: str) -> Dict:
    """统一调用"""
    return get_model_layer().call(model, prompt)


# 测试
if __name__ == "__main__":
    layer = get_model_layer()
    
    print("=== Model Layer 测试 ===\n")
    
    # 可用模型
    models = layer.get_available_models()
    print(f"Ollama模型: {models}")
    
    # 调用
    result = layer.call("qwen2.5:latest", "Hi")
    print(f"\n调用结果: {result['success']}")
    if result['success']:
        print(f"回复: {result['response'][:50]}...")
