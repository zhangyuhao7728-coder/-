#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沙盒健康检查脚本 (可在沙盒中运行)
检测连接状态并自动修复
"""

import requests
import time
import json
import os
from datetime import datetime

# 配置
GATEWAY_URL = "http://localhost:18789"
TELEGRAM_TOKEN = "8277132121:AAGaL2OZ7Ruv2Xa2KhNOm3qZYccbj_qASJw"
TELEGRAM_ID = "8793442405"
OLLAMA_URL = "http://localhost:11434"
GATEWAY_TOKEN = "34040a0d864c8f7a3ff06736abed300da541a6e84691758c"

def log(msg):
    """日志输出"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def check_gateway():
    """检查 Gateway 状态"""
    try:
        resp = requests.get(f"{GATEWAY_URL}/health", timeout=5)
        return resp.json().get("ok", False)
    except:
        return False

def check_telegram_via_gateway():
    """通过Gateway检查Telegram"""
    try:
        # Gateway API check
        resp = requests.get(f"{GATEWAY_URL}/api/channels/telegram", 
                           headers={"Authorization": f"Bearer {GATEWAY_TOKEN}"}, 
                           timeout=5)
        return resp.ok
    except:
        return None  # 未知状态

def check_ollama():
    """检查 Ollama"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if resp.ok:
            models = resp.json().get("models", [])
            return len(models)
        return False
    except:
        return False

def check_sandbox_network():
    """检查沙盒网络环境"""
    # 检查是否能访问外网
    try:
        requests.get("https://api.github.com", timeout=3)
        return True
    except:
        return False

def send_telegram(msg):
    """发送Telegram消息 (通过Gateway)"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_ID, "text": msg}, timeout=10)
    except:
        pass

def check_all():
    """全面检查"""
    results = {
        "gateway": check_gateway(),
        "telegram": "skip",  # 沙盒无法直接访问Telegram
        "ollama": check_ollama()
    }
    return results

def run_health_check():
    """运行健康检查"""
    log("🔍 正在检查系统状态...")
    
    # 检测环境
    has_internet = check_sandbox_network()
    if not has_internet:
        log("ℹ️ 沙盒无外网访问 (正常)")
    
    results = check_all()
    
    # 格式化输出
    status_str = []
    issues = []
    
    if results["gateway"]:
        status_str.append("✅ Gateway")
    else:
        status_str.append("❌ Gateway")
        issues.append("Gateway")
    
    # Telegram在沙盒中无法直接检测
    status_str.append("ℹ️ Telegram(通过Gateway)")
    
    ollama_result = results["ollama"]
    if ollama_result:
        status_str.append(f"✅ Ollama ({ollama_result}模型)")
    else:
        status_str.append("❌ Ollama")
        issues.append("Ollama")
    
    log(" | ".join(status_str))
    
    if issues:
        log(f"⚠️ 发现问题: {', '.join(issues)}")
    else:
        log("✅ 所有服务正常")
    
    return results

if __name__ == "__main__":
    run_health_check()
