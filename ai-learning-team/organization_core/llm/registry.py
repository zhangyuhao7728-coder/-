"""
LLM Registry
LLM 提供商注册中心
"""

from typing import Dict, Optional
from organization_core.llm.base import BaseLLMProvider
from organization_core.llm.cloud_provider import MiniMaxProvider
from organization_core.llm.local_provider import OllamaProvider


class LLMRegistry:
    """LLM 提供商注册中心"""
    
    def __init__(self):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._default_provider: Optional[str] = None
    
    def register(self, name: str, provider: BaseLLMProvider, set_default: bool = False) -> None:
        """
        注册 LLM 提供商
        
        Args:
            name: 提供商名称
            provider: 提供商实例
            set_default: 是否设为默认
        """
        self._providers[name] = provider
        
        if set_default or not self._default_provider:
            self._default_provider = name
        
        print(f"✅ LLM Provider registered: {name}")
    
    def get(self, name: str) -> Optional[BaseLLMProvider]:
        """
        获取提供商
        
        Args:
            name: 提供商名称
            
        Returns:
            提供商实例
        """
        return self._providers.get(name)
    
    def get_default(self) -> Optional[BaseLLMProvider]:
        """
        获取默认提供商
        
        Returns:
            默认提供商实例
        """
        if self._default_provider:
            return self._providers.get(self._default_provider)
        return None
    
    def set_default(self, name: str) -> bool:
        """
        设置默认提供商
        
        Args:
            name: 提供商名称
            
        Returns:
            是否成功
        """
        if name in self._providers:
            self._default_provider = name
            return True
        return False
    
    def list_providers(self) -> Dict[str, dict]:
        """
        列出所有提供商
        
        Returns:
            提供商信息字典
        """
        result = {}
        for name, provider in self._providers.items():
            result[name] = {
                "name": provider.name,
                "max_tokens": provider.max_tokens,
                "supports_streaming": provider.supports_streaming,
                "health": provider.health_check(),
                "default": name == self._default_provider
            }
        return result
    
    def get_health_status(self) -> Dict[str, bool]:
        """
        获取所有提供商健康状态
        
        Returns:
            健康状态字典
        """
        return {
            name: provider.health_check() 
            for name, provider in self._providers.items()
        }


# 全局注册中心
_registry = None


def get_llm_registry() -> LLMRegistry:
    """获取 LLM 注册中心实例"""
    global _registry
    if _registry is None:
        _registry = LLMRegistry()
        
        # 自动注册默认提供商
        try:
            minimax = MiniMaxProvider()
            _registry.register("minimax", minimax, set_default=True)
        except Exception as e:
            print(f"⚠️ MiniMax registration failed: {e}")
        
        try:
            ollama = OllamaProvider()
            _registry.register("ollama", ollama)
        except Exception as e:
            print(f"⚠️ Ollama registration failed: {e}")
    
    return _registry


def register_provider(name: str, provider: BaseLLMProvider, set_default: bool = False) -> None:
    """注册 LLM 提供商（便捷函数）"""
    get_llm_registry().register(name, provider, set_default)


def get_provider(name: str = None) -> Optional[BaseLLMProvider]:
    """获取 LLM 提供商（便捷函数）"""
    registry = get_llm_registry()
    if name:
        return registry.get(name)
    return registry.get_default()
