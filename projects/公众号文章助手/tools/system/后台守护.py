#!/usr/bin/env python3
"""
后台稳定守护进程
确保OpenClaw稳定运行
"""
import subprocess
import time
import os
from datetime import datetime

class OpenClawDaemon:
    def __init__(self):
        self.check_interval = 60  # 60秒检查一次
        self.log_file = os.path.expanduser("~/.openclaw/logs/daemon.log")
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {msg}\n"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, "a") as f:
            f.write(log_msg)
        print(log_msg.strip())
    
    def is_gateway_running(self):
        """检查Gateway是否运行"""
        result = subprocess.run(
            ["openclaw", "gateway", "status"],
            capture_output=True,
            text=True
        )
        return "Listening" in result.stdout
    
    def start_gateway(self):
        """启动Gateway"""
        self.log("⚠️ Gateway未运行，尝试启动...")
        result = subprocess.run(
            ["openclaw", "gateway", "start"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            self.log("✅ Gateway已启动")
            return True
        else:
            self.log(f"❌ 启动失败: {result.stderr}")
            return False
    
    def run(self):
        """运行守护进程"""
        self.log("🚀 守护进程启动")
        
        while True:
            try:
                if not self.is_gateway_running():
                    self.start_gateway()
                time.sleep(self.check_interval)
            except KeyboardInterrupt:
                self.log("🛑 守护进程停止")
                break
            except Exception as e:
                self.log(f"❌ 错误: {e}")
                time.sleep(self.check_interval)

def start_daemon():
    """启动守护进程"""
    daemon = OpenClawDaemon()
    
    # 检查是否已经在运行
    result = subprocess.run(
        ["pgrep", "-f", "后台守护.py"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("⚠️ 守护进程已在运行")
        return
    
    # 以后台模式运行
    print("🚀 启动后台守护进程...")
    subprocess.Popen(
        ["python3", __file__],
        stdout=open(os.devnull, "w"),
        stderr=open(os.devnull, "w"),
        start_new_session=True
    )
    print("✅ 守护进程已启动")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--start':
        start_daemon()
    else:
        daemon = OpenClawDaemon()
        daemon.run()
