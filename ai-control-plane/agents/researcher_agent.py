#!/usr/bin/env python3
"""
Researcher Agent - 研究Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """Researcher Agent - 研究者"""
    
    def __init__(self, router=None):
        super().__init__("Researcher", "研究者", "qwen2.5:14b")
        self.router = router
    
    def research(self, topic: str) -> str:
        """研究"""
        self.tasks_completed += 1
        return f"[Researcher] 调研: 正在收集{topic}相关信息"
    
    def search(self, query: str) -> str:
        """搜索"""
        return f"[Researcher] 搜索: {query}"


# 全局实例
_researcher = None

def get_researcher_agent(router=None) -> ResearcherAgent:
    global _researcher
    if _researcher is None:
        _researcher = ResearcherAgent(router)
    return _researcher
