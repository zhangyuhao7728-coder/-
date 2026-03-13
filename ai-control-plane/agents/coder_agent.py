#!/usr/bin/env python3
"""
Coder Agent - 编码Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class CoderAgent(BaseAgent):
    """Coder Agent - 编码者"""
    
    def __init__(self, router=None):
        super().__init__("Coder", "编码者", "deepseek-coder:6.7b")
        self.router = router
    
    def code(self, task: str) -> str:
        """编写代码"""
        self.tasks_completed += 1
        
        if "python" in task.lower():
            return f"[Coder] 编写Python代码: {task}"
        elif "web" in task.lower():
            return f"[Coder] 编写Web代码: {task}"
        else:
            return f"[Coder] 编写代码: {task}"
    
    def review_code(self, code: str) -> str:
        """代码审查"""
        issues = []
        
        if "def " not in code and "class " not in code:
            issues.append("缺少函数定义")
        
        if len(code) < 10:
            issues.append("代码过短")
        
        if issues:
            return f"[Coder] 建议改进: {', '.join(issues)}"
        return "[Coder] 代码审查通过"


# 全局实例
_coder = None

def get_coder_agent(router=None) -> CoderAgent:
    global _coder
    if _coder is None:
        _coder = CoderAgent(router)
    return _coder
