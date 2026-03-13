#!/usr/bin/env python3
"""
Code Reviewer - 代码审查
"""


class CodeReviewer:
    """代码审查"""
    
    def review(self, code: str) -> dict:
        issues = []
        score = 100
        
        # 检查缩进
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            if line and not line.startswith(" ") and not line.startswith("\t"):
                if i > 1 and lines[i-2].strip():
                    issues.append({"line": i, "type": "indent", "msg": "缩进不一致"})
                    score -= 5
        
        # 检查变量命名
        if "var" in code.lower() or "Var" in code:
            issues.append({"line": 0, "type": "naming", "msg": "建议使用snake_case命名"})
            score -= 5
        
        # 检查print调试
        if "print(" in code:
            count = code.count("print(")
            if count > 3:
                issues.append({"line": 0, "type": "debug", "msg": f"有{count}个print，建议删除调试代码"})
                score -= 10
        
        # 检查硬编码
        if "100" in code and "/" in code:
            issues.append({"line": 0, "type": "magic", "msg": "避免硬编码数字，建议用常量"})
        
        # 检查注释
        if "#" not in code and len(code) > 100:
            issues.append({"line": 0, "type": "comment", "msg": "建议添加注释"})
        
        return {
            "score": max(0, score),
            "issues": issues,
            "grade": self._get_grade(score)
        }
    
    def _get_grade(self, score):
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"


_reviewer = None

def get_code_reviewer():
    global _reviewer
    if _reviewer is None:
        _reviewer = CodeReviewer()
    return _reviewer
