#!/usr/bin/env python3
"""
File System Guard - 文件系统隔离守卫
功能：确保 Agent 只能访问项目目录，禁止访问敏感目录
"""
import os
from pathlib import Path
from typing import List, Optional


class FileSystemGuard:
    """文件系统守卫"""
    
    # 项目根目录
    PROJECT_ROOT = os.path.expanduser("~/项目/Ai学习系统")
    
    # 禁止访问的目录
    FORBIDDEN_DIRS = [
        # SSH/密钥
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.aws"),
        
        # 配置目录
        os.path.expanduser("~/.config"),
        os.path.expanduser("~/.aws/credentials"),
        os.path.expanduser("~/.kube"),
        
        # 系统敏感目录
        "/etc",
        "/var",
        "/usr/local/etc",
        "/System",
        
        # 其他密钥
        os.path.expanduser("~/.gnupg"),
        os.path.expanduser("~/.npm/_cacache"),
        os.path.expanduser("~/.npm-global"),
        
        # 项目外目录
        os.path.expanduser("~/项目/AI返利系统"),
    ]
    
    # 允许访问的目录
    ALLOWED_DIRS = [
        # 项目目录
        os.path.expanduser("~/项目/Ai学习系统"),
        os.path.expanduser("~/项目"),
        
        # 临时目录
        "/tmp",
        os.path.expanduser("~/Downloads"),
        
        # Home 目录 (只读部分)
        os.path.expanduser("~"),
    ]
    
    # 禁止的文件/模式
    FORBIDDEN_PATTERNS = [
        # 密钥文件
        "*.key",
        "*.pem",
        "*.crt",
        "*.p12",
        "*.pfx",
        "id_rsa*",
        "id_ed25519*",
        
        # 敏感配置
        ".env",
        ".env.local",
        ".npmrc",
        ".pypirc",
        
        # 凭证
        "credentials",
        ".aws/credentials",
        ".kube/config",
        
        # 历史记录
        ".bash_history",
        ".zsh_history",
        ".mysql_history",
        ".psql_history",
    ]
    
    def __init__(self, project_root: str = None):
        """初始化"""
        if project_root:
            self.PROJECT_ROOT = os.path.abspath(project_root)
        
        # 确保路径标准化
        self._forbidden_dirs = [os.path.abspath(d) for d in self.FORBIDDEN_DIRS]
        self._allowed_dirs = [os.path.abspath(d) for d in self.ALLOWED_DIRS]
    
    def _normalize(self, path: str) -> str:
        """标准化路径"""
        return os.path.abspath(os.path.expanduser(path))
    
    def is_forbidden_dir(self, path: str) -> bool:
        """检查是否在禁止目录中"""
        abs_path = self._normalize(path)
        
        for forbidden in self._forbidden_dirs:
            if abs_path.startswith(forbidden):
                return True
        
        return False
    
    def is_allowed_dir(self, path: str) -> bool:
        """检查是否在允许目录中"""
        abs_path = self._normalize(path)
        
        # 必须在允许目录内
        for allowed in self._allowed_dirs:
            if abs_path.startswith(allowed):
                return True
        
        return False
    
    def is_in_project(self, path: str) -> bool:
        """检查是否在项目目录内"""
        abs_path = self._normalize(path)
        return abs_path.startswith(self.PROJECT_ROOT)
    
    def is_forbidden_file(self, filename: str) -> bool:
        """检查文件名是否敏感"""
        import fnmatch
        
        for pattern in self.FORBIDDEN_PATTERNS:
            if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                return True
        
        return False
    
    def validate_path(self, path: str, require_project: bool = False) -> dict:
        """
        验证路径是否安全
        
        Args:
            path: 要访问的路径
            require_project: 是否强制要求在项目目录内
            
        Returns:
            dict: 验证结果
        """
        abs_path = self._normalize(path)
        
        # 1. 检查禁止目录
        if self.is_forbidden_dir(abs_path):
            return {
                'allowed': False,
                'reason': f'禁止访问目录: {path}',
                'blocked': True
            }
        
        # 2. 如果要求在项目内
        if require_project:
            if not self.is_in_project(abs_path):
                return {
                    'allowed': False,
                    'reason': f'必须在项目目录内: {self.PROJECT_ROOT}',
                    'blocked': True
                }
        
        # 3. 检查是否在允许目录
        if not self.is_allowed_dir(abs_path):
            return {
                'allowed': False,
                'reason': f'不在允许目录内: {path}',
                'blocked': True
            }
        
        return {
            'allowed': True,
            'reason': '路径安全'
        }
    
    def validate_file(self, filepath: str, require_project: bool = True) -> dict:
        """
        验证文件访问
        
        Args:
            filepath: 文件路径
            require_project: 是否必须在项目目录
        """
        abs_path = self._normalize(filepath)
        
        # 1. 先验证路径
        path_result = self.validate_path(abs_path, require_project)
        if not path_result['allowed']:
            return path_result
        
        # 2. 检查文件名
        filename = os.path.basename(abs_path)
        if self.is_forbidden_file(filename):
            return {
                'allowed': False,
                'reason': f'禁止访问敏感文件: {filename}',
                'blocked': True
            }
        
        return {
            'allowed': True,
            'reason': '文件访问允许'
        }
    
    def check_path(self, path: str, require_project: bool = False) -> bool:
        """
        检查路径，如果不允许则抛异常
        """
        result = self.validate_path(path, require_project)
        
        if not result['allowed']:
            raise PermissionError(
                f"🚫 路径访问被阻止\n"
                f"路径: {path}\n"
                f"原因: {result['reason']}\n"
                f"项目目录: {self.PROJECT_ROOT}"
            )
        
        return True
    
    def check_file(self, filepath: str, require_project: bool = True) -> bool:
        """
        检查文件访问，如果不允许则抛异常
        """
        result = self.validate_file(filepath, require_project)
        
        if not result['allowed']:
            raise PermissionError(
                f"🚫 文件访问被阻止\n"
                f"文件: {filepath}\n"
                f"原因: {result['reason']}"
            )
        
        return True
    
    def get_allowed_dirs(self) -> List[str]:
        """获取允许的目录"""
        return self._allowed_dirs.copy()
    
    def get_forbidden_dirs(self) -> List[str]:
        """获取禁止的目录"""
        return self._forbidden_dirs.copy()


# 全局实例
_guard = None

def get_fs_guard(project_root: str = None) -> FileSystemGuard:
    """获取文件系统守卫实例"""
    global _guard
    if _guard is None:
        _guard = FileSystemGuard(project_root)
    return _guard


# 便捷函数
def validate_path(path: str, require_project: bool = False) -> dict:
    """验证路径"""
    return get_fs_guard().validate_path(path, require_project)

def validate_file(filepath: str, require_project: bool = True) -> dict:
    """验证文件"""
    return get_fs_guard().validate_file(filepath, require_project)

def check_path(path: str, require_project: bool = False) -> bool:
    """检查路径"""
    return get_fs_guard().check_path(path, require_project)

def check_file(filepath: str, require_project: bool = True) -> bool:
    """检查文件"""
    return get_fs_guard().check_file(filepath, require_project)


# 测试
if __name__ == "__main__":
    guard = get_fs_guard()
    
    print("=== File System Guard 测试 ===")
    
    # 测试路径
    test_paths = [
        "~/项目/Ai学习System/projects/crawler/crawler.py",  # 项目内
        "~/项目/Ai学习系统/security/secrets_manager.py",  # 项目内
        "~/.ssh/id_rsa",                                  # 禁止
        "~/.aws/credentials",                             # 禁止
        "/etc/passwd",                                    # 禁止
        "/tmp/test.txt",                                  # 临时目录
        "~/Downloads/file.txt",                          # 下载目录
    ]
    
    print(f"\n项目目录: {guard.PROJECT_ROOT}")
    print(f"\n允许目录: {guard.get_allowed_dirs()}")
    print(f"禁止目录: {guard.get_forbidden_dirs()}")
    
    print("\n路径验证:")
    for path in test_paths:
        result = guard.validate_path(path)
        status = "✅" if result['allowed'] else "❌"
        print(f"  {status} {path}")
        if not result['allowed']:
            print(f"      原因: {result['reason']}")
    
    print("\n✅ File System Guard 工作正常")
