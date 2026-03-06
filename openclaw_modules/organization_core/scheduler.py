"""
Scheduler
负责决策调度 + LLM 智能路由
"""

from typing import Dict, Optional
from organization_core.llm.router import get_llm_router


class Scheduler:
    """调度器 - 意图识别 + LLM 路由"""
    
    # LLM 路由阈值配置
    USE_LLM_ROUTING = True  # 启用 LLM 路由
    LOCAL_THRESHOLD = 1500   # token 阈值
    
    def __init__(self):
        self.llm_router = get_llm_router()
        print("✅ Scheduler initialized with LLM routing")
    
    def decide(self, message: Dict) -> str:
        """
        决策：哪个 Agent 处理消息
        
        Args:
            message: 消息字典
            
        Returns:
            Agent 名称
        """
        content = message.get("content", "")
        
        # 原有规则匹配
        if "审查" in content or "review" in content.lower() or "审计" in content:
            return "reviewer"
        if "计划" in content or "规划" in content:
            return "planner"
        if "研究" in content or "调研" in content or "搜索" in content:
            return "researcher"
        if "写代码" in content or "代码" in content or "编程" in content or "脚本" in content or "开发" in content:
            return "engineer"
        if "分析" in content or "统计" in content:
            return "analyst"
        
        return "ceo"
    
    def select_llm_provider(self, message: Dict) -> str:
        """
        选择 LLM 提供商 (本地/云端)
        
        Args:
            message: 消息字典
            
        Returns:
            提供商名称
        """
        content = message.get("content", "")
        
        # 使用 LLM Router 选择
        provider = self.llm_router.select_provider(content)
        
        print(f"📡 LLM Provider selected: {provider} (content length: {len(content)})")
        
        return provider
    
    def decide_with_llm(self, message: Dict) -> tuple:
        """
        决策：Agent + LLM 提供商
        
        Args:
            message: 消息字典
            
        Returns:
            (agent_name, llm_provider)
        """
        agent = self.decide(message)
        provider = self.select_llm_provider(message)
        
        return agent, provider
