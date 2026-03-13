#!/usr/bin/env python3
"""
Telegram 命令处理示例 - 带用户白名单
展示如何集成 TelegramGuard
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openclaw_modules.telegram_guard import check_user, authorized_only, get_telegram_guard


class TelegramCommandHandler:
    """Telegram 命令处理器"""
    
    def __init__(self):
        self.guard = get_telegram_guard()
    
    def handle_message(self, user_id: int, command: str, args: list):
        """
        处理消息
        """
        # 🔐 第一步：检查用户权限
        self.guard.check(user_id)
        
        # ✅ 用户允许，执行命令
        if command == "/start":
            return self.cmd_start(user_id)
        
        elif command == "/status":
            return self.cmd_status()
        
        elif command == "/help":
            return self.cmd_help()
        
        elif command == "/gateway":
            return self.cmd_gateway(user_id, args)
        
        else:
            return f"未知命令: {command}"
    
    def cmd_start(self, user_id: int):
        """欢迎命令"""
        return f"""
👋 欢迎！
        
你的 ID: {user_id}
白名单: {'✅ 已授权' if self.guard.is_allowed(user_id) else '❌ 未授权'}
        """
    
    def cmd_status(self):
        """状态命令"""
        from security.secrets_manager import get_secrets_manager
        
        sm = get_secrets_manager()
        secrets = sm.get_all()
        
        status = "=== 系统状态 ===\n\n"
        status += f"Gateway: ✅ 运行中\n"
        status += f"白名单用户: {self.guard.get_allowed_users()}\n"
        status += f"密钥配置: {sum(secrets.values())} 个"
        
        return status
    
    def cmd_help(self):
        """帮助命令"""
        return """
📖 可用命令:

/start - 欢迎
/status - 系统状态
/help - 帮助
/gateway start - 启动 Gateway
/gateway stop - 停止 Gateway
/gateway restart - 重启 Gateway

⚠️ 仅白名单用户可用
        """
    
    @authorized_only
    def cmd_gateway(self, user_id: int, args: list):
        """Gateway 控制命令"""
        if not args:
            return "用法: /gateway [start|stop|restart]"
        
        action = args[0]
        
        if action == "start":
            return "🔄 启动 Gateway..."
        elif action == "stop":
            return "🔄 停止 Gateway..."
        elif action == "restart":
            return "🔄 重启 Gateway..."
        else:
            return f"未知操作: {action}"


# 使用示例
def main():
    handler = TelegramCommandHandler()
    
    print("=== Telegram 命令处理测试 ===\n")
    
    # 模拟消息
    test_messages = [
        (8793442405, "/start", []),      # 你
        (8793442405, "/status", []),     # 你
        (8793442405, "/gateway", ["start"]),  # 你
        (123456789, "/start", []),       # 其他人
        (123456789, "/gateway", ["start"]),   # 其他人
    ]
    
    for user_id, command, args in test_messages:
        print(f"用户 {user_id} -> {command} {args}")
        try:
            result = handler.handle_message(user_id, command, args)
            print(f"  ✅ 结果: {result[:80]}...")
        except PermissionError as e:
            print(f"  ❌ 拒绝: {str(e)[:60]}...")
        print()


if __name__ == "__main__":
    main()
