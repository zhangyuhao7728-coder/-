"""
LLM Service
统一 LLM 服务层
"""

import json
from typing import Dict, List, Optional
from pathlib import Path

from organization_core.llm.providers.ollama_provider import OllamaProvider
from organization_core.llm.providers.minimax_provider import MiniMaxProvider


class LLMService:
    """统一 LLM 服务"""
    
    def __init__(self, config_path: str = None):
        # 加载配置
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "model_config.json"
        
        with open(config_path) as f:
            self.config = json.load(f)
        
        # 初始化提供商
        self.providers = {
            "ollama": OllamaProvider(
                base_url=self.config["providers"]["ollama"]["base_url"],
                timeout=self.config["providers"]["ollama"]["timeout"]
            ),
            "mimax": MiniMaxProvider(
                api_key="",  # 需要配置
                base_url=self.config["providers"]["mimax"]["base_url"],
                timeout=self.config["providers"]["mimax"]["timeout"]
            )
        }
        
        # 模型路由
        self.models = self.config["models"]
        self.fallbacks = self.config["fallbacks"]
        
        print("✅ LLMService initialized")
        print(f"   - Models: {list(self.models.keys())}")
        print(f"   - Providers: {list(self.providers.keys())}")
    
    def route(self, agent: str, task_type: str) -> str:
        """
        路由到合适的模型
        
        Args:
            agent: Agent 名称
            task_type: 任务类型 (code/analysis/general)
            
        Returns:
            模型标识符 (e.g., "ollama/qwen2.5:14b")
        """
        # 根据任务类型选择模型
        if task_type in self.models:
            return self.models[task_type]
        
        # 默认通用模型
        return self.models["general"]
    
    def generate(
        self, 
        agent: str = None, 
        task_type: str = "general", 
        prompt: str = "",
        system: str = None,
        **kwargs
    ) -> str:
        """
        生成文本
        
        Args:
            agent: Agent 名称
            task_type: 任务类型
            prompt: 提示
            system: 系统提示
            
        Returns:
            生成的文本
        """
        # 1. 路由选择模型
        model_key = self.route(agent, task_type)
        
        # 2. 解析提供商和模型
        if "/" in model_key:
            provider_name, model = model_key.split("/", 1)
        else:
            provider_name = "ollama"
            model = model_key
        
        # 3. 获取提供商
        provider = self.providers.get(provider_name)
        
        if not provider:
            # 尝试 fallback
            fallback_key = self.fallbacks.get(task_type, self.models["general"])
            if "/" in fallback_key:
                provider_name, model = fallback_key.split("/", 1)
            else:
                provider_name = "ollama"
                model = fallback_key
            provider = self.providers.get(provider_name)
        
        if not provider:
            raise RuntimeError(f"No provider available for {model_key}")
        
        # 4. 调用生成
        print(f"🤖 LLMService: {provider_name}/{model}")
        
        try:
            return provider.generate(model, prompt, system, **kwargs)
        except Exception as e:
            # 5. 降级处理
            print(f"⚠️ LLM call failed: {e}, trying fallback...")
            
            fallback_key = self.fallbacks.get(task_type, self.models["general"])
            if "/" in fallback_key:
                provider_name, model = fallback_key.split("/", 1)
            else:
                provider_name = "ollama"
                model = fallback_key
            
            provider = self.providers.get(provider_name, self.providers["ollama"])
            return provider.generate(model, prompt, system, **kwargs)
    
    def chat(
        self,
        agent: str = None,
        task_type: str = "general",
        messages: List[Dict] = None,
        **kwargs
    ) -> str:
        """对话模式"""
        if not messages:
            return ""
        
        # 提取最后一条用户消息作为 prompt
        user_prompt = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_prompt = msg.get("content", "")
                break
        
        system_prompt = None
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
                break
        
        return self.generate(agent, task_type, user_prompt, system_prompt, **kwargs)
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """获取可用模型"""
        result = {}
        
        for name, provider in self.providers.items():
            try:
                models = provider.list_models()
                result[name] = models
            except:
                result[name] = []
        
        return result


# 全局实例
_llm_service = None


def get_llm_service() -> LLMService:
    """获取 LLM 服务实例"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
