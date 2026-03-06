"""
Ollama Provider
本地模型提供商
"""

import requests
from typing import Dict, List, Optional


class OllamaProvider:
    """Ollama 本地模型提供商"""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
    
    def generate(self, model: str, prompt: str, system: str = None, **kwargs) -> str:
        """
        生成文本
        
        Args:
            model: 模型名称
            prompt: 提示
            system: 系统提示
            
        Returns:
            生成的文本
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        if system:
            payload["system"] = system
        
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()["response"]
    
    def chat(self, model: str, messages: List[Dict], **kwargs) -> str:
        """
        对话模式
        
        Args:
            model: 模型名称
            messages: 消息列表
            
        Returns:
            回复文本
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()["message"]["content"]
    
    def list_models(self) -> List[str]:
        """列出可用模型"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            return len(self.list_models()) > 0
        except:
            return False
