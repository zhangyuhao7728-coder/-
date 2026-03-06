"""
LLM Agent Wrapper
LLM 驱动的 Agent 包装器
"""

from typing import Dict, Any, Optional, Callable
from organization_core.llm.base import LLMResponse
from organization_core.llm import get_provider, get_llm_router


class LLMAgent:
    """
    LLM 驱动的 Agent
    
    将普通 Agent 函数包装为 LLM 驱动的 Agent
    支持自动路由到本地/云端模型
    """
    
    def __init__(
        self, 
        name: str,
        system_prompt: str,
        agent_func: Optional[Callable] = None,
        llm_provider: Optional[str] = None
    ):
        """
        初始化 LLM Agent
        
        Args:
            name: Agent 名称
            system_prompt: 系统提示词
            agent_func: 原有 Agent 函数 (可选)
            llm_provider: 强制使用某个 LLM 提供商
        """
        self.name = name
        self.system_prompt = system_prompt
        self.agent_func = agent_func
        self.llm_provider = llm_provider
        self.router = get_llm_router()
        
        print(f"✅ LLMAgent initialized: {name}")
    
    def _get_provider(self) -> Any:
        """获取 LLM 提供商"""
        if self.llm_provider:
            provider = get_provider(self.llm_provider)
            if provider:
                return provider
        
        # 自动选择
        return get_provider()
    
    def generate(self, message: Dict[str, Any]) -> LLMResponse:
        """
        使用 LLM 生成响应
        
        Args:
            message: 消息字典
            
        Returns:
            LLMResponse: LLM 响应
        """
        content = message.get("content", "")
        
        # 构建消息
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": content}
        ]
        
        # 选择 LLM 提供商
        if self.llm_provider:
            provider_name = self.llm_provider
        else:
            provider_name = self.router.select_provider(content)
        
        provider = get_provider(provider_name)
        
        if not provider:
            raise RuntimeError(f"No LLM provider available: {provider_name}")
        
        print(f"🔄 [{self.name}] Using provider: {provider_name}")
        
        # 调用 LLM
        response = provider.generate(messages)
        
        return response
    
    def handle(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理消息
        
        Args:
            message: 消息字典
            
        Returns:
            处理结果
        """
        try:
            # 如果有原有函数，先调用
            if self.agent_func:
                result = self.agent_func(message)
                return result
            
            # 使用 LLM 生成
            response = self.generate(message)
            
            return {
                "agent": self.name,
                "status": "completed",
                "message": response.content,
                "llm_model": response.model,
                "tokens_used": response.tokens_used
            }
            
        except Exception as e:
            return {
                "agent": self.name,
                "status": "error",
                "error": str(e)
            }


# ========== 便捷函数 ==========

def create_llm_agent(
    name: str,
    system_prompt: str,
    agent_func: Optional[Callable] = None,
    llm_provider: Optional[str] = None
) -> LLMAgent:
    """
    创建 LLM Agent
    
    Args:
        name: Agent 名称
        system_prompt: 系统提示词
        agent_func: 原有 Agent 函数
        llm_provider: 强制使用某个 LLM 提供商
        
    Returns:
        LLMAgent 实例
    """
    return LLMAgent(name, system_prompt, agent_func, llm_provider)


# ========== 示例：创建 LLM 驱动的 Agent ==========

def get_ceo_llm_agent() -> LLMAgent:
    """获取 CEO LLM Agent"""
    return create_llm_agent(
        name="ceo",
        system_prompt="""你是 AI 学习团队的 CEO，负责整体调度和决策。
你擅长分析任务需求，选择合适的 Agent 来处理。
团队成员：
- planner: 制定计划
- researcher: 调研信息
- engineer: 编写代码
- reviewer: 审查质量
- analyst: 分析数据

根据用户需求，选择合适的 Agent 来处理。""",
        llm_provider="ollama"  # 简单任务用本地
    )


def get_engineer_llm_agent() -> LLMAgent:
    """获取 Engineer LLM Agent"""
    return create_llm_agent(
        name="engineer",
        system_prompt="""你是 AI 学习团队的 Engineer，负责编写代码。
你擅长 Python、JavaScript、Shell 等编程语言。
根据用户需求，编写高质量、可运行的代码。""",
        llm_provider="ollama"
    )
