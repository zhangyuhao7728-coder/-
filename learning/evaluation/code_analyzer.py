#!/usr/bin/env python3
"""
Code Analyzer - 代码分析器
分析代码结构、函数设计、复杂度
"""
import ast
import re
from typing import Dict, List


class CodeAnalyzer:
    """代码分析器"""
    
    def __init__(self):
        self.issues = []
    
    # ===== 1. 解析代码结构 =====
    
    def analyze_structure(self, code: str) -> Dict:
        """分析代码结构"""
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e)
            }
        
        functions = []
        classes = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": ast.unparse(node.returns) if node.returns else None
                })
            elif isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": methods
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        return {
            "valid": True,
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(code.split("\n"))
        }
    
    # ===== 2. 检查函数设计 =====
    
    def check_functions(self, code: str) -> List[str]:
        """检查函数设计问题"""
        issues = []
        
        # 函数太长
        functions = re.findall(r'def (\w+)\([^)]*\):', code)
        
        # 简单检查
        lines = code.split("\n")
        
        for func in functions:
            # 查找函数开始
            for i, line in enumerate(lines):
                if f"def {func}" in line:
                    # 统计函数行数
                    func_lines = 0
                    for j in range(i+1, len(lines)):
                        if lines[j].strip() and not lines[j].startswith(" "):
                            break
                        if lines[j].strip():
                            func_lines += 1
                    
                    if func_lines > 50:
                        issues.append(f"函数 {func} 太长 ({func_lines}行)，建议拆分")
                    break
        
        # 检查变量命名
        if "var" in code.lower() or "Var" in code:
            issues.append("建议使用 snake_case 命名: var_name")
        
        if "def " in code and "self" not in code and "class" not in code:
            # 非类方法使用下划线命名
            pass
        
        return issues
    
    # ===== 3. 复杂度分析 =====
    
    def analyze_complexity(self, code: str) -> Dict:
        """分析代码复杂度"""
        
        complexity = 1  # 基础复杂度
        
        # 计算分支
        complexity += code.count("if ")
        complexity += code.count("elif ")
        complexity += code.count("else:")
        
        # 循环
        complexity += code.count("for ")
        complexity += code.count("while ")
        
        # 异常
        complexity += code.count("except")
        
        # 逻辑运算符
        complexity += code.count(" and ")
        complexity += code.count(" or ")
        
        # 评估级别
        if complexity <= 5:
            level = "简单"
        elif complexity <= 10:
            level = "中等"
        elif complexity <= 20:
            level = "复杂"
        else:
            level = "非常复杂"
        
        return {
            "score": complexity,
            "level": level,
            "branches": code.count("if ") + code.count("elif "),
            "loops": code.count("for ") + code.count("while "),
            "suggestion": self._get_suggestion(complexity)
        }
    
    def _get_suggestion(self, complexity: int) -> str:
        if complexity <= 5:
            return "代码复杂度良好"
        elif complexity <= 10:
            return "建议拆分函数以提高可读性"
        elif complexity <= 20:
            return "建议重构，考虑使用辅助函数"
        else:
            return "代码过于复杂，建议大幅重构"
    
    # ===== 4. 完整分析 =====
    
    def analyze(self, code: str) -> Dict:
        """完整分析"""
        
        # 结构
        structure = self.analyze_structure(code)
        
        # 函数检查
        issues = self.check_functions(code)
        
        # 复杂度
        complexity = self.analyze_complexity(code)
        
        return {
            "structure": structure,
            "issues": issues,
            "complexity": complexity,
            "score": self._calculate_score(complexity, issues)
        }
    
    def _calculate_score(self, complexity: Dict, issues: List) -> int:
        score = 100
        
        # 扣分
        score -= min(30, complexity.get("score", 0) * 2)
        score -= len(issues) * 10
        
        return max(0, score)
    
    # ===== 5. 评分 =====
    
    def get_grade(self, score: int) -> str:
        if score >= 90:
            return "A - 优秀"
        elif score >= 80:
            return "B - 良好"
        elif score >= 70:
            return "C - 及格"
        elif score >= 60:
            return "D - 需改进"
        else:
            return "F - 不及格"


# 全局实例
_analyzer = None

def get_code_analyzer() -> CodeAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = CodeAnalyzer()
    return _analyzer

def analyze_code(code: str) -> Dict:
    return get_code_analyzer().analyze(code)


# 测试
if __name__ == "__main__":
    analyzer = get_code_analyzer()
    
    code = """
def hello():
    print("Hello")
    for i in range(10):
        if i > 5:
            print(i)
"""
    
    print("=== 代码分析 ===\n")
    
    result = analyzer.analyze(code)
    
    print("结构:")
    s = result["structure"]
    print(f"  函数: {len(s.get('functions', []))}")
    print(f"  类: {len(s.get('classes', []))}")
    print(f"  行数: {s.get('lines', 0)}")
    
    print("\n复杂度:")
    c = result["complexity"]
    print(f"  分数: {c['score']}")
    print(f"  级别: {c['level']}")
    
    print("\n问题:")
    for issue in result["issues"]:
        print(f"  - {issue}")
    
    print(f"\n总评: {analyzer.get_grade(result['score'])}")
