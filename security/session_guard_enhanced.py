#!/usr/bin/env python3
"""
Enhanced Session Guard - 增强版会话守卫
功能：
1. 会话管理
2. 会话ID
3. 30分钟过期
4. 登录/登出
5. 防止Token盗用
"""
import os
import hashlib
import time
import secrets
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class EnhancedSessionGuard:
    """增强版会话守卫"""
    
    # 会话配置
    DEFAULT_EXPIRE_MINUTES = 30
    MAX_SESSIONS_PER_USER = 5
    
    def __init__(self):
        """初始化"""
        # 会话存储
        self.sessions: Dict[str, dict] = {}
        
        # 用户会话索引
        self.user_sessions: Dict[str, List[str]] = {}
        
        # 统计
        self.stats = {
            'total_logins': 0,
            'total_logouts': 0,
            'expired': 0,
            'failed': 0
        }
        
        # 日志
        self.log: List[dict] = []
    
    def _log(self, event: str, user_id: str, details: dict = None):
        """记录日志"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'user_id': user_id,
            'details': details or {}
        }
        self.log.append(entry)
        
        # 写入文件
        log_file = os.path.expanduser('~/.openclaw/logs/session_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {event}: user={user_id} {details}\n")
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return secrets.token_urlsafe(32)
    
    def _generate_token(self, user_id: str) -> str:
        """生成用户Token"""
        data = f"{user_id}:{time.time()}:{secrets.token_hex(16)}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    # ========== 会话管理 ==========
    
    def login(self, user_id: str, metadata: dict = None) -> dict:
        """
        用户登录
        
        Returns:
            dict: {
                'session_id': str,
                'token': str,
                'expires_at': str,
                'expires_in': int (秒)
            }
        """
        # 检查用户会话数
        if user_id in self.user_sessions:
            user_session_ids = self.user_sessions[user_id]
            
            # 清理过期会话
            self._cleanup_user_sessions(user_id)
            
            # 检查数量
            if len(user_session_ids) >= self.MAX_SESSIONS_PER_USER:
                # 删除最早的会话
                oldest = user_session_ids.pop(0)
                if oldest in self.sessions:
                    del self.sessions[oldest]
        
        # 生成会话
        session_id = self._generate_session_id()
        token = self._generate_token(user_id)
        expires_at = datetime.now() + timedelta(minutes=self.DEFAULT_EXPIRE_MINUTES)
        
        # 存储会话
        self.sessions[session_id] = {
            'user_id': user_id,
            'token': token,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'last_active': datetime.now().isoformat(),
            'ip_address': metadata.get('ip_address') if metadata else None,
            'user_agent': metadata.get('user_agent') if metadata else None,
            'metadata': metadata or {}
        }
        
        # 更新用户会话索引
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = []
        self.user_sessions[user_id].append(session_id)
        
        # 统计
        self.stats['total_logins'] += 1
        
        # 日志
        self._log('login', user_id, {
            'session_id': session_id[:16],
            'expires_at': expires_at.isoformat()
        })
        
        return {
            'session_id': session_id,
            'token': token,
            'expires_at': expires_at.isoformat(),
            'expires_in': self.DEFAULT_EXPIRE_MINUTES * 60
        }
    
    def logout(self, session_id: str) -> bool:
        """用户登出"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        user_id = session['user_id']
        
        # 删除会话
        del self.sessions[session_id]
        
        # 更新索引
        if user_id in self.user_sessions:
            if session_id in self.user_sessions[user_id]:
                self.user_sessions[user_id].remove(session_id)
        
        # 统计
        self.stats['total_logouts'] += 1
        
        # 日志
        self._log('logout', user_id, {'session_id': session_id[:16]})
        
        return True
    
    def logout_user(self, user_id: str) -> int:
        """登出用户所有会话"""
        if user_id not in self.user_sessions:
            return 0
        
        count = 0
        for session_id in self.user_sessions[user_id]:
            if session_id in self.sessions:
                del self.sessions[session_id]
                count += 1
        
        self.user_sessions[user_id] = []
        
        self._log('logout_all', user_id, {'count': count})
        
        return count
    
    # ========== 会话验证 ==========
    
    def validate(self, session_id: str, token: str = None) -> dict:
        """
        验证会话
        
        Returns:
            dict: {
                'valid': bool,
                'user_id': str,
                'expires_at': str,
                'message': str
            }
        """
        # 检查会话是否存在
        if session_id not in self.sessions:
            return {
                'valid': False,
                'message': '会话不存在'
            }
        
        session = self.sessions[session_id]
        
        # 检查是否过期
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            # 删除过期会话
            self._cleanup_session(session_id)
            self.stats['expired'] += 1
            
            return {
                'valid': False,
                'message': '会话已过期'
            }
        
        # 验证Token (可选)
        if token and session['token'] != token:
            return {
                'valid': False,
                'message': 'Token无效'
            }
        
        # 更新最后活跃时间
        session['last_active'] = datetime.now().isoformat()
        
        return {
            'valid': True,
            'user_id': session['user_id'],
            'expires_at': session['expires_at'],
            'message': '会话有效'
        }
    
    def refresh(self, session_id: str) -> dict:
        """刷新会话"""
        if session_id not in self.sessions:
            return {'valid': False, 'message': '会话不存在'}
        
        session = self.sessions[session_id]
        
        # 检查是否过期
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            return {'valid': False, 'message': '会话已过期'}
        
        # 刷新过期时间
        new_expires = datetime.now() + timedelta(minutes=self.DEFAULT_EXPIRE_MINUTES)
        session['expires_at'] = new_expires.isoformat()
        session['last_active'] = datetime.now().isoformat()
        
        self._log('refresh', session['user_id'], {'session_id': session_id[:16]})
        
        return {
            'valid': True,
            'expires_at': new_expires.isoformat(),
            'expires_in': self.DEFAULT_EXPIRE_MINUTES * 60
        }
    
    # ========== 清理 ==========
    
    def _cleanup_session(self, session_id: str):
        """清理单个会话"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            user_id = session['user_id']
            
            del self.sessions[session_id]
            
            if user_id in self.user_sessions:
                if session_id in self.user_sessions[user_id]:
                    self.user_sessions[user_id].remove(session_id)
    
    def _cleanup_user_sessions(self, user_id: str):
        """清理用户过期会话"""
        if user_id not in self.user_sessions:
            return
        
        expired = []
        for session_id in self.user_sessions[user_id]:
            if session_id not in self.sessions:
                expired.append(session_id)
                continue
            
            session = self.sessions[session_id]
            expires_at = datetime.fromisoformat(session['expires_at'])
            
            if datetime.now() > expires_at:
                expired.append(session_id)
                del self.sessions[session_id]
        
        for session_id in expired:
            self.user_sessions[user_id].remove(session_id)
    
    def cleanup_expired(self) -> int:
        """清理所有过期会话"""
        expired = []
        
        for session_id, session in self.sessions.items():
            expires_at = datetime.fromisoformat(session['expires_at'])
            if datetime.now() > expires_at:
                expired.append(session_id)
        
        for session_id in expired:
            self._cleanup_session(session_id)
            self.stats['expired'] += 1
        
        return len(expired)
    
    # ========== 查询 ==========
    
    def get_user_sessions(self, user_id: str) -> List[dict]:
        """获取用户所有会话"""
        if user_id not in self.user_sessions:
            return []
        
        # 清理过期
        self._cleanup_user_sessions(user_id)
        
        sessions = []
        for session_id in self.user_sessions.get(user_id, []):
            if session_id in self.sessions:
                session = self.sessions[session_id].copy()
                session['session_id'] = session_id
                sessions.append(session)
        
        return sessions
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话信息"""
        return self.sessions.get(session_id)
    
    def is_logged_in(self, user_id: str) -> bool:
        """检查用户是否登录"""
        sessions = self.get_user_sessions(user_id)
        return len(sessions) > 0
    
    def get_stats(self) -> dict:
        return self.stats.copy()
    
    def get_all_sessions(self) -> int:
        return len(self.sessions)


# 全局实例
_guard = None

def get_guard() -> EnhancedSessionGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedSessionGuard()
    return _guard

def login(user_id: str, metadata: dict = None) -> dict:
    return get_guard().login(user_id, metadata)

def logout(session_id: str) -> bool:
    return get_guard().logout(session_id)

def validate_session(session_id: str, token: str = None) -> dict:
    return get_guard().validate(session_id, token)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Session Guard 测试 ===\n")
    
    # 登录
    print("1. 用户登录:")
    result = guard.login('8793442405', {'ip_address': '127.0.0.1'})
    session_id = result['session_id']
    print(f"   会话ID: {session_id[:20]}...")
    print(f"   Token: {result['token'][:20]}...")
    print(f"   过期: {result['expires_in']}秒")
    
    # 验证
    print("\n2. 验证会话:")
    result = guard.validate(session_id)
    print(f"   有效: {result['valid']}")
    print(f"   用户: {result.get('user_id')}")
    
    # 刷新
    print("\n3. 刷新会话:")
    result = guard.refresh(session_id)
    print(f"   新过期: {result.get('expires_in')}秒")
    
    # 查询
    print("\n4. 用户会话:")
    sessions = guard.get_user_sessions('8793442405')
    print(f"   会话数: {len(sessions)}")
    
    # 登出
    print("\n5. 用户登出:")
    guard.logout(session_id)
    print("   已登出")
    
    print(f"\n统计: {guard.get_stats()}")
