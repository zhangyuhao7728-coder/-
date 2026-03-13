#!/usr/bin/env python3
"""
Enhanced Telegram Guard - 增强版 Telegram 守卫
功能：
1. 用户ID白名单
2. IP地址限制
3. 二次验证
4. 登录尝试限制
5. 操作审计
"""
import os
import time
from typing import Set, Dict, Optional, List
from datetime import datetime, timedelta
import hashlib


class EnhancedTelegramGuard:
    """增强版 Telegram 守卫"""
    
    def __init__(self):
        """初始化"""
        # 用户白名单
        self.allowed_users: Set[int] = set()
        self._load_config()
        
        # IP 白名单
        self.allowed_ips: Set[str] = {
            '127.0.0.1',
            'localhost',
            # 添加你的局域网IP
            # '10.239.39.73',
        }
        
        # 二次验证
        self.two_factor_codes: Dict[int, str] = {}  # user_id -> code
        self.pending_verification: Dict[int, dict] = {}  # user_id -> info
        
        # 登录尝试限制
        self.login_attempts: Dict[int, dict] = {}  # user_id -> attempts
        self.max_attempts = 3
        self.lockout_duration = 300  # 5分钟
        
        # 会话管理
        self.sessions: Dict[int, dict] = {}
        self.session_timeout = 3600  # 1小时
        
        # 审计
        self.audit_log: List[dict] = []
    
    def _load_config(self):
        """从环境变量加载配置"""
        # 用户白名单
        users = os.environ.get('TELEGRAM_ALLOWED_USERS', '')
        if users:
            for uid in users.split(','):
                uid = uid.strip()
                if uid.isdigit():
                    self.allowed_users.add(int(uid))
        
        # 备用: 从 .env 文件加载
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.env'
        )
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('TELEGRAM_ALLOWED_USERS='):
                        users = line.split('=', 1)[1].strip()
                        for uid in users.split(','):
                            uid = uid.strip()
                            if uid.isdigit():
                                self.allowed_users.add(int(uid))
    
    def _log(self, event: str, user_id: int, **kwargs):
        """记录审计日志"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'user_id': user_id,
            **kwargs
        }
        self.audit_log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/telegram_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {event} user={user_id} {kwargs}\n")
    
    # ========== 用户白名单 ==========
    
    def add_user(self, user_id: int):
        """添加用户到白名单"""
        self.allowed_users.add(user_id)
        self._log('user_added', user_id)
    
    def remove_user(self, user_id: int):
        """从白名单移除用户"""
        self.allowed_users.discard(user_id)
        self._log('user_removed', user_id)
    
    def is_allowed_user(self, user_id: int) -> bool:
        """检查用户是否在白名单"""
        if not self.allowed_users:
            return True  # 空白名单允许所有
        return user_id in self.allowed_users
    
    # ========== IP 限制 ==========
    
    def add_ip(self, ip: str):
        """添加IP到白名单"""
        self.allowed_ips.add(ip)
    
    def remove_ip(self, ip: str):
        """从白名单移除IP"""
        self.allowed_ips.discard(ip)
    
    def is_allowed_ip(self, ip: str) -> bool:
        """检查IP是否允许"""
        if not self.allowed_ips:
            return True  # 空白名单允许所有
        # 检查直接匹配
        if ip in self.allowed_ips:
            return True
        # 检查局域网段
        for allowed_ip in self.allowed_ips:
            if allowed_ip.endswith('.0') or allowed_ip.endswith('.1'):
                # 简单网段匹配
                if ip.startswith(allowed_ip.rsplit('.', 1)[0]):
                    return True
        return False
    
    # ========== 登录限制 ==========
    
    def _get_attempts(self, user_id: int) -> dict:
        """获取登录尝试记录"""
        if user_id not in self.login_attempts:
            self.login_attempts[user_id] = {
                'count': 0,
                'first_attempt': None,
                'locked_until': None
            }
        return self.login_attempts[user_id]
    
    def _record_attempt(self, user_id: int, success: bool):
        """记录登录尝试"""
        attempts = self._get_attempts(user_id)
        
        if success:
            attempts['count'] = 0
            attempts['first_attempt'] = None
            attempts['locked_until'] = None
        else:
            attempts['count'] = attempts.get('count', 0) + 1
            if attempts['first_attempt'] is None:
                attempts['first_attempt'] = datetime.now()
            
            if attempts['count'] >= self.max_attempts:
                attempts['locked_until'] = datetime.now() + timedelta(seconds=self.lockout_duration)
                self._log('account_locked', user_id, attempts=attempts['count'])
    
    def _is_locked(self, user_id: int) -> bool:
        """检查是否被锁定"""
        attempts = self._get_attempts(user_id)
        if attempts['locked_until']:
            if datetime.now() < attempts['locked_until']:
                return True
            else:
                # 解锁
                attempts['count'] = 0
                attempts['locked_until'] = None
        return False
    
    # ========== 二次验证 ==========
    
    def generate_2fa_code(self, user_id: int) -> str:
        """生成二次验证码"""
        import random
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # 存储验证码
        self.two_factor_codes[user_id] = code
        
        # 设置过期时间 (5分钟)
        self.pending_verification[user_id] = {
            'code': code,
            'expires': datetime.now() + timedelta(minutes=5),
            'attempts': 0
        }
        
        self._log('2fa_generated', user_id)
        
        return code
    
    def verify_2fa(self, user_id: int, code: str) -> bool:
        """验证二次验证码"""
        if user_id not in self.pending_verification:
            return False
        
        verification = self.pending_verification[user_id]
        
        # 检查过期
        if datetime.now() > verification['expires']:
            del self.pending_verification[user_id]
            self._log('2fa_expired', user_id)
            return False
        
        # 检查尝试次数
        verification['attempts'] += 1
        if verification['attempts'] >= 3:
            del self.pending_verification[user_id]
            self._log('2fa_max_attempts', user_id)
            return False
        
        # 验证
        if verification['code'] == code:
            del self.pending_verification[user_id]
            if user_id in self.two_factor_codes:
                del self.two_factor_codes[user_id]
            self._log('2fa_success', user_id)
            return True
        
        return False
    
    def requires_2fa(self, user_id: int) -> bool:
        """检查是否需要二次验证"""
        # 新用户或敏感操作需要
        return user_id not in self.sessions
    
    # ========== 会话管理 ==========
    
    def create_session(self, user_id: int, ip: str) -> str:
        """创建会话"""
        session_token = hashlib.sha256(
            f"{user_id}:{ip}:{time.time()}".encode()
        ).hexdigest()[:32]
        
        self.sessions[user_id] = {
            'token': session_token,
            'ip': ip,
            'created': datetime.now(),
            'last_active': datetime.now()
        }
        
        self._log('session_created', user_id, ip=ip)
        
        return session_token
    
    def validate_session(self, user_id: int, token: str) -> bool:
        """验证会话"""
        if user_id not in self.sessions:
            return False
        
        session = self.sessions[user_id]
        
        # 检查超时
        if (datetime.now() - session['last_active']).seconds > self.session_timeout:
            del self.sessions[user_id]
            self._log('session_expired', user_id)
            return False
        
        # 验证token
        if session['token'] != token:
            return False
        
        # 更新活跃时间
        session['last_active'] = datetime.now()
        
        return True
    
    def revoke_session(self, user_id: int):
        """撤销会话"""
        if user_id in self.sessions:
            del self.sessions[user_id]
            self._log('session_revoked', user_id)
    
    # ========== 主验证流程 ==========
    
    def verify(self, user_id: int, ip: str = None, 
               two_fa_code: str = None) -> dict:
        """
        完整验证流程
        
        Returns:
            dict: {
                'allowed': bool,
                'reason': str,
                'requires_2fa': bool,
                'session_token': str
            }
        """
        # 1. 检查是否锁定
        if self._is_locked(user_id):
            self._log('access_denied', user_id, reason='locked', ip=ip)
            return {
                'allowed': False,
                'reason': '账户已锁定，请5分钟后再试',
                'requires_2fa': False
            }
        
        # 2. 检查用户白名单
        if not self.is_allowed_user(user_id):
            self._record_attempt(user_id, False)
            self._log('access_denied', user_id, reason='not_in_whitelist', ip=ip)
            return {
                'allowed': False,
                'reason': '你不在授权用户列表中'
            }
        
        # 3. 检查IP白名单
        if ip and not self.is_allowed_ip(ip):
            self._log('access_denied', user_id, reason='ip_not_allowed', ip=ip)
            return {
                'allowed': False,
                'reason': 'IP地址不被允许'
            }
        
        # 4. 检查是否需要二次验证
        if self.requires_2fa(user_id):
            if not two_fa_code:
                # 生成验证码
                code = self.generate_2fa_code(user_id)
                self._log('2fa_required', user_id)
                return {
                    'allowed': False,
                    'reason': '需要二次验证',
                    'requires_2fa': True,
                    '2fa_sent': True  # 实际应该发送验证码到Telegram
                }
            else:
                # 验证验证码
                if not self.verify_2fa(user_id, two_fa_code):
                    self._record_attempt(user_id, False)
                    self._log('access_denied', user_id, reason='2fa_failed', ip=ip)
                    return {
                        'allowed': False,
                        'reason': '验证码错误'
                    }
        
        # 5. 创建会话
        session_token = self.create_session(user_id, ip or 'unknown')
        
        # 6. 记录成功
        self._record_attempt(user_id, True)
        self._log('access_allowed', user_id, ip=ip)
        
        return {
            'allowed': True,
            'reason': '验证通过',
            'session_token': session_token
        }
    
    # ========== 便捷方法 ==========
    
    def check(self, user_id: int, ip: str = None) -> bool:
        """简单检查 - 是否允许"""
        result = self.verify(user_id, ip)
        return result['allowed']
    
    def get_audit_log(self, limit: int = 100) -> List[dict]:
        """获取审计日志"""
        return self.audit_log[-limit:]


# 全局实例
_guard = None

def get_guard() -> EnhancedTelegramGuard:
    """获取守卫实例"""
    global _guard
    if _guard is None:
        _guard = EnhancedTelegramGuard()
    return _guard


# 便捷函数
def check_user(user_id: int, ip: str = None) -> bool:
    """检查用户"""
    return get_guard().check(user_id, ip)

def verify_access(user_id: int, ip: str = None, two_fa_code: str = None) -> dict:
    """验证访问"""
    return get_guard().verify(user_id, ip, two_fa_code)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Telegram Guard 测试 ===")
    
    print(f"\n白名单用户: {guard.allowed_users}")
    print(f"白名单IP: {guard.allowed_ips}")
    
    # 测试验证
    print("\n测试验证:")
    test_id = 8793442405
    
    result = guard.verify(test_id, '127.0.0.1')
    print(f"用户 {test_id}: {result}")
    
    # 测试拒绝
    print("\n测试拒绝:")
    result = guard.verify(123456789, '127.0.0.1')
    print(f"用户 123456789: {result}")
    
    print("\n✅ 测试完成")
