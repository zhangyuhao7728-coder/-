"""
Cloud LLM Provider
云端 LLM 提供商 (MiniMax)
"""

import requests
from typing import List, Dict, Any, Optional
from organization_core.llm.base import BaseLLMProvider, LLMResponse
import os


class MiniMaxProvider(BaseLLMProvider):
    """MiniMax 云端 LLM 提供商"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """
        初始化 MiniMax 提供商
        
        Args:
            api_key: API Key (默认从环境变量读取)
            base_url: API 地址
        """
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self.base_url = base_url or "https://api.minimax.chat/v1"
        self.model = "MiniMax-M2.5"
        
        # Token 限制
        self._max_tokens = 200000  # 200k context
        
        # 估算比率 (中文约 1.5 token/char, 英文约 4 char/token)
        self._token_ratio = 0.5
    
    @property
    def name(self) -> str:
        return "minimax"
    
    @property
    def max_tokens(self) -> int:
        return self._max_tokens
    
    @property
    def supports_streaming(self) -> bool:
        return False  # MiniMax M2.5 暂不支持流式
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        调用 MiniMax API 生成响应
        
        Args:
            messages: 消息列表
            temperature: 温度
            max_tokens: 最大 token
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 响应对象
        """
        url = f"{self.base_url}/text/chatcompletion_v2"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        # 添加其他参数
        payload.update(kwargs)
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # 解析响应
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage", {})
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=usage.get("total_tokens", 0),
                finish_reason=data["choices"][0].get("finish_reason")
            )
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"MiniMax API error: {e}")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Invalid MiniMax response: {e}")
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算 token 数量
        
        Args:
            text: 文本
            
        Returns:
            估算的 token 数
        """
        # 简单估算：中文字符约 1.5 token/字符
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        other_chars = len(text) - chinese_chars
        
        return int(chinese_chars * 1.5 + other_chars * 0.25)
    
    def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            是否可用
        """
        if not self.api_key:
            return False
        
        try:
            # 发送简单请求测试
            self.chat("test")
            return True
        except:
            return False


# 全局实例
_minimax_provider = None


def get_minimax_provider() -> MiniMaxProvider:
    """获取 MiniMax 提供商实例"""
    global _minimax_provider
    if _minimax_provider is None:
        _minimax_provider = MiniMaxProvider()
    return _minimax_provider


def set_minimax_api_key(api_key: str) -> None:
    """设置 API Key"""
    global _minimax_provider
    _minimax_provider = MiniMaxProvider(api_key=api_key)
