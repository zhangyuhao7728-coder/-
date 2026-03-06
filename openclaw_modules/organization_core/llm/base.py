"""
LLM Base Provider
LLM 提供商抽象基类
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class LLMMessage:
    """LLM 消息"""
    
    def __init__(self, role: str, content: str):
        self.role = role  # "system", "user", "assistant"
        self.content = content
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class LLMResponse:
    """LLM 响应"""
    
    def __init__(
        self, 
        content: str, 
        model: str,
        tokens_used: Optional[int] = None,
        finish_reason: Optional[str] = None
    ):
        self.content = content
        self.model = model
        self.tokens_used = tokens_used
        self.finish_reason = finish_reason


class BaseLLMProvider(ABC):
    """LLM 提供商抽象基类"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """提供商名称"""
        pass
    
    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """最大 token 数"""
        pass
    
    @property
    @abstractmethod
    def supports_streaming(self) -> bool:
        """是否支持流式输出"""
        pass
    
    @abstractmethod
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        生成响应
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大 token 数
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 响应对象
        """
        pass
    
    def chat(self, message: str, system_prompt: Optional[str] = None, **kwargs) -> LLMResponse:
        """
        简单对话接口
        
        Args:
            message: 用户消息
            system_prompt: 系统提示
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 响应对象
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        return self.generate(messages, **kwargs)
    
    @abstractmethod
    def estimate_tokens(self, text: str) -> int:
        """
        估算 token 数量
        
        Args:
            text: 文本
            
        Returns:
            估算的 token 数
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        健康检查
        
        Returns:
            是否可用
        """
        pass
