#!/usr/bin/env python3
"""
Sandbox - 沙盒环境
功能：提供安全的代码执行环境
"""
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any


class Sandbox:
    """沙盒环境"""
    
    # 允许的危险操作
    ALLOWED_OPERATIONS = [
        'read_file',
        'write_file', 
        'list_dir',
        'network_request',
    ]
    
    # 禁止的操作
    FORBIDDEN_OPERATIONS = [
        'execute_shell',
        'delete_file',
        'modify_system',
        'access_sensitive',
    ]
    
    def __init__(self, workspace: str = None):
        """
        初始化沙盒
        
        Args:
            workspace: 工作目录
        """
        if workspace is None:
            workspace = Path(__file__).parent.parent / 'sandbox'
        
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        self.allowed_dirs = [self.workspace]
        self.blocked = True  # 默认阻止
    
    def _is_safe_path(self, path: str) -> bool:
        """检查路径是否安全"""
        try:
            abs_path = Path(path).resolve()
            # 必须在允许目录内
            for allowed in self.allowed_dirs:
                if str(abs_path).startswith(str(allowed.resolve())):
                    return True
            return False
        except:
            return False
    
    def read_file(self, filepath: str, max_size: int = 1024 * 1024) -> Optional[str]:
        """
        安全读取文件
        
        Args:
            filepath: 文件路径
            max_size: 最大读取大小 (1MB)
            
        Returns:
            文件内容
        """
        if not self._is_safe_path(filepath):
            raise PermissionError(f"路径不安全: {filepath}")
        
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        # 检查大小
        if path.stat().st_size > max_size:
            raise ValueError(f"文件过大: {path.stat().st_size} > {max_size}")
        
        # 禁止读取敏感文件
        forbidden = ['.env', '.key', '.pem', 'id_rsa', 'id_ed25519']
        if any(f in str(path) for f in forbidden):
            raise PermissionError(f"禁止读取敏感文件: {filepath}")
        
        return path.read_text(encoding='utf-8')
    
    def write_file(self, filepath: str, content: str) -> bool:
        """
        安全写入文件
        
        Args:
            filepath: 文件路径
            content: 文件内容
        """
        if not self._is_safe_path(filepath):
            raise PermissionError(f"路径不安全: {filepath}")
        
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        
        return True
    
    def list_directory(self, directory: str) -> list:
        """
        列出目录内容
        
        Args:
            directory: 目录路径
        """
        if not self._is_safe_path(directory):
            raise PermissionError(f"路径不安全: {directory}")
        
        path = Path(directory)
        if not path.is_dir():
            raise NotADirectoryError(f"不是目录: {directory}")
        
        return [str(p) for p in path.iterdir()]
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        执行命令 (受限)
        
        Args:
            command: 命令
            timeout: 超时时间
        """
        # 检查危险命令
        dangerous = ['rm -rf', 'dd if=', 'mkfs', ':(){:|:', '> /dev/']
        if any(d in command for d in dangerous):
            raise PermissionError(f"禁止执行危险命令: {command}")
        
        # 限制命令
        allowed_commands = ['ls', 'cat', 'echo', 'grep', 'find', 'python', 'python3']
        cmd_first = command.split()[0] if command else ''
        if cmd_first not in allowed_commands:
            raise PermissionError(f"命令不允许: {cmd_first}")
        
        # 执行
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout[:10000],
                'stderr': result.stderr[:1000],
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"命令执行超时: {timeout}秒")
    
    def create_workspace(self, name: str) -> str:
        """
        创建临时工作区
        
        Args:
            name: 工作区名称
            
        Returns:
            工作区路径
        """
        workspace = self.workspace / name
        workspace.mkdir(parents=True, exist_ok=True)
        return str(workspace)
    
    def cleanup(self, name: str = None):
        """
        清理工作区
        
        Args:
            name: 工作区名称，为空则清理所有
        """
        if name:
            workspace = self.workspace / name
            if workspace.exists():
                shutil.rmtree(workspace)
        else:
            # 清理所有临时文件
            for item in self.workspace.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                elif item.suffix in ['.tmp', '.log', '.cache']:
                    item.unlink()


# 全局实例
_sandbox = None

def get_sandbox() -> Sandbox:
    """获取沙盒实例"""
    global _sandbox
    if _sandbox is None:
        _sandbox = Sandbox()
    return _sandbox


# 便捷函数
def safe_read(filepath: str, max_size: int = 1024 * 1024) -> str:
    return get_sandbox().read_file(filepath, max_size)

def safe_write(filepath: str, content: str) -> bool:
    return get_sandbox().write_file(filepath, content)

def safe_list(directory: str) -> list:
    return get_sandbox().list_directory(directory)

def safe_exec(command: str, timeout: int = 30) -> Dict[str, Any]:
    return get_sandbox().execute_command(command, timeout)


# 测试
if __name__ == "__main__":
    sandbox = get_sandbox()
    
    print("=== 沙盒测试 ===")
    
    # 测试创建工作区
    ws = sandbox.create_workspace('test')
    print(f"✅ 创建工作区: {ws}")
    
    # 测试写入
    test_file = ws + '/test.txt'
    sandbox.write_file(test_file, 'Hello Sandbox!')
    print(f"✅ 写入文件: {test_file}")
    
    # 测试读取
    content = sandbox.read_file(test_file)
    print(f"✅ 读取内容: {content}")
    
    # 测试列出目录
    files = sandbox.list_directory(ws)
    print(f"✅ 目录内容: {files}")
    
    # 测试命令执行
    result = sandbox.execute_command('echo "test"')
    print(f"✅ 命令结果: {result}")
    
    # 清理
    sandbox.cleanup('test')
    print("✅ 清理完成")
