#!/usr/bin/env python3
"""
🎯 自动代码评测系统
运行测试并输出详细结果
"""

import json
import subprocess
import sys
import time
from pathlib import Path
import re

class CodeEvaluator:
    def __init__(self, problem_dir=None):
        self.base_dir = Path("~/项目/Ai学习系统/learning").expanduser()
        self.problem_dir = Path(problem_dir) if problem_dir else self.base_dir / "problems"
        self.results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "time_complexity": "O(?)",
            "memory_complexity": "O(?)",
            "code_quality": 0,
            "details": []
        }
    
    def analyze_complexity(self, code):
        """分析代码复杂度"""
        # 简单的时间复杂度分析
        time_complexity = "O(n)"
        memory_complexity = "O(n)"
        
        # 检测嵌套循环
        if code.count("for") >= 2 or code.count("while") >= 2:
            time_complexity = "O(n²)"
        
        # 检测递归
        if "def " in code and code.count("return") > 1:
            if "fib" in code.lower() or "factorial" in code.lower():
                time_complexity = "O(2^n)"
        
        # 检测字典/集合使用
        if "dict()" in code or "{}" in code or "set()" in code:
            memory_complexity = "O(n)"
        else:
            memory_complexity = "O(1)"
        
        return time_complexity, memory_complexity
    
    def analyze_code_quality(self, code):
        """分析代码质量"""
        score = 10.0
        
        # 缺少文档字符串 -0.5
        if '"""' not in code and "'''" not in code:
            score -= 0.5
        
        # 变量命名不规范 -1.0
        bad_names = ['a', 'b', 'c', 'd', 'x', 'y', 'z']
        for name in bad_names:
            if re.search(rf'\b{name}\b', code) and len(code) > 200:
                score -= 0.3
        
        # 缺少类型注解 -0.5
        if ":" not in code or "->" not in code:
            score -= 0.3
        
        # 代码过长 -0.5
        if len(code.split('\n')) > 50:
            score -= 0.5
        
        # 有try-except + finally + else - 好习惯 +0.5
        if "try:" in code and "except" in code:
            score += 0.3
        
        return max(0, min(10, score))
    
    def run_test(self, code, test_input, expected_output):
        """运行单个测试"""
        # 创建临时文件
        temp_file = "/tmp/test_code.py"
        
        # 组合代码
        full_code = code
        if test_input:
            full_code += f"\n\n# Test\nprint({test_input})"
        
        with open(temp_file, "w") as f:
            f.write(full_code)
        
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                timeout=5,
                text=True
            )
            elapsed = time.time() - start_time
            
            actual = result.stdout.strip()
            
            # 处理输出格式
            if isinstance(expected_output, str):
                expected = expected_output.strip()
            elif isinstance(expected_output, list):
                expected = str(expected_output).strip()
            else:
                expected = str(expected_output).strip()
            
            passed = actual == expected
            
            return {
                "passed": passed,
                "input": test_input,
                "expected": expected,
                "actual": actual,
                "time": f"{elapsed:.3f}s"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "input": test_input,
                "expected": expected_output,
                "actual": "Time Limit Exceeded",
                "time": "5.000s"
            }
        except Exception as e:
            return {
                "passed": False,
                "input": test_input,
                "expected": expected_output,
                "actual": f"Error: {str(e)}",
                "time": "0.000s"
            }
    
    def evaluate(self, code, test_cases):
        """评估代码"""
        self.results["total"] = len(test_cases)
        
        for case in test_cases:
            input_data = case.get("input", "")
            expected = case.get("output", "")
            
            result = self.run_test(code, input_data, expected)
            self.results["details"].append(result)
            
            if result["passed"]:
                self.results["passed"] += 1
            else:
                self.results["failed"] += 1
        
        # 分析复杂度和质量
        self.results["time_complexity"], self.results["memory_complexity"] = self.analyze_complexity(code)
        self.results["code_quality"] = self.analyze_code_quality(code)
        
        return self.results
    
    def print_results(self):
        """打印结果"""
        r = self.results
        
        print("=" * 50)
        print("🎯 Test Results")
        print("=" * 50)
        
        # 通过率
        passed = r["passed"]
        total = r["total"]
        percentage = (passed / total * 100) if total > 0 else 0
        
        status = "✅ PASSED" if passed == total else "⚠️ PARTIAL" if passed > 0 else "❌ FAILED"
        print(f"\n{status} | Passed: {passed}/{total} ({percentage:.0f}%)")
        
        # 复杂度分析
        print(f"\n📊 Complexity Analysis:")
        print(f"  Time Complexity:   {r['time_complexity']}")
        print(f"  Memory Usage:     {r['memory_complexity']}")
        
        # 代码质量
        quality = r["code_quality"]
        quality_emoji = "⭐" * int(quality // 2)
        print(f"\n📝 Code Quality:    {quality:.1f}/10 {quality_emoji}")
        
        # 失败的测试
        if r["failed"] > 0:
            print(f"\n❌ Failed Tests:")
            for i, detail in enumerate(r["details"], 1):
                if not detail["passed"]:
                    print(f"  Test {i}: {detail['input']}")
                    print(f"    Expected: {detail['expected']}")
                    print(f"    Got:      {detail['actual']}")
        
        print("\n" + "=" * 50)
        
        return r

def main():
    # 示例代码和测试
    sample_code = '''
def two_sum(nums, target):
    """
    两数之和 - 哈希表解法
    时间复杂度: O(n)
    空间复杂度: O(n)
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
'''
    
    test_cases = [
        {"input": "two_sum([2,7,11,15], 9)", "output": "[0, 1]"},
        {"input": "two_sum([3,2,4], 6)", "output": "[1, 2]"},
        {"input": "two_sum([3,3], 6)", "output": "[0, 1]"},
    ]
    
    # 评测
    evaluator = CodeEvaluator()
    results = evaluator.evaluate(sample_code, test_cases)
    evaluator.print_results()

if __name__ == "__main__":
    # 如果传入代码文件
    if len(sys.argv) > 1:
        code_file = sys.argv[1]
        with open(code_file) as f:
            code = f.read()
        
        # 尝试加载测试用例
        test_file = code_file.replace(".py", "_test.json")
        if Path(test_file).exists():
            with open(test_file) as f:
                tests = json.load(f)
        else:
            tests = [{"input": "", "output": ""}]
        
        evaluator = CodeEvaluator()
        evaluator.evaluate(code, tests)
        evaluator.print_results()
    else:
        main()
