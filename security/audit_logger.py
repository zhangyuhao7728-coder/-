#!/usr/bin/env python3
"""
Audit Logger - 审计日志模块
功能：
1. security.log - 安全日志
2. access.log - 访问日志
3. commands.log - 命令日志
"""
import os
import json
from datetime import datetime
from typing import Optional


class AuditLogger:
    """审计日志器"""
    
    LOGS_DIR = os.path.expanduser('~/.openclaw/logs')
    
    def __init__(self):
        """初始化"""
        os.makedirs(self.LOGS_DIR, exist_ok=True)
    
    # ========== Security Log ==========
    
    def log_security(self, level: str, event: str, user_id: str = None, 
                     details: dict = None, ip: str = None):
        """
        记录安全日志
        
        [SECURITY ALERT]
        Time: 2026-03-13 18:53:00
        Level: WARNING
        Event: unauthorized_command
        User: 8793442405
        IP: 127.0.0.1
        Details: {"command": "rm -rf"}
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"""[SECURITY {level.upper()}]
Time: {timestamp}
Event: {event}
User: {user_id or 'unknown'}
IP: {ip or 'N/A'}
Details: {json.dumps(details) if details else 'N/A'}
"""
        
        filepath = os.path.join(self.LOGS_DIR, 'security.log')
        with open(filepath, 'a') as f:
            f.write(log_entry + '\n')
        
        print(log_entry)
    
    def log_unauthorized(self, event: str, user_id: str = None,
                        command: str = None, ip: str = None):
        """记录未授权访问"""
        self.log_security('ALERT', event, user_id, 
                        {'command': command} if command else None, ip)
    
    # ========== Access Log ==========
    
    def log_access(self, user_id: str, resource: str, 
                   action: str, status: str, ip: str = None):
        """
        记录访问日志
        
        [ACCESS]
        Time: 2026-03-13 18:53:00
        User: 8793442405
        Resource: /api/crawler
        Action: read
        Status: OK
        IP: 127.0.0.1
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"""[ACCESS]
Time: {timestamp}
User: {user_id}
Resource: {resource}
Action: {action}
Status: {status}
IP: {ip or 'N/A'}
"""
        
        filepath = os.path.join(self.LOGS_DIR, 'access.log')
        with open(filepath, 'a') as f:
            f.write(log_entry + '\n')
    
    # ========== Commands Log ==========
    
    def log_command(self, user_id: str, command: str, 
                   status: str, duration_ms: int = None, ip: str = None):
        """
        记录命令日志
        
        [COMMAND]
        Time: 2026-03-13 18:53:00
        User: 8793442405
        Command: python projects/crawler/crawler.py -p 3
        Status: OK
        Duration: 5000ms
        IP: 127.0.0.1
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"""[COMMAND]
Time: {timestamp}
User: {user_id}
Command: {command}
Status: {status}
Duration: {duration_ms}ms
IP: {ip or 'N/A'}
"""
        
        filepath = os.path.join(self.LOGS_DIR, 'commands.log')
        with open(filepath, 'a') as f:
            f.write(log_entry + '\n')
    
    # ========== 便捷方法 ==========
    
    def log_login(self, user_id: str, success: bool, ip: str = None):
        """登录日志"""
        self.log_access(user_id, '/auth/login', 'login', 
                      'SUCCESS' if success else 'FAILED', ip)
        
        if not success:
            self.log_unauthorized('login_failed', user_id, ip=ip)
    
    def log_file_access(self, user_id: str, filepath: str, 
                       action: str, status: str):
        """文件访问日志"""
        self.log_access(user_id, filepath, action, status)
    
    def log_network(self, user_id: str, url: str, status: int):
        """网络请求日志"""
        self.log_access(user_id, url, 'http', str(status))
    
    def log_api(self, user_id: str, endpoint: str, 
                method: str, status: int, duration_ms: int):
        """API调用日志"""
        self.log_access(user_id, endpoint, method, str(status))
        
        if status >= 400:
            self.log_security('WARNING', 'api_error', user_id,
                           {'endpoint': endpoint, 'status': status})


# 全局实例
_logger = None

def get_audit_logger() -> AuditLogger:
    global _logger
    if _logger is None:
        _logger = AuditLogger()
    return _logger


# 便捷方法
def log_security(level: str, event: str, **kwargs):
    get_audit_logger().log_security(level, event, **kwargs)

def log_command(user_id: str, command: str, status: str, **kwargs):
    get_audit_logger().log_command(user_id, command, status, **kwargs)

def log_access(user_id: str, resource: str, action: str, status: str, **kwargs):
    get_audit_logger().log_access(user_id, resource, action, status, **kwargs)


# 测试
if __name__ == "__main__":
    logger = get_audit_logger()
    
    print("=== Audit Logger 测试 ===\n")
    
    # Security Log
    print("1. Security Log:")
    logger.log_security('ALERT', 'unauthorized_command', 
                       user_id='8793442405',
                       command='rm -rf /',
                       ip='127.0.0.1')
    
    # Access Log
    print("\n2. Access Log:")
    logger.log_access('8793442405', '/api/crawler', 'read', 'OK', '127.0.0.1')
    
    # Command Log
    print("\n3. Command Log:")
    logger.log_command('8793442405', 'python projects/crawler.py -p 3', 
                      'OK', 5000, '127.0.0.1')
    
    print("\n✅ 测试完成")
