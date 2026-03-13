#!/usr/bin/env python3
"""
Reviewer Agent - 审查代理
"""
from typing import Dict


class ReviewerAgent:
    """代码审查代理"""
    
    def review(self, code: str) -> Dict:
        """审查代码"""
        
        issues = []
        
        # 简单检查
        if len(code) > 200:
            issues.append("代码过长，建议拆分")
        
        if "var" in code.lower():
            issues.append("建议使用snake_case命名")
        
        if "print(" in code and code.count("print(") > 3:
            issues.append("注意调试代码")
        
        return {
            "score": max(0, 100 - len(issues) * 20),
            "issues": issues if issues else ["代码良好"],
            "grade": "A" if len(issues) < 2 else "B"
        }


_agent = None

def get_reviewer_agent():
    global _agent
    if _agent is None:
        _agent = ReviewerAgent()
    return _agent
