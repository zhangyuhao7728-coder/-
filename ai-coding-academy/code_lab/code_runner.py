#!/usr/bin/env python3
"""
代码运行器 - 支持多语言
"""
import subprocess
import tempfile
import os
import shutil
from typing import Dict, Optional


class CodeRunner:
    """代码运行器"""
    
    def __init__(self):
        self.timeout = 30  # 默认超时30秒
        self.supported_languages = ["python", "javascript", "bash"]
    
    def run_python(self, code: str, timeout: int = None) -> Dict:
        """运行Python代码"""
        
        timeout = timeout or self.timeout
        
        # 安全检查
        if self._is_dangerous(code):
            return {
                "success": False,
                "output": "",
                "error": "代码包含危险操作",
                "language": "python"
            }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            os.unlink(temp_file)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "language": "python"
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "代码执行超时",
                "language": "python"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "language": "python"
            }
    
    def run_javascript(self, code: str, timeout: int = None) -> Dict:
        """运行JavaScript代码"""
        
        timeout = timeout or self.timeout
        
        # 检查Node.js
        if not shutil.which("node"):
            return {
                "success": False,
                "output": "",
                "error": "Node.js未安装",
                "language": "javascript"
            }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            os.unlink(temp_file)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else "",
                "language": "javascript"
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "language": "javascript"
            }
    
    def run_bash(self, code: str, timeout: int = None) -> Dict:
        """运行Bash脚本"""
        
        timeout = timeout or self.timeout
        
        try:
            result = subprocess.run(
                code,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else "",
                "language": "bash"
            }
            
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "language": "bash"
            }
    
    def run(self, code: str, language: str = "python", timeout: int = None) -> Dict:
        """运行代码"""
        
        if language == "python":
            return self.run_python(code, timeout)
        elif language == "javascript":
            return self.run_javascript(code, timeout)
        elif language == "bash":
            return self.run_bash(code, timeout)
        else:
            return {
                "success": False,
                "output": "",
                "error": f"不支持的语言: {language}",
                "language": language
            }
    
    def _is_dangerous(self, code: str) -> bool:
        """检查危险操作"""
        
        dangerous = [
            "import os",
            "import sys",
            "import subprocess",
            "import socket",
            "import requests",
            "__import__",
            "eval(",
            "exec(",
            "open(",
            "write(",
        ]
        
        code_lower = code.lower()
        for d in dangerous:
            if d.lower() in code_lower:
                return True
        
        return False


# 全局实例
_runner = None

def get_code_runner() -> CodeRunner:
    global _runner
    if _runner is None:
        _runner = CodeRunner()
    return _runner

# 便捷函数
def run_python(code: str, timeout: int = None) -> Dict:
    return get_code_runner().run_python(code, timeout)

def run_code(code: str, language: str = "python") -> Dict:
    return get_code_runner().run(code, language)


if __name__ == "__main__":
    # 测试
    runner = get_code_runner()
    
    print("=== 代码运行器测试 ===\n")
    
    # Python测试
    result = runner.run_python("print('Hello, Python!')")
    print(f"Python: {result['success']} - {result['output']}")
    
    # JavaScript测试
    result = runner.run_javascript("console.log('Hello, JS!');")
    print(f"JavaScript: {result['success']} - {result['output']}")
