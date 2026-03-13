#!/usr/bin/env python3
"""
Permission Guard - 权限守卫
功能：控制文件和命令的执行权限
"""
import os
import stat
import subprocess
from pathlib import Path
from typing import List, Optional


class PermissionGuard:
    """权限守卫"""
    
    # 危险命令列表
    DANGEROUS_COMMANDS = [
        'rm -rf',
        'mkfs',
        'dd if=',
        ':(){:|:&};:',
        'chmod 777',
        'chown -R',
        '> /dev/sda',
        'wget | sh',
        'curl | sh',
    ]
    
    # 安全目录 (只读)
    SAFE_DIRS = [
        '/usr/bin',
        '/usr/sbin',
        '/bin',
        '/sbin',
    ]
    
    def __init__(self):
        self.blocked = False
        self.log_file = Path(__file__).parent.parent / 'logs' / 'permission_guard.log'
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """确保日志目录存在"""
        log_dir = self.log_file.parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    def _log(self, message: str):
        """记录日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def check_file_permission(self, filepath: str) -> dict:
        """
        检查文件权限
        
        Returns:
            dict: 权限信息
        """
        path = Path(filepath)
        
        if not path.exists():
            return {'safe': False, 'reason': '文件不存在'}
        
        st = path.stat()
        mode = st.st_mode
        
        # 检查危险权限
        issues = []
        
        # 其他用户可写
        if mode & stat.S_IWOTH:
            issues.append('其他用户可写')
        
        # 其他用户可执行
        if mode & stat.S_IXOTH:
            issues.append('其他用户可执行')
        
        # 检查敏感文件
        if str(path).endswith('.env'):
            if mode & (stat.S_IRWXG | stat.S_IRWXO):
                issues.append('.env 权限过于开放')
        
        return {
            'safe': len(issues) == 0,
            'issues': issues,
            'mode': oct(stat.S_IMODE(mode)),
            'owner': st.st_uid
        }
    
    def check_command(self, command: str) -> bool:
        """
        检查命令是否危险
        
        Returns:
            bool: 是否允许执行
        """
        command_lower = command.lower()
        
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                self._log(f"🚫 阻止危险命令: {command}")
                return False
        
        return True
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[dict]:
        """
        扫描目录中的权限问题
        
        Args:
            directory: 目录路径
            extensions: 要检查的文件扩展名
        """
        results = []
        path = Path(directory)
        
        if not path.exists():
            return results
        
        for file_path in path.rglob('*'):
            if not file_path.is_file():
                continue
            
            # 检查特定扩展名
            if extensions and file_path.suffix not in extensions:
                continue
            
            perm = self.check_file_permission(str(file_path))
            if not perm['safe']:
                results.append({
                    'file': str(file_path),
                    'issues': perm['issues'],
                    'mode': perm['mode']
                })
        
        return results
    
    def fix_permissions(self, filepath: str) -> bool:
        """
        修复文件权限
        
        Args:
            filepath: 文件路径
        """
        path = Path(filepath)
        
        if not path.exists():
            return False
        
        try:
            # 敏感文件: 600
            if str(path).endswith('.env') or str(path).endswith('.key'):
                os.chmod(filepath, 0o600)
                self._log(f"✅ 修复权限: {filepath} -> 600")
            
            # Python 文件: 644
            elif str(path).endswith('.py'):
                os.chmod(filepath, 0o644)
                self._log(f"✅ 修复权限: {filepath} -> 644")
            
            return True
            
        except Exception as e:
            self._log(f"❌ 修复失败: {filepath} - {e}")
            return False


# 全局实例
_guard = None

def get_guard() -> PermissionGuard:
    """获取权限守卫实例"""
    global _guard
    if _guard is None:
        _guard = PermissionGuard()
    return _guard


# 便捷函数
def check_file(filepath: str) -> dict:
    """检查文件权限"""
    return get_guard().check_file_permission(filepath)

def check_command(command: str) -> bool:
    """检查命令是否安全"""
    return get_guard().check_command(command)

def scan_dir(directory: str, extensions: List[str] = None) -> List[dict]:
    """扫描目录"""
    return get_guard().scan_directory(directory, extensions)

def fix_perm(filepath: str) -> bool:
    """修复权限"""
    return get_guard().fix_permissions(filepath)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== 权限守卫测试 ===")
    
    # 检查当前目录
    print("\n📁 扫描 Python 文件...")
    results = scan_dir('.', ['.py', '.env'])
    
    if results:
        print(f"⚠️ 发现 {len(results)} 个权限问题:")
        for r in results[:5]:
            print(f"  {r['file']}: {r['issues']}")
    else:
        print("✅ 无权限问题")
