#!/usr/bin/env python3
"""
Code Quality Checker - 代码质量检查
"""
import re
from typing import Dict, List


class CodeQualityChecker:
    """代码质量检查"""
    
    def check(self, code: str) -> Dict:
        """检查代码质量"""
        
        issues = []
        score = 100
        
        # 检查函数长度
        functions = re.findall(r'def (\w+)\([^)]*\):', code)
        lines = len(code.split('\n'))
        
        if lines > 200:
            issues.append({"type": "length", "msg": f"代码过长({lines}行)，建议拆分"})
            score -= 15
        
        # 检查变量命名
        if re.search(r'\bvar\b|\bVar\b', code):
            issues.append({"type": "naming", "msg": "建议使用snake_case命名"})
            score -= 5
        
        # 检查硬编码
        if re.search(r'\d{3,}', code):
            issues.append({"type": "magic", "msg": "避免硬编码数字"})
            score -= 5
        
        # 检查注释
        if '#' not in code and lines > 50:
            issues.append({"type": "comment", "msg": "建议添加注释"})
            score -= 10
        
        # 检查错误处理
        if 'try:' not in code and 'open(' in code:
            issues.append({"type": "error", "msg": "建议添加异常处理"})
            score -= 10
        
        return {
            "score": max(0, score),
            "issues": issues,
            "grade": self._get_grade(score)
        }
    
    def _get_grade(self, score):
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        return "D"


_checker = None

def get_code_quality_checker():
    global _checker
    if _checker is None:
        _checker = CodeQualityChecker()
    return _checker
