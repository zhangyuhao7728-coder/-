#!/usr/bin/env python3
"""
Audit Logger - 审计日志
功能：记录所有敏感操作
"""
import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from functools import wraps
import inspect


class AuditLogger:
    """审计日志器"""
    
    def __init__(self, log_dir: str = None):
        """
        初始化
        
        Args:
            log_dir: 日志目录
        """
        if log_dir is None:
            log_dir = Path(__file__).parent.parent / 'logs'
        
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.log_dir / 'audit.log'
        self.current_user = os.environ.get('USER', 'unknown')
    
    def _hash_sensitive(self, data: str) -> str:
        """对敏感数据脱敏"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _format_entry(self, event: str, details: Dict[str, Any]) -> dict:
        """格式化日志条目"""
        return {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'user': self.current_user,
            'details': details
        }
    
    def log(self, event: str, **kwargs):
        """
        记录日志
        
        Args:
            event: 事件名称
            **kwargs: 详细信息
        """
        entry = self._format_entry(event, kwargs)
        
        # 写入文件
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        # 敏感字段脱敏
        sensitive_fields = ['password', 'token', 'key', 'secret', 'api_key']
        for field in sensitive_fields:
            if field in kwargs:
                kwargs[field] = self._hash_sensitive(kwargs[field])
        
        print(f"📝 [{event}] {kwargs}")
    
    def log_command(self, command: str, allowed: bool):
        """记录命令执行"""
        self.log(
            'command_executed',
            command=command[:100],  # 截断
            allowed=allowed,
            status='allowed' if allowed else 'blocked'
        )
    
    def log_file_access(self, filepath: str, operation: str):
        """记录文件访问"""
        self.log(
            'file_accessed',
            filepath=str(filepath)[:200],
            operation=operation
        )
    
    def log_api_call(self, endpoint: str, status: int):
        """记录 API 调用"""
        self.log(
            'api_call',
            endpoint=endpoint[:100],
            status=status
        )
    
    def log_login(self, success: bool, method: str = 'unknown'):
        """记录登录"""
        self.log(
            'login_attempt',
            success=success,
            method=method
        )
    
    def log_config_change(self, key: str, old_value: str = None, new_value: str = None):
        """记录配置变更"""
        self.log(
            'config_changed',
            key=key,
            old_value='***' if old_value else None,
            new_value='***' if new_value else None
        )
    
    def get_recent(self, limit: int = 100) -> list:
        """获取最近日志"""
        if not self.log_file.exists():
            return []
        
        entries = []
        with open(self.log_file, 'r') as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    continue
        
        return entries[-limit:]


# 装饰器：自动审计函数
def audit(event_name: str = None):
    """
    审计装饰器
    
    Usage:
        @audit('function_called')
        def my_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = AuditLogger()
            event = event_name or func.__name__
            
            try:
                result = func(*args, **kwargs)
                logger.log(
                    f'{event}_success',
                    function=func.__name__,
                    args=str(args)[:100],
                    kwargs=str(kwargs)[:100]
                )
                return result
            except Exception as e:
                logger.log(
                    f'{event}_error',
                    function=func.__name__,
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator


# 全局实例
_logger = None

def get_logger() -> AuditLogger:
    """获取日志器实例"""
    global _logger
    if _logger is None:
        _logger = AuditLogger()
    return _logger


# 便捷函数
def log(event: str, **kwargs):
    """记录日志"""
    get_logger().log(event, **kwargs)

def audit_log(event_name: str):
    """审计装饰器"""
    return audit(event_name)


# 测试
if __name__ == "__main__":
    logger = get_logger()
    
    print("=== 审计日志测试 ===")
    
    # 测试记录
    logger.log('test_event', message='Hello')
    logger.log_command('ls -la', True)
    logger.log_file_access('/etc/passwd', 'read')
    logger.log_api_call('/api/users', 200)
    logger.log_login(True, 'password')
    
    print("\n📝 最近日志:")
    for entry in logger.get_recent(3):
        print(f"  {entry['timestamp'][:19]} - {entry['event']}")
