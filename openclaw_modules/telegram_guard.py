#!/usr/bin/env python3
"""
Telegram Guard - Telegram 用户白名单
功能：只允许授权用户执行命令
"""
import os
from typing import Set, Optional


class TelegramGuard:
    """Telegram 用户守卫"""
    
    def __init__(self):
        """初始化"""
        # 允许的用户 ID 集合
        self.allowed_users: Set[int] = set()
        self._load_from_env()
        self._load_from_file()
    
    def _load_from_file(self):
        """从 .env 文件加载"""
        # 尝试从项目根目录的 .env 加载
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            '.env'
        )
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('TELEGRAM_ALLOWED_USERS='):
                        value = line.split('=', 1)[1].strip()
                        if value:
                            for user_id in value.split(','):
                                user_id = user_id.strip()
                                if user_id.isdigit():
                                    self.allowed_users.add(int(user_id))
    
    def _load_from_env(self):
        """从环境变量加载白名单"""
        # 从环境变量读取，格式: "123456789,987654321"
        env_value = os.environ.get('TELEGRAM_ALLOWED_USERS', '')
        
        if env_value:
            for user_id in env_value.split(','):
                user_id = user_id.strip()
                if user_id.isdigit():
                    self.allowed_users.add(int(user_id))
        
        # 如果没有配置，默认允许当前用户
        # 从 TELEGRAM_CHAT_ID 获取
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        if chat_id.isdigit():
            self.allowed_users.add(int(chat_id))
    
    def add_user(self, user_id: int):
        """添加允许的用户"""
        self.allowed_users.add(user_id)
    
    def remove_user(self, user_id: int):
        """移除用户"""
        self.allowed_users.discard(user_id)
    
    def is_allowed(self, user_id: int) -> bool:
        """检查用户是否允许"""
        # 白名单为空时，禁止所有（安全模式）
        # 如果没有配置白名单，必须明确设置用户
        if not self.allowed_users:
            print("⚠️ 警告: 白名单未配置，禁止所有用户访问！")
            return False
        return user_id in self.allowed_users
    
    def check(self, user_id: int) -> bool:
        """
        检查用户权限，如果不允许则抛异常
        """
        if not self.is_allowed(user_id):
            raise PermissionError(
                f"❌ 未授权用户: {user_id}\n"
                f"你不在白名单中，无法执行命令。\n"
                f"请联系管理员添加你到白名单。"
            )
        return True
    
    def get_allowed_users(self) -> list:
        """获取所有允许的用户"""
        return list(self.allowed_users)
    
    def set_allowed_users(self, user_ids: list):
        """设置白名单"""
        self.allowed_users = set(user_ids)


# 全局实例
_guard = None

def get_telegram_guard() -> TelegramGuard:
    """获取 Telegram 守卫实例"""
    global _guard
    if _guard is None:
        _guard = TelegramGuard()
    return _guard


# 便捷函数
def check_user(user_id: int) -> bool:
    """检查用户权限"""
    return get_telegram_guard().check(user_id)

def is_allowed(user_id: int) -> bool:
    """检查是否允许"""
    return get_telegram_guard().is_allowed(user_id)

def add_user(user_id: int):
    """添加用户"""
    get_telegram_guard().add_user(user_id)

def remove_user(user_id: int):
    """移除用户"""
    get_telegram_guard().remove_user(user_id)


# 装饰器：保护函数
def authorized_only(func):
    """
    装饰器：仅允许白名单用户执行
    
    Usage:
        # 方法1：作为函数装饰器
        @authorized_only
        def my_command(user_id, args):
            pass
        
        # 方法2：类方法使用 (需要 self 作为第一个参数)
        @authorized_only
        def cmd_gateway(self, user_id, args):
            pass
    """
    def wrapper(*args, **kwargs):
        # 尝试找到 user_id 参数
        user_id = None
        
        # 检查第一个参数是否是 self (类方法)
        if len(args) > 0 and hasattr(args[0], '__class__'):
            # 类方法，user_id 是第二个参数
            if len(args) > 1:
                user_id = args[1]
        else:
            # 普通函数，user_id 是第一个参数
            if len(args) > 0:
                user_id = args[0]
        
        # 从 kwargs 获取
        if user_id is None:
            user_id = kwargs.get('user_id')
        
        if user_id is None:
            raise ValueError("未找到 user_id 参数")
        
        check_user(user_id)
        return func(*args, **kwargs)
    return wrapper


# 测试
if __name__ == "__main__":
    guard = get_telegram_guard()
    
    print("=== Telegram Guard 测试 ===")
    
    print(f"\n当前允许的用户: {guard.get_allowed_users()}")
    
    # 测试允许的用户
    test_id = 8793442405
    try:
        guard.check(test_id)
        print(f"✅ 用户 {test_id} - 允许")
    except PermissionError as e:
        print(f"❌ 用户 {test_id} - 拒绝: {e}")
    
    # 测试禁止的用户
    test_id = 999999999
    try:
        guard.check(test_id)
        print(f"✅ 用户 {test_id} - 允许")
    except PermissionError as e:
        print(f"❌ 用户 {test_id} - 拒绝")
    
    # 添加用户
    print("\n添加用户 111111...")
    guard.add_user(111111)
    print(f"当前白名单: {guard.get_allowed_users()}")
