#!/usr/bin/env python3
"""
安全警报系统
检测到威胁时自动发送警报
"""
import json
import os
from datetime import datetime

class SecurityAlerter:
    """安全警报系统"""
    
    def __init__(self):
        self.alert_log = os.path.expanduser("~/.openclaw/logs/security_alerts.json")
        os.makedirs(os.path.dirname(self.alert_log), exist_ok=True)
        
        # 警报级别
        self.levels = {
            'critical': '🔴 严重',
            'high': '🟠 高危',
            'medium': '🟡 中等',
            'low': '🟢 低'
        }
    
    def load_alerts(self):
        if os.path.exists(self.alert_log):
            with open(self.alert_log, 'r') as f:
                return json.load(f)
        return []
    
    def save_alerts(self, alerts):
        with open(self.alert_log, 'w') as f:
            json.dump(alerts, f, indent=2, ensure_ascii=False)
    
    def create_alert(self, level: str, title: str, details: str, source: str = '自动检测'):
        """创建警报"""
        alert = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'level': level,
            'level_name': self.levels.get(level, '未知'),
            'title': title,
            'details': details,
            'source': source,
            'timestamp': datetime.now().isoformat(),
            'status': 'unread'
        }
        
        # 保存
        alerts = self.load_alerts()
        alerts.append(alert)
        alerts = alerts[-50:]  # 只保留50条
        self.save_alerts(alerts)
        
        return alert
    
    def send_telegram_alert(self, alert: dict):
        """发送Telegram警报"""
        try:
            from message import action
            message = f"""
{alert['level_name']} 安全警报

🚨 {alert['title']}

📝 详情: {alert['details']}

⏰ 时间: {alert['timestamp']}
📍 来源: {alert['source']}

🆔 ID: {alert['id']}
"""
            # 这里简化处理，实际会调用message工具
            print(f"📨 发送Telegram警报...")
            return True
        except:
            return False
    
    def notify(self, level: str, title: str, details: str, source: str = '自动检测'):
        """发送警报"""
        # 创建警报
        alert = self.create_alert(level, title, details, source)
        
        # 打印警报
        print(f"\n{'='*50}")
        print(f"{alert['level_name']} 安全警报")
        print(f"{'='*50}")
        print(f"🚨 {title}")
        print(f"📝 {details}")
        print(f"⏰ {alert['timestamp']}")
        print(f"{'='*50}\n")
        
        # 发送Telegram（高级别才发送）
        if level in ['critical', 'high']:
            self.send_telegram_alert(alert)
        
        return alert
    
    def get_recent_alerts(self, limit: int = 10):
        """获取最近警报"""
        alerts = self.load_alerts()
        return alerts[-limit:]


# 与防御系统集成
def alert_on_threat(threat_type: str, details: str, level: str = 'high'):
    """检测到威胁时触发警报"""
    alerter = SecurityAlerter()
    
    titles = {
        'dangerous_command': '危险命令检测',
        'suspicious_url': '可疑URL',
        'malware': '恶意程序',
        'phishing': '钓鱼链接',
        'credential_leak': '凭证泄露'
    }
    
    title = titles.get(threat_type, '安全威胁')
    
    return alerter.notify(level, title, details)


# 测试
if __name__ == '__main__':
    alerter = SecurityAlerter()
    
    print("🔔 安全警报系统")
    print("="*50)
    
    # 测试警报
    alert_on_threat('dangerous_command', '发现危险命令: rm -rf /', 'high')
    
    # 查看最近警报
    print("\n📋 最近警报:")
    for a in alerter.get_recent_alerts(5):
        print(f"  {a['level_name']} {a['title']} - {a['timestamp']}")
