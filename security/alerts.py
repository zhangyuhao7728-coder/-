#!/usr/bin/env python3
"""
Alerts Module - 报警模块
功能：
1. 多种报警方式
2. 报警历史
3. 报警级别
"""
import os
import requests
from typing import Dict, List, Optional
from datetime import datetime


class AlertManager:
    """报警管理器"""
    
    # 报警级别
    LEVELS = {
        'info': 'ℹ️ 信息',
        'warning': '🟡 警告',
        'error': '🔴 错误',
        'critical': '🚨 严重'
    }
    
    def __init__(self):
        """初始化"""
        self.alerts: List[dict] = []
        self.telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        self.telegram_chat_id = os.environ.get('TELEGRAM_CHAT_ID', '')
    
    def send_telegram(self, message: str, level: str = 'info') -> bool:
        """发送 Telegram 报警"""
        if not self.telegram_token:
            print(f"⚠️ Telegram token 未设置")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            icon = self.LEVELS.get(level, 'ℹ️')
            
            requests.post(url, json={
                'chat_id': self.telegram_chat_id,
                'text': f"{icon} {message}",
                'parse_mode': 'HTML'
            }, timeout=10)
            
            return True
        except Exception as e:
            print(f"❌ Telegram 发送失败: {e}")
            return False
    
    def send(self, message: str, level: str = 'info', title: str = '安全报警'):
        """发送报警"""
        # 记录
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'title': title,
            'message': message
        }
        
        self.alerts.append(alert)
        
        # 打印
        icon = self.LEVELS.get(level, 'ℹ️')
        print(f"{icon} [{title}] {message}")
        
        # 发送 Telegram
        if level in ['error', 'critical']:
            self.send_telegram(f"🚨 {title}\n{message}", level)
    
    def get_alerts(self, limit: int = 50) -> List[dict]:
        return self.alerts[-limit:]


# 全局实例
_alert_manager = None

def get_alert_manager() -> AlertManager:
    global _alert_manager
    if _alert_manager is None:
        _alert_manager = AlertManager()
    return _alert_manager

def send_alert(message: str, level: str = 'info'):
    get_alert_manager().send(message, level)


# 测试
if __name__ == "__main__":
    alert = get_alert_manager()
    
    print("=== Alert Manager 测试 ===\n")
    
    alert.send("测试信息", "info")
    alert.send("测试警告", "warning")
    alert.send("测试错误", "error")
    alert.send("测试严重", "critical")
