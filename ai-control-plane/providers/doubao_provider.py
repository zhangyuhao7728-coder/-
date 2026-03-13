#!/usr/bin/env python3
"""
Doubao Provider - 火山引擎模型提供者
"""
import os
import requests
from typing import Dict


class DoubaoProvider:
    """Doubao提供者"""
    
    def __init__(self, api_key: str = None, base_url: str = "https://ark.cn-beijing.volces.com/api/v3"):
        self.api_key = api_key or os.environ.get('VOLCENGINE_API_KEY', '')
        self.base_url = base_url
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return bool(self.api_key)
    
    def generate(self, model: str, prompt: str, **kwargs) -> Dict:
        """生成回复"""
        if not self.is_available():
            return {'error': 'API key not set'}
        
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': model,
                    'messages': [{'role': 'user', 'content': prompt}],
                },
                timeout=kwargs.get('timeout', 60)
            )
            
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'success': True,
                    'response': data['choices'][0]['message']['content']
                }
            else:
                return {'error': f'HTTP {resp.status_code}', 'detail': resp.text}
                
        except Exception as e:
            return {'error': str(e)}


# 全局实例
_doubao_provider = None

def get_doubao_provider() -> DoubaoProvider:
    global _doubao_provider
    if _doubao_provider is None:
        _doubao_provider = DoubaoProvider()
    return _doubao_provider
