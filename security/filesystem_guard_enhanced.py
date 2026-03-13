#!/usr/bin/env python3
"""
Enhanced FileSystem Guard - 增强版文件系统守卫
功能：
1. 项目目录隔离
2. 敏感目录禁止访问
3. 文件类型限制
4. 操作审计
"""
import os
import re
from typing import List, Dict, Tuple


class EnhancedFileSystemGuard:
    """增强版文件系统守卫"""
    
    # ========== 项目根目录 ==========
    PROJECT_ROOT = os.path.expanduser("~/项目/Ai学习系统")
    
    # ========== 允许的目录 ==========
    ALLOWED_DIRS = [
        PROJECT_ROOT,
        os.path.expanduser("~/项目"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Desktop"),
        "/tmp",
    ]
    
    # ========== 禁止的目录 ==========
    FORBIDDEN_DIRS = [
        # SSH/密钥
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.gnupg"),
        
        # 云凭证
        os.path.expanduser("~/.aws"),
        os.path.expanduser("~/.azure"),
        os.path.expanduser("~/.gcloud"),
        
        # 配置
        os.path.expanduser("~/.config"),
        os.path.expanduser("~/.kube"),
        
        # 系统
        "/etc",
        "/var",
        "/usr/local/etc",
        "/System",
        "/Applications",
        
        # 项目外
        os.path.expanduser("~/Library"),
        os.path.expanduser("~/Documents"),
    ]
    
    # ========== 允许的文件类型 ==========
    ALLOWED_EXTENSIONS = {
        # 代码
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.c', '.cpp', '.h', '.hpp',
        '.go', '.rs', '.rb', '.php',
        
        # 数据
        '.json', '.yaml', '.yml', '.toml',
        '.xml', '.csv', '.txt', '.md',
        
        # 配置
        '.env', '.example', '.conf', '.ini',
        
        # Web
        '.html', '.css', '.scss', '.sass',
        
        # 文档
        '.pdf', '.doc', '.docx',
        
        # 镜像
        '.jpg', '.jpeg', '.png', '.gif', '.svg',
        
        # 压缩
        '.zip', '.tar', '.gz', '.rar',
    }
    
    # ========== 禁止的文件类型 ==========
    FORBIDDEN_EXTENSIONS = {
        '.exe', '.dmg', '.app',
        '.sh', '.bash', '.zsh',
        '.key', '.pem', '.crt', '.p12', '.pfx',
        '.sql', '.db', '.sqlite',
    }
    
    # ========== 禁止的文件名模式 ==========
    FORBIDDEN_FILENAMES = [
        # 密钥
        r'id_.*',
        r'.*\.key',
        r'.*\.pem',
        r'.*\.crt',
        
        # 凭证
        r'.*credentials.*',
        r'.*\.env$',
        r'.*\.token.*',
        r'.*\.secret.*',
        
        # 历史
        r'\.bash_history',
        r'\.zsh_history',
        r'\.mysql_history',
        
        # 缓存
        r'\.cache',
        r'.*\.log',
    ]
    
    def __init__(self, project_root: str = None):
        """初始化"""
        if project_root:
            self.PROJECT_ROOT = os.path.abspath(project_root)
        
        # 标准化路径
        self._allowed_dirs = [os.path.abspath(d) for d in self.ALLOWED_DIRS]
        self._forbidden_dirs = [os.path.abspath(d) for d in self.FORBIDDEN_DIRS]
        
        # 编译禁止文件名模式
        self._forbidden_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.FORBIDDEN_FILENAMES
        ]
        
        # 统计
        self.stats = {'total': 0, 'blocked': 0, 'allowed': 0}
        
        # 日志
        self.log: List[dict] = []
    
    def _log(self, action: str, path: str, reason: str = ''):
        """记录日志"""
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'path': path,
            'reason': reason
        }
        self.log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/filesystem_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {action}: {path} ({reason})\n")
    
    def _normalize_path(self, path: str) -> str:
        """标准化路径"""
        path = os.path.expanduser(path)
        return os.path.abspath(path)
    
    def is_in_allowed_dir(self, path: str) -> Tuple[bool, str]:
        """检查是否在允许目录"""
        path = self._normalize_path(path)
        
        for allowed_dir in self._allowed_dirs:
            if path.startswith(allowed_dir):
                return True, ''
        
        return False, f'不在允许目录内'
    
    def is_in_forbidden_dir(self, path: str) -> Tuple[bool, str]:
        """检查是否在禁止目录"""
        path = self._normalize_path(path)
        
        for forbidden_dir in self._forbidden_dirs:
            if path.startswith(forbidden_dir):
                return True, f'禁止目录: {forbidden_dir}'
        
        return False, ''
    
    def is_allowed_extension(self, path: str) -> Tuple[bool, str]:
        """检查文件扩展名"""
        path = self._normalize_path(path)
        
        # 无扩展名 - 允许
        if '.' not in os.path.basename(path):
            return True, ''
        
        ext = os.path.splitext(path)[1].lower()
        
        # 检查禁止扩展
        if ext in self.FORBIDDEN_EXTENSIONS:
            return False, f'禁止的文件类型: {ext}'
        
        # 检查允许扩展 (如果不限制则允许)
        # if ext not in self.ALLOWED_EXTENSIONS:
        #     return False, f'不支持的文件类型: {ext}'
        
        return True, ''
    
    def is_forbidden_filename(self, path: str) -> Tuple[bool, str]:
        """检查禁止的文件名"""
        path = self._normalize_path(path)
        filename = os.path.basename(path)
        
        for pattern in self._forbidden_patterns:
            if pattern.match(filename):
                return True, f'禁止的文件名: {filename}'
        
        return False, ''
    
    def check_path(self, path: str) -> Dict:
        """检查路径"""
        self.stats['total'] += 1
        
        path = self._normalize_path(path)
        
        # 1. 检查禁止目录
        blocked, reason = self.is_in_forbidden_dir(path)
        if blocked:
            self.stats['blocked'] += 1
            self._log('BLOCKED', path, reason)
            return {
                'allowed': False,
                'reason': reason,
                'level': 'forbidden'
            }
        
        # 2. 检查允许目录
        allowed, reason = self.is_in_allowed_dir(path)
        if not allowed:
            self.stats['blocked'] += 1
            self._log('BLOCKED', path, reason)
            return {
                'allowed': False,
                'reason': reason,
                'level': 'restricted'
            }
        
        # 3. 检查文件名
        blocked, reason = self.is_forbidden_filename(path)
        if blocked:
            self.stats['blocked'] += 1
            self._log('BLOCKED', path, reason)
            return {
                'allowed': False,
                'reason': reason,
                'level': 'forbidden'
            }
        
        # 4. 检查扩展名
        allowed, reason = self.is_allowed_extension(path)
        if not allowed:
            self.stats['blocked'] += 1
            self._log('BLOCKED', path, reason)
            return {
                'allowed': False,
                'reason': reason,
                'level': 'restricted'
            }
        
        # 通过
        self.stats['allowed'] += 1
        self._log('ALLOWED', path)
        
        return {
            'allowed': True,
            'reason': '路径允许',
            'level': 'allowed'
        }
    
    def validate_read(self, path: str) -> Dict:
        """验证读取操作"""
        return self.check_path(path)
    
    def validate_write(self, path: str) -> Dict:
        """验证写入操作"""
        result = self.check_path(path)
        
        # 写入需要额外检查
        if result['allowed']:
            # 检查是否是只读目录
            readonly_dirs = ['/tmp', '/Downloads']
            for rd in readonly_dirs:
                if path.startswith(rd):
                    return {
                        'allowed': True,
                        'reason': '可写入',
                        'level': 'allowed'
                    }
        
        return result
    
    def validate_delete(self, path: str) -> Dict:
        """验证删除操作 - 更严格"""
        result = self.check_path(path)
        
        if not result['allowed']:
            return result
        
        # 删除需要更严格检查
        # 不能删除项目根目录下的文件
        if path == self.PROJECT_ROOT:
            return {
                'allowed': False,
                'reason': '不能删除项目根目录',
                'level': 'forbidden'
            }
        
        # 检查是否是系统文件
        dangerous = ['node_modules', '.git', '__pycache__']
        for d in dangerous:
            if d in path:
                return {
                    'allowed': False,
                    'reason': f'不能删除: {d}',
                    'level': 'forbidden'
                }
        
        return result
    
    def validate(self, path: str, operation: str = 'read') -> Dict:
        """
        验证操作
        
        Args:
            path: 文件路径
            operation: 操作类型 (read/write/delete)
        """
        if operation == 'read':
            return self.validate_read(path)
        elif operation == 'write':
            return self.validate_write(path)
        elif operation == 'delete':
            return self.validate_delete(path)
        else:
            return self.check_path(path)
    
    def check(self, path: str, operation: str = 'read') -> bool:
        """检查并抛出异常"""
        result = self.validate(path, operation)
        
        if not result['allowed']:
            raise PermissionError(
                f"🚫 文件访问被阻止\n"
                f"路径: {path}\n"
                f"操作: {operation}\n"
                f"原因: {result['reason']}"
            )
        
        return True
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def get_log(self, limit: int = 100) -> List[dict]:
        return self.log[-limit:]


# 全局实例
_guard = None

def get_guard(project_root: str = None) -> EnhancedFileSystemGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedFileSystemGuard(project_root)
    return _guard

def check_path(path: str, operation: str = 'read') -> bool:
    return get_guard().check(path, operation)

def validate_path(path: str, operation: str = 'read') -> Dict:
    return get_guard().validate(path, operation)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced FileSystem Guard 测试 ===\n")
    
    tests = [
        # 禁止目录
        ("~/.ssh/id_rsa", "read", "forbidden"),
        ("~/.aws/credentials", "read", "forbidden"),
        ("/etc/passwd", "read", "forbidden"),
        
        # 允许目录
        ("~/项目/Ai学习系统/crawler.py", "read", "allowed"),
        ("~/项目/Ai学习系统/security/secrets_manager.py", "read", "allowed"),
        
        # 项目外
        ("~/Downloads/file.txt", "read", "allowed"),
        
        # 禁止文件
        ("~/项目/.env", "read", "forbidden"),
        ("~/.bash_history", "read", "forbidden"),
        
        # 危险操作
        ("~/项目/Ai学习系统/__pycache__", "delete", "forbidden"),
    ]
    
    print(f"{'路径':<45} {'操作':<8} {'结果'}")
    print("-" * 65)
    
    for path, operation, expected in tests:
        result = guard.validate(path, operation)
        status = "✅" if (result['level'] == expected) else "❌"
        print(f"{path[:42]:<45} {operation:<8} {result['level']:<12} {status}")
    
    print(f"\n统计: {guard.get_stats()}")
