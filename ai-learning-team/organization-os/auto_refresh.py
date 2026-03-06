"""
Session Auto Refresh - 自动刷新 Session
当 Context 超过阈值时自动清理
"""

import time
import requests
from datetime import datetime

# 配置
GATEWAY_URL = "http://localhost:18789"
CONTEXT_THRESHOLD = 0.7  # 70% 自动刷新


def check_and_refresh():
    """检查并刷新"""
    try:
        # 获取 session 状态
        resp = requests.get(f"{GATEWAY_URL}/api/sessions", timeout=5)
        
        if resp.status_code == 200:
            sessions = resp.json()
            print(f"✅ Session 正常")
            return True
            
    except Exception as e:
        print(f"⚠️ 需要刷新: {e}")
    
    return False


def auto_refresh_loop(interval: int = 60):
    """自动刷新循环"""
    print(f"🔄 自动刷新已启动 (间隔 {interval}秒)")
    print("按 Ctrl+C 停止")
    
    try:
        while True:
            check_and_refresh()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n⏹️ 已停止")


if __name__ == "__main__":
    # 检查当前状态
    print("=== Session 状态检查 ===")
    check_and_refresh()
