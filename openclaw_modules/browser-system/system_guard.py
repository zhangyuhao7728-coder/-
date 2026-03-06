#!/usr/bin/env python3
"""
System Guard - 守护进程
"""

import os
import sys
import time
import redis
import logging
import psutil

# 防止多实例
LOCK_FILE = "logs/system_guard.lock"
if os.path.exists(LOCK_FILE):
    print("Guard already running.")
    sys.exit(0)
open(LOCK_FILE, "w").close()

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

BASE_DIR = os.path.expanduser("~/.openclaw")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "system_guard.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_TRANSCRIPTS = 50
MAX_DAYS = 7
TASK_TIMEOUT = 86400  # 24h
MAX_BROWSER_PROCESSES = 5

def log(msg):
    print(msg)
    logging.info(msg)

# ---------- 清理锁 ----------
def cleanup_locks():
    for file in os.listdir(BASE_DIR):
        if file.endswith(".lock"):
            path = os.path.join(BASE_DIR, file)
            try:
                os.remove(path)
                log(f"Removed orphan lock: {file}")
            except:
                pass

# ---------- 清理 transcript ----------
def cleanup_transcripts():
    if not os.path.exists(TRANSCRIPT_DIR):
        return
    
    files = sorted(
        [os.path.join(TRANSCRIPT_DIR, f) for f in os.listdir(TRANSCRIPT_DIR)],
        key=lambda x: os.path.getmtime(x)
    )
    
    while len(files) > MAX_TRANSCRIPTS:
        old = files.pop(0)
        os.remove(old)
        log(f"Removed old transcript: {old}")
    
    now = time.time()
    for file in files:
        if now - os.path.getmtime(file) > MAX_DAYS * 86400:
            os.remove(file)
            log(f"Removed expired transcript: {file}")

# ---------- 任务超时 ----------
def cleanup_tasks():
    for key in r.scan_iter("task:*"):
        created_at = r.hget(key, "created_at")
        status = r.hget(key, "status")
        if created_at and status in ["pending", "running"]:
            if time.time() - float(created_at) > TASK_TIMEOUT:
                r.hset(key, mapping={
                    "status": "failed",
                    "error": "Task expired"
                })
                log(f"Expired task: {key}")

# ---------- 浏览器进程检查 ----------
def check_browser_processes():
    count = 0
    for proc in psutil.process_iter(['name']):
        try:
            if "Chromium" in proc.info['name'] or "chrome" in proc.info['name']:
                count += 1
        except:
            pass
    
    if count > MAX_BROWSER_PROCESSES:
        log(f"⚠ Too many browser processes: {count}")
    else:
        log(f"Browser processes: {count}")

# ---------- 内存检查 ----------
def check_memory():
    mem = psutil.virtual_memory()
    used_mb = mem.used / 1024 / 1024
    log(f"Memory used: {int(used_mb)} MB")

# ---------- 主循环 ----------
def guard_loop():
    log("🛡 System Guard started")
    
    while True:
        try:
            cleanup_locks()
            cleanup_transcripts()
            cleanup_tasks()
            check_browser_processes()
            check_memory()
        except Exception as e:
            log(f"Guard error: {e}")
        
        time.sleep(600)  # 每10分钟巡检

if __name__ == "__main__":
    guard_loop()
