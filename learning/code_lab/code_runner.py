#!/usr/bin/env python3
"""
Code Runner - 代码运行器
"""
import subprocess
import tempfile
import os
from typing import Dict, List
from sandbox import get_sandbox


class CodeRunner:
    """代码运行器"""
    
    def __init__(self):
        self.sandbox = get_sandbox()
        self.history = []
    
    def run(self, code: str, language: str = "python") -> Dict:
        """运行代码"""
        
        result = self.sandbox.run(code, language)
        
        # 记录历史
        self.history.append({
            "code": code[:100],
            "result": result,
            "success": result.get("success", False)
        })
        
        return result
    
    def run_test(self, code: str, expected: str) -> Dict:
        """运行测试"""
        
        result = self.run(code)
        
        success = result.get("success", False)
        output = result.get("output", "").strip()
        
        passed = success and output == expected.strip()
        
        return {
            "passed": passed,
            "expected": expected,
            "actual": output,
            "result": result
        }
    
    def run_multiple(self, tests: List[Dict]) -> Dict:
        """运行多个测试"""
        
        results = []
        passed = 0
        
        for test in tests:
            code = test.get("code", "")
            expected = test.get("expected", "")
            
            result = self.run_test(code, expected)
            
            if result["passed"]:
                passed += 1
            
            results.append(result)
        
        return {
            "total": len(tests),
            "passed": passed,
            "failed": len(tests) - passed,
            "results": results
        }
    
    def get_history(self, n: int = 10) -> List:
        """获取历史"""
        return self.history[-n:]


_runner = None

def get_code_runner() -> CodeRunner:
    global _runner
    if _runner is None:
        _runner = CodeRunner()
    return _runner


# 便捷函数
def run(code: str) -> Dict:
    return get_code_runner().run(code)


# 测试
if __name__ == "__main__":
    runner = get_code_runner()
    
    print("=== 代码运行器测试 ===\n")
    
    # 测试
    result = runner.run("print('Hello')\nprint(2*3)")
    print(f"成功: {result['success']}")
    print(f"输出: {result['output']}")
