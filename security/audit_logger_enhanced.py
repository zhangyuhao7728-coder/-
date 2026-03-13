#!/usr/bin/env python3
"""
Enhanced Audit Logger - 增强版审计日志
功能：
1. 记录所有操作
2. 用户行为追踪
3. 时间线记录
4. 统计分析
5. 日志轮转
"""
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class EnhancedAuditLogger:
    """增强版审计日志器"""
    
    # 日志数据库
    DB_PATH = os.path.expanduser('~/.openclaw/logs/audit.db')
    
    # 日志级别
    LEVELS = {
        'INFO': 1,
        'WARNING': 2,
        'ERROR': 3,
        'CRITICAL': 4
    }
    
    # 操作类型
    OPERATION_TYPES = {
        'command': '命令执行',
        'file_access': '文件访问',
        'network': '网络请求',
        'login': '登录',
        'logout': '登出',
        'permission': '权限检查',
        'config': '配置变更',
        'api': 'API调用',
        'system': '系统操作',
        'security': '安全事件'
    }
    
    def __init__(self):
        """初始化"""
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        os.makedirs(os.path.dirname(self.DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT DEFAULT 'INFO',
                operation TEXT NOT NULL,
                user_id TEXT,
                username TEXT,
                command TEXT,
                file_path TEXT,
                ip_address TEXT,
                status TEXT,
                details TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON audit_log(timestamp)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_user ON audit_log(user_id)
        ''')
        conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_operation ON audit_log(operation)
        ''')
        
        conn.commit()
        conn.close()
    
    def _connect(self):
        """连接数据库"""
        return sqlite3.connect(self.DB_PATH)
    
    def log(self, 
            operation: str,
            level: str = 'INFO',
            user_id: str = None,
            username: str = None,
            command: str = None,
            file_path: str = None,
            ip_address: str = None,
            status: str = 'OK',
            details: dict = None,
            duration_ms: int = None):
        """
        记录日志
        
        Args:
            operation: 操作类型
            level: 日志级别
            user_id: 用户ID
            username: 用户名
            command: 命令
            file_path: 文件路径
            ip_address: IP地址
            status: 状态
            details: 详情
            duration_ms: 耗时(毫秒)
        """
        timestamp = datetime.now().isoformat()
        
        conn = self._connect()
        conn.execute('''
            INSERT INTO audit_log 
            (timestamp, level, operation, user_id, username, command, file_path, 
             ip_address, status, details, duration_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            timestamp,
            level,
            operation,
            user_id,
            username,
            command,
            file_path,
            ip_address,
            status,
            json.dumps(details) if details else None,
            duration_ms
        ))
        conn.commit()
        conn.close()
        
        # 同时写入文本日志
        self._write_text_log(timestamp, level, operation, user_id, status, details)
    
    def _write_text_log(self, timestamp, level, operation, user_id, status, details):
        """写入文本日志"""
        log_file = os.path.expanduser('~/.openclaw/logs/audit.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        msg = f"[{timestamp}] [{level}] {operation}"
        if user_id:
            msg += f" user={user_id}"
        if status:
            msg += f" status={status}"
        if details:
            msg += f" details={json.dumps(details)[:100]}"
        
        with open(log_file, 'a') as f:
            f.write(msg + '\n')
    
    # ========== 便捷方法 ==========
    
    def log_command(self, user_id: str, command: str, status: str = 'OK', duration_ms: int = None):
        """记录命令执行"""
        self.log(
            operation='command',
            user_id=user_id,
            command=command,
            status=status,
            duration_ms=duration_ms
        )
    
    def log_file_access(self, user_id: str, file_path: str, operation: str, status: str = 'OK'):
        """记录文件访问"""
        self.log(
            operation='file_access',
            user_id=user_id,
            file_path=file_path,
            details={'operation': operation},
            status=status
        )
    
    def log_network(self, user_id: str, url: str, status: str = 'OK', status_code: int = None):
        """记录网络请求"""
        self.log(
            operation='network',
            user_id=user_id,
            details={'url': url, 'status_code': status_code},
            status=status
        )
    
    def log_login(self, user_id: str, username: str, ip_address: str, success: bool):
        """记录登录"""
        self.log(
            operation='login',
            user_id=user_id,
            username=username,
            ip_address=ip_address,
            status='SUCCESS' if success else 'FAILED'
        )
    
    def log_permission(self, user_id: str, permission: str, granted: bool):
        """记录权限检查"""
        self.log(
            operation='permission',
            user_id=user_id,
            details={'permission': permission, 'granted': granted},
            status='GRANTED' if granted else 'DENIED'
        )
    
    def log_security(self, level: str, event: str, details: dict):
        """记录安全事件"""
        self.log(
            operation='security',
            level=level,
            details=details,
            status=event
        )
    
    def log_api(self, user_id: str, endpoint: str, method: str, status_code: int, duration_ms: int):
        """记录API调用"""
        self.log(
            operation='api',
            user_id=user_id,
            details={'endpoint': endpoint, 'method': method, 'status_code': status_code},
            status=str(status_code),
            duration_ms=duration_ms
        )
    
    # ========== 查询方法 ==========
    
    def query(self, 
              user_id: str = None,
              operation: str = None,
              status: str = None,
              start_time: str = None,
              end_time: str = None,
              limit: int = 100) -> List[Dict]:
        """查询日志"""
        conn = self._connect()
        
        sql = 'SELECT * FROM audit_log WHERE 1=1'
        params = []
        
        if user_id:
            sql += ' AND user_id = ?'
            params.append(user_id)
        
        if operation:
            sql += ' AND operation = ?'
            params.append(operation)
        
        if status:
            sql += ' AND status = ?'
            params.append(status)
        
        if start_time:
            sql += ' AND timestamp >= ?'
            params.append(start_time)
        
        if end_time:
            sql += ' AND timestamp <= ?'
            params.append(end_time)
        
        sql += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor = conn.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_user_activity(self, user_id: str, limit: int = 100) -> List[Dict]:
        """获取用户活动"""
        return self.query(user_id=user_id, limit=limit)
    
    def get_failed_operations(self, limit: int = 100) -> List[Dict]:
        """获取失败的操作"""
        return self.query(status='FAILED', limit=limit)
    
    def get_security_events(self, limit: int = 100) -> List[Dict]:
        """获取安全事件"""
        return self.query(operation='security', limit=limit)
    
    def get_today_stats(self) -> Dict:
        """获取今日统计"""
        today = datetime.now().date().isoformat()
        
        conn = self._connect()
        
        # 总数
        cursor = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE timestamp >= ?",
            (today,)
        )
        total = cursor.fetchone()[0]
        
        # 失败数
        cursor = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE timestamp >= ? AND status = 'FAILED'",
            (today,)
        )
        failed = cursor.fetchone()[0]
        
        # 按操作类型统计
        cursor = conn.execute('''
            SELECT operation, COUNT(*) as count 
            FROM audit_log 
            WHERE timestamp >= ?
            GROUP BY operation 
            ORDER BY count DESC
        ''', (today,))
        operations = dict(cursor.fetchall())
        
        # 按用户统计
        cursor = conn.execute('''
            SELECT user_id, COUNT(*) as count 
            FROM audit_log 
            WHERE timestamp >= ? AND user_id IS NOT NULL
            GROUP BY user_id 
            ORDER BY count DESC
            LIMIT 5
        ''', (today,))
        users = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total': total,
            'failed': failed,
            'success_rate': f"{(total-failed)/total*100:.1f}%" if total > 0 else "N/A",
            'by_operation': operations,
            'by_user': users
        }
    
    # ========== 日志管理 ==========
    
    def rotate(self, days: int = 30):
        """日志轮转 - 删除旧日志"""
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        conn = self._connect()
        cursor = conn.execute(
            "DELETE FROM audit_log WHERE timestamp < ?",
            (cutoff,)
        )
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_size(self) -> int:
        """获取日志大小"""
        if os.path.exists(self.DB_PATH):
            return os.path.getsize(self.DB_PATH)
        return 0
    
    def export_json(self, filepath: str, start_time: str = None, end_time: str = None):
        """导出JSON"""
        logs = self.query(start_time=start_time, end_time=end_time, limit=100000)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
        
        return len(logs)


# 全局实例
_logger = None

def get_logger() -> EnhancedAuditLogger:
    global _logger
    if _logger is None:
        _logger = EnhancedAuditLogger()
    return _logger

# 便捷方法
def log_command(user_id: str, command: str, status: str = 'OK'):
    get_logger().log_command(user_id, command, status)

def log_file_access(user_id: str, file_path: str, operation: str, status: str = 'OK'):
    get_logger().log_file_access(user_id, file_path, operation, status)

def log_login(user_id: str, username: str, ip_address: str, success: bool):
    get_logger().log_login(user_id, username, ip_address, success)

def log_security(event: str, details: dict):
    get_logger().log_security('INFO', event, details)


# 测试
if __name__ == "__main__":
    logger = get_logger()
    
    print("=== Enhanced Audit Logger 测试 ===\n")
    
    # 记录测试日志
    print("记录测试日志...")
    logger.log_command('8793442405', 'python projects/crawler.py', 'OK', 5000)
    logger.log_file_access('8793442405', '~/项目/Ai学习系统/crawler.py', 'read', 'OK')
    logger.log_login('8793442405', 'zhangyuhao', '127.0.0.1', True)
    logger.log_security('unauthorized_access', {'user_id': '123456', 'attempt': 'sudo'})
    
    # 今日统计
    print("\n今日统计:")
    stats = logger.get_today_stats()
    print(f"  总操作: {stats['total']}")
    print(f"  失败: {stats['failed']}")
    print(f"  成功率: {stats['success_rate']}")
    
    # 查询最近日志
    print("\n最近日志:")
    recent = logger.query(limit=5)
    for log in recent:
        print(f"  {log['timestamp'][:19]} | {log['operation']:12} | {log['status']}")
    
    print(f"\n日志大小: {logger.get_size()} bytes")
