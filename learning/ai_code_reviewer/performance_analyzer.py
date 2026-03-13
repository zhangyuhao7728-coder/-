#!/usr/bin/env python3
"""
Performance Analyzer - 性能分析
"""
import re
from typing import Dict, List


class PerformanceAnalyzer:
    """性能分析"""
    
    def analyze(self, code: str) -> Dict:
        """分析性能"""
        
        issues = []
        
        # 检查循环嵌套
        nested_loops = len(re.findall(r'for .+ in .+:', code))
        if nested_loops > 2:
            issues.append("注意循环嵌套可能影响性能")
        
        # 检查重复计算
        if code.count('len(') > 5:
            issues.append("考虑缓存len()结果")
        
        # 检查字符串拼接
        if '+' in code and 'str' in code:
            issues.append("建议使用join()代替字符串+拼接")
        
        # 检查列表推导式
        if 'for' in code and 'if' in code and '[' not in code.split('for')[0]:
            pass  # 可能是列表推导式
        
        return {
            "issues": issues if issues else ["性能良好"],
            "suggestions": self._get_suggestions(issues)
        }
    
    def _get_suggestions(self, issues: List) -> List[str]:
        suggestions = [
            "使用生成器代替列表",
            "避免重复计算",
            "使用缓存",
            "批量操作代替循环"
        ]
        return suggestions[:2] if issues else []


_analyzer = None

def get_performance_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = PerformanceAnalyzer()
    return _analyzer
