"""
LLM Module
LLM 提供商抽象层
"""

from .base import BaseLLMProvider, LLMResponse, LLMMessage
from .cloud_provider import MiniMaxProvider, get_minimax_provider, set_minimax_api_key
from .local_provider import OllamaProvider, get_ollama_provider, set_ollama_model
from .registry import LLMRegistry, get_llm_registry, get_provider, register_provider
from .router import LLMRouter, get_llm_router

__all__ = [
    # Base
    "BaseLLMProvider",
    "LLMResponse",
    "LLMMessage",
    
    # Cloud
    "MiniMaxProvider",
    "get_minimax_provider",
    "set_minimax_api_key",
    
    # Local
    "OllamaProvider",
    "get_ollama_provider",
    "set_ollama_model",
    
    # Registry
    "LLMRegistry",
    "get_llm_registry",
    "get_provider",
    "register_provider",
    
    # Router
    "LLMRouter",
    "get_llm_router",
]
