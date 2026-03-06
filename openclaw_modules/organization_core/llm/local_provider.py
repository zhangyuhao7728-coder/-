"""
Local LLM Provider
本地 LLM 提供商 (Ollama)
"""

import requests
import json
from typing import List, Dict, Any, Optional, Generator
from organization_core.llm.base import BaseLLMProvider, LLMResponse
import os


class OllamaProvider(BaseLLMProvider):
    """Ollama 本地 LLM 提供商"""
    
    def __init__(self, base_url: str = None, model: str = "qwen2.5:7b"):
        """
        初始化 Ollama 提供商
        
        Args:
            base_url: Ollama 服务地址
            model: 模型名称
        """
        self.base_url = base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = model
        
        # Token 限制 (Qwen2.5 7B 约 8k)
        self._max_tokens = 8192
    
    @property
    def name(self) -> str:
        return "ollama"
    
    @property
    def max_tokens(self) -> int:
        return self._max_tokens
    
    @property
    def supports_streaming(self) -> bool:
        return True
    
    def generate(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> LLMResponse:
        """
        调用 Ollama API 生成响应
        
        Args:
            messages: 消息列表
            temperature: 温度
            max_tokens: 最大 token
            **kwargs: 其他参数
            
        Returns:
            LLMResponse: 响应对象
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False
        }
        
        if max_tokens:
            payload["num_predict"] = max_tokens
        
        # 添加其他参数
        payload.update(kwargs)
        
        try:
            response = requests.post(url, json=payload, timeout=30)  # 30秒超时
            response.raise_for_status()
            
            # 手动解析 JSON
            text = response.text.strip()
            data = json.loads(text)
            
            # 解析响应
            content = data["message"]["content"]
            
            return LLMResponse(
                content=content,
                model=self.model,
                tokens_used=data.get("eval_count", len(content.split()))
            )
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API error: {e}")
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Invalid Ollama response: {e}, response: {response.text[:200] if response else 'no response'}")
    
    def generate_stream(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        流式生成响应
        
        Args:
            messages: 消息列表
            temperature: 温度
            max_tokens: 最大 token
            **kwargs: 其他参数
            
        Yields:
            生成的文本片段
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        
        if max_tokens:
            payload["num_predict"] = max_tokens
        
        try:
            response = requests.post(url, json=payload, timeout=30, stream=True)  # 30秒超时
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'message' in data and 'content' in data['message']:
                            content = data['message']['content']
                            if content:
                                yield content
                    except:
                        pass
                            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama streaming error: {e}")
    
    def estimate_tokens(self, text: str) -> int:
        """
        估算 token 数量
        
        Args:
            text: 文本
            
        Returns:
            估算的 token 数
        """
        # 简单估算：约 4 个字符 = 1 token
        return len(text) // 4
    
    def health_check(self) -> bool:
        """
        健康检查 (带超时)
        
        Returns:
            是否可用
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[str]:
        """
        列出可用模型 (带超时)
        
        Returns:
            模型列表
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
        except:
            return []


# 全局实例
_ollama_provider = None


def get_ollama_provider() -> OllamaProvider:
    """获取 Ollama 提供商实例"""
    global _ollama_provider
    if _ollama_provider is None:
        _ollama_provider = OllamaProvider()
    return _ollama_provider


def set_ollama_model(model: str) -> None:
    """设置模型"""
    global _ollama_provider
    _ollama_provider = OllamaProvider(model=model)
