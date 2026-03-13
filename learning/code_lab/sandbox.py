#!/usr/bin/env python3
"""
Sandbox - 安全沙盒
"""
import subprocess
import tempfile
import os
from typing import Dict


class Sandbox:
    """安全代码运行环境"""
    
    def __init__(self):
        self.timeout = 5  # 超时秒数
        self.max_output = 10000  # 最大输出
    
    def run(self, code: str, language: str = "python") -> Dict:
        """运行代码"""
        
        if language == "python":
            return self._run_python(code)
        
        return {"success": False, "error": "不支持的语言"}
    
    def _run_python(self, code: str) -> Dict:
        """运行Python代码"""
        
        # 安全检查
        if self._is_dangerous(code):
            return {
                "success": False,
                "error": "代码包含危险操作",
                "output": ""
            }
        
        try:
            # 写入临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # 运行
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            # 清理
            os.unlink(temp_file)
            
            # 返回结果
            output = result.stdout[:self.max_output]
            error = result.stderr[:self.max_output]
            
            return {
                "success": result.returncode == 0,
                "output": output,
                "error": error,
                "returncode": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "代码执行超时", "output": ""}
        except Exception as e:
            return {"success": False, "error": str(e), "output": ""}
    
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
            "delete",
            "rm ",
            "format",
        ]
        
        code_lower = code.lower()
        for d in dangerous:
            if d.lower() in code_lower:
                return True
        
        return False


_sandbox = None

def get_sandbox() -> Sandbox:
    global _sandbox
    if _sandbox is None:
        _sandbox = Sandbox()
    return _sandbox


# 测试
if __name__ == "__main__":
    sb = get_sandbox()
    
    print("=== 沙盒测试 ===\n")
    
    # 测试正常代码
    result = sb.run("print('Hello World')\nprint(1+2)")
    print(f"结果: {result['success']}")
    print(f"输出: {result['output']}")
