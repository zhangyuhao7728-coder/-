#!/usr/bin/env python3
"""
Gateway 保活脚本 (沙盒版)
每5分钟检查一次，通过HTTP检测Gateway状态
"""

import requests
import time
from datetime import datetime

GATEWAY_URL = "http://localhost:18789"
OLLAMA_URL = "http://localhost:11434"
CHECK_INTERVAL = 300  # 5分钟

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def check_gateway():
    """检查Gateway是否运行"""
    try:
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        return resp.json().get("ok", False)
    except:
        return False

def check_ollama():
    """检查Ollama是否运行"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return resp.ok
    except:
        return False

def main():
    log("🔍 检查Gateway状态...")
    
    gateway_ok = check_gateway()
    ollama_ok = check_ollama()
    
    if gateway_ok:
        log("✅ Gateway运行正常")
    else:
        log("⚠️ Gateway未运行")
        log("💡 请在Mac终端执行: openclaw gateway restart")
    
    if ollama_ok:
        log("✅ Ollama运行正常")
    else:
        log("⚠️ Ollama未运行")
        log("💡 请在Mac终端执行: ollama serve")

if __name__ == "__main__":
    main()
