#!/usr/bin/env python3
"""
Enhanced Rate Limit Guard - 增强版速率限制守卫
功能：
1. 请求频率限制
2. 防止暴力攻击
3. 自动封禁
4. 多种策略
"""
import os
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class EnhancedRateLimitGuard:
    """增强版速率限制守卫"""
    
    # 限制策略
    STRATEGIES = {
        'fixed': '固定窗口',
        'sliding': '滑动窗口',
        'token_bucket': '令牌桶',
    }
    
    def __init__(self, default_limit: int = 10, window_seconds: int = 60):
        """
        初始化
        
        Args:
            default_limit: 默认限制次数
            window_seconds: 时间窗口(秒)
        """
        self.default_limit = default_limit
        self.window_seconds = window_seconds
        
        # 限制配置
        self.limits: Dict[str, dict] = {}
        
        # 请求记录
        self.requests: Dict[str, List[float]] = defaultdict(list)
        
        # 封禁记录
        self.banned: Dict[str, dict] = {}
        
        # 统计
        self.stats = {
            'total_requests': 0,
            'allowed': 0,
            'denied': 0,
            'banned': 0
        }
        
        # 日志
        self.log: List[dict] = []
    
    def _log(self, event: str, identifier: str, details: dict = None):
        """记录日志"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'identifier': identifier,
            'details': details or {}
        }
        self.log.append(entry)
        
        # 写入文件
        log_file = os.path.expanduser('~/.openclaw/logs/rate_limit.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {event}: {identifier} {details}\n")
    
    # ========== 限制管理 ==========
    
    def set_limit(self, identifier: str, limit: int, window: int = None, strategy: str = 'sliding'):
        """
        设置限制
        
        Args:
            identifier: 标识符 (如用户ID、IP)
            limit: 限制次数
            window: 时间窗口(秒)
            strategy: 策略
        """
        self.limits[identifier] = {
            'limit': limit,
            'window': window or self.window_seconds,
            'strategy': strategy
        }
    
    def set_global_limit(self, limit: int, window: int = None, strategy: str = 'sliding'):
        """设置全局限制"""
        self.default_limit = limit
        self.window_seconds = window or self.window_seconds
    
    def add_limit_rule(self, pattern: str, limit: int, window: int = None):
        """添加限制规则 (支持通配符)"""
        self.limits[pattern] = {
            'limit': limit,
            'window': window or self.window_seconds,
            'is_pattern': True
        }
    
    # ========== 速率限制算法 ==========
    
    def _check_fixed_window(self, identifier: str, limit: int, window: int) -> bool:
        """固定窗口算法"""
        now = time.time()
        window_start = now - window
        
        # 清理旧记录
        self.requests[identifier] = [
            t for t in self.requests[identifier] if t > window_start
        ]
        
        return len(self.requests[identifier]) < limit
    
    def _check_sliding_window(self, identifier: str, limit: int, window: int) -> bool:
        """滑动窗口算法"""
        now = time.time()
        window_start = now - window
        
        # 清理旧记录
        self.requests[identifier] = [
            t for t in self.requests[identifier] if t > window_start
        ]
        
        return len(self.requests[identifier]) < limit
    
    def _check_token_bucket(self, identifier: str, rate: float, capacity: int) -> bool:
        """令牌桶算法"""
        now = time.time()
        
        if identifier not in self.requests:
            # 初始化
            self.requests[identifier] = [now, capacity - 1]
            return True
        
        tokens, last_update = self.requests[identifier]
        
        # 添加令牌
        elapsed = now - last_update
        tokens = min(capacity, tokens + elapsed * rate)
        
        if tokens >= 1:
            tokens -= 1
            self.requests[identifier] = [tokens, now]
            return True
        
        return False
    
    # ========== 检查方法 ==========
    
    def check(self, identifier: str, cost: int = 1) -> dict:
        """
        检查请求是否允许
        
        Args:
            identifier: 标识符 (用户ID/IP)
            cost: 消耗的请求数
            
        Returns:
            dict: {
                'allowed': bool,
                'remaining': int,
                'reset_time': int,
                'reason': str
            }
        """
        self.stats['total_requests'] += 1
        
        # 1. 检查是否被封禁
        if identifier in self.banned:
            ban_info = self.banned[identifier]
            if time.time() < ban_info['expires']:
                self.stats['denied'] += 1
                self._log('banned_denied', identifier, ban_info)
                return {
                    'allowed': False,
                    'remaining': 0,
                    'reset_time': int(ban_info['expires']),
                    'reason': f'已封禁 until {ban_info["expires"]}'
                }
            else:
                # 解封
                del self.banned[identifier]
        
        # 2. 获取限制配置
        limit_info = self.limits.get(identifier) or self.limits.get('*') or {
            'limit': self.default_limit,
            'window': self.window_seconds,
            'strategy': 'sliding'
        }
        
        limit = limit_info.get('limit', self.default_limit)
        window = limit_info.get('window', self.window_seconds)
        strategy = limit_info.get('strategy', 'sliding')
        
        # 3. 检查限制
        now = time.time()
        
        if strategy == 'fixed':
            allowed = self._check_fixed_window(identifier, limit, window)
        elif strategy == 'token_bucket':
            allowed = self._check_token_bucket(identifier, limit/window, limit)
        else:  # sliding
            allowed = self._check_sliding_window(identifier, limit, window)
        
        if allowed:
            # 记录请求
            self.requests[identifier].append(now)
            
            # 计算剩余
            window_start = now - window
            requests_in_window = [
                t for t in self.requests[identifier] if t > window_start
            ]
            remaining = max(0, limit - len(requests_in_window))
            
            self.stats['allowed'] += 1
            self._log('allowed', identifier, {'remaining': remaining})
            
            return {
                'allowed': True,
                'remaining': remaining,
                'reset_time': int(now + window),
                'reason': 'OK'
            }
        else:
            # 拒绝
            self.stats['denied'] += 1
            
            # 触发连续失败检查
            self._check_ban(identifier)
            
            self._log('denied', identifier, {'limit': limit})
            
            return {
                'allowed': False,
                'remaining': 0,
                'reset_time': int(now + window),
                'reason': f'超过限制: {limit}次/{window}秒'
            }
    
    def _check_ban(self, identifier: str, threshold: int = 5):
        """检查是否需要封禁"""
        # 统计最近的拒绝
        recent_denied = 0
        now = time.time()
        
        for log in self.log[-100:]:
            if log['event'] == 'denied' and log['identifier'] == identifier:
                # 简单判断：连续3次拒绝
                recent_denied += 1
        
        if recent_denied >= threshold:
            # 封禁
            ban_duration = 300  # 5分钟
            self.banned[identifier] = {
                'reason': f'连续{threshold}次超限',
                'expires': now + ban_duration,
                'banned_at': now
            }
            self.stats['banned'] += 1
            self._log('banned', identifier, {'duration': ban_duration})
    
    def ban(self, identifier: str, duration: int = 300, reason: str = ''):
        """手动封禁"""
        self.banned[identifier] = {
            'reason': reason or '手动封禁',
            'expires': time.time() + duration,
            'banned_at': time.time()
        }
        self.stats['banned'] += 1
        self._log('banned', identifier, {'duration': duration, 'reason': reason})
    
    def unban(self, identifier: str):
        """解封"""
        if identifier in self.banned:
            del self.banned[identifier]
            self._log('unbanned', identifier)
    
    def is_banned(self, identifier: str) -> bool:
        """检查是否被封禁"""
        if identifier not in self.banned:
            return False
        
        if time.time() < self.banned[identifier]['expires']:
            return True
        
        # 解封
        del self.banned[identifier]
        return False
    
    # ========== 查询 ==========
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return self.stats.copy()
    
    def get_requests(self, identifier: str) -> int:
        """获取请求数"""
        now = time.time()
        window = self.limits.get(identifier, {}).get('window', self.window_seconds)
        window_start = now - window
        
        return len([
            t for t in self.requests[identifier] if t > window_start
        ])
    
    def get_remaining(self, identifier: str) -> int:
        """获取剩余次数"""
        limit = self.limits.get(identifier, {}).get('limit', self.default_limit)
        requests = self.get_requests(identifier)
        return max(0, limit - requests)
    
    def get_banned(self) -> List[dict]:
        """获取封禁列表"""
        now = time.time()
        return [
            {'identifier': k, **v}
            for k, v in self.banned.items()
            if v['expires'] > now
        ]
    
    def reset(self, identifier: str = None):
        """重置"""
        if identifier:
            if identifier in self.requests:
                del self.requests[identifier]
            if identifier in self.banned:
                del self.banned[identifier]
        else:
            self.requests.clear()
            self.banned.clear()


# 全局实例
_guard = None

def get_guard() -> EnhancedRateLimitGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedRateLimitGuard()
    return _guard

def check_rate_limit(identifier: str) -> dict:
    return get_guard().check(identifier)

def is_banned(identifier: str) -> bool:
    return get_guard().is_banned(identifier)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Rate Limit Guard 测试 ===\n")
    
    # 设置限制
    guard.set_global_limit(5, 60)  # 每分钟5次
    
    # 测试
    print("测试: 每分钟5次限制")
    for i in range(7):
        result = guard.check('test_user')
        status = "✅" if result['allowed'] else "❌"
        print(f"  请求{i+1}: {status} - {result['reason']}")
    
    print(f"\n统计: {guard.get_stats()}")
    print(f"封禁列表: {guard.get_banned()}")
