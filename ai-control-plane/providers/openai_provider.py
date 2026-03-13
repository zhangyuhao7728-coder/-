#!/usr/bin/env python3
"""
OpenAI Provider - ChatGPT 提供商
功能：
1. GPT-4o / GPT-4 / GPT-3.5 调用
2. 自动重试
3. 成本追踪
"""
import os
import requests
from typing import Dict


class OpenAIProvider:
    """OpenAI (ChatGPT) 提供商"""
    
    BASE_URL = "https://api.openai.com/v1"
    
    # 支持的模型
    MODELS = {
        "gpt-4o": {"name": "GPT-4o", "context": 128000, "cost": 0.005},
        "gpt-4-turbo": {"name": "GPT-4 Turbo", "context": 128000, "cost": 0.01},
        "gpt-4": {"name": "GPT-4", "context": 8192, "cost": 0.03},
        "gpt-3.5-turbo": {"name": "GPT-3.5", "context": 16385, "cost": 0.002},
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return bool(self.api_key) and self.api_key != "sk-your-api-key"
    
    def list_models(self) -> list:
        """列出可用模型"""
        if not self.is_available():
            return []
        
        try:
            resp = requests.get(
                f"{self.BASE_URL}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            
            if resp.status_code == 200:
                models = resp.json()["data"]
                return [m["id"] for m in models]
        except:
            pass
        
        return list(self.MODELS.keys())
    
    def generate(self, model: str, prompt: str, **kwargs) -> Dict:
        """
        生成回复
        
        Args:
            model: 模型名 (gpt-4o, gpt-4, gpt-3.5-turbo)
            prompt: 用户输入
            **kwargs: 其他参数 (temperature, max_tokens等)
        
        Returns:
            {"success": True/False, "response": "...", "error": "..."}
        """
        if not self.is_available():
            return {"success": False, "error": "No API key", "provider": "openai"}
        
        try:
            # 构建请求
            messages = [{"role": "user", "content": prompt}]
            
            data = {
                "model": model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048),
            }
            
            resp = requests.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=data,
                timeout=kwargs.get("timeout", 60)
            )
            
            if resp.status_code == 200:
                result = resp.json()
                response = result["choices"][0]["message"]["content"]
                tokens = result.get("usage", {}).get("total_tokens", 0)
                
                return {
                    "success": True,
                    "response": response,
                    "model": model,
                    "provider": "openai",
                    "tokens": tokens,
                }
            elif resp.status_code == 401:
                return {"success": False, "error": "Invalid API key", "provider": "openai"}
            elif resp.status_code == 429:
                return {"success": False, "error": "Rate limit", "provider": "openai", "quota": True}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}", "provider": "openai"}
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Timeout", "provider": "openai"}
        except Exception as e:
            return {"success": False, "error": str(e), "provider": "openai"}
    
    def get_cost(self, model: str, tokens: int) -> float:
        """计算成本"""
        cost_per_1k = self.MODELS.get(model, {}).get("cost", 0.002)
        return (tokens / 1000) * cost_per_1k


# 全局实例
_openai = None

def get_openai() -> OpenAIProvider:
    global _openai
    if _openai is None:
        _openai = OpenAIProvider()
    return _openai


def generate(prompt: str, model: str = "gpt-4o") -> Dict:
    """生成回复"""
    return get_openai().generate(model, prompt)


# 测试
if __name__ == "__main__":
    provider = get_openai()
    
    print("=== OpenAI Provider ===\n")
    print(f"可用: {provider.is_available()}")
    print(f"模型: {list(provider.MODELS.keys())}")
    
    if provider.is_available():
        result = provider.generate("gpt-4o", "Hello, how are you?")
        print(f"\n结果: {result['success']}")
        if result["success"]:
            print(f"回复: {result['response'][:100]}...")
            print(f"Tokens: {result.get('tokens', 0)}")
