"""
MiniMax Provider
云端模型提供商
"""

import requests
from typing import Dict, List, Optional


class MiniMaxProvider:
    """MiniMax 云端模型提供商"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.minimax.chat/v1", timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.model = "MiniMax-M2.5"
    
    def generate(self, model: str, prompt: str, system: str = None, **kwargs) -> str:
        """
        生成文本
        
        Args:
            model: 模型名称 (会被忽略)
            prompt: 提示
            system: 系统提示
            
        Returns:
            生成的文本
        """
        url = f"{self.base_url}/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def chat(self, model: str, messages: List[Dict], **kwargs) -> str:
        """
        对话模式
        
        Args:
            model: 模型名称 (会被忽略)
            messages: 消息列表
            
        Returns:
            回复文本
        """
        url = f"{self.base_url}/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def health_check(self) -> bool:
        """健康检查"""
        try:
            self.generate("test", "hi")
            return True
        except:
            return False
