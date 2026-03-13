#!/usr/bin/env python3
"""
Telegram Alert - 实时Telegram告警
功能：
1. 安全事件告警
2. Gateway状态告警
3. 自动发送
"""
import os
import requests
from datetime import datetime


class TelegramAlerts:
    """Telegram告警器"""
    
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
        self.enabled = bool(self.token and self.chat_id)
        
        if not self.enabled:
            print("⚠️ Telegram告警未配置 (缺少TELEGRAM_BOT_TOKEN或TELEGRAM_CHAT_ID)")
    
    def send(self, message: str, level: str = 'info') -> bool:
        """发送告警"""
        if not self.enabled:
            return False
        
        icons = {
            'info': 'ℹ️',
            'warning': '🟡',
            'error': '🔴',
            'critical': '🚨'
        }
        
        icon = icons.get(level, 'ℹ️')
        text = f"{icon} *安全告警*\n\n{message}"
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            resp = requests.post(url, json={
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }, timeout=10)
            
            return resp.status_code == 200
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def send_security_alert(self, event: str, details: str):
        """发送安全告警"""
        self.send(f"*{event}*\n\n{details}", 'warning')
    
    def send_gateway_down(self):
        """Gateway宕机告警"""
        self.send("*Gateway宕机!*", 'critical')
        self.send("正在自动重启...", 'info')
    
    def send_gateway_recovered(self):
        """Gateway恢复"""
        self.send("*Gateway已恢复* ✅", 'info')
    
    def send_token_leak(self, count: int):
        """Token泄漏告警"""
        self.send(f"*检测到Token泄漏!*\n\n数量: {count}", 'critical')
    
    def send_login_failed(self, user_id: str, ip: str):
        """登录失败告警"""
        self.send(f"*登录失败*\n\n用户: {user_id}\nIP: {ip}", 'warning')


# 全局实例
_alert = None

def get_telegram_alerts() -> TelegramAlerts:
    global _alert
    if _alert is None:
        _alert = TelegramAlerts()
    return _alert

def send_alert(message: str, level: str = 'info'):
    return get_telegram_alerts().send(message, level)


# 测试
if __name__ == "__main__":
    print("=== Telegram Alert 测试 ===\n")
    
    alerts = get_telegram_alerts()
    
    if alerts.enabled:
        alerts.send("测试消息", 'info')
    else:
        print("⚠️ 未配置Telegram")
        print("需要设置环境变量:")
        print("  TELEGRAM_BOT_TOKEN")
        print("  TELEGRAM_CHAT_ID")
