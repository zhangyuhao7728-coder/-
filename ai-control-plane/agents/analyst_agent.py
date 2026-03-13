#!/usr/bin/env python3
"""
Analyst Agent - 分析Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class AnalystAgent(BaseAgent):
    """Analyst Agent - 分析师"""
    
    def __init__(self, router=None):
        super().__init__("Analyst", "分析师", "qwen2.5:14b")
        self.router = router
    
    def analyze(self, data: str) -> str:
        """分析"""
        self.tasks_completed += 1
        
        # 简单分析
        length = len(data)
        
        return f"[Analyst] 分析完成: 数据长度{length}字符"


# 全局实例
_analyst = None

def get_analyst_agent(router=None) -> AnalystAgent:
    global _analyst
    if _analyst is None:
        _analyst = AnalystAgent(router)
    return _analyst
