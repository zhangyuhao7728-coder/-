#!/usr/bin/env python3
"""
System Guard - 自动清理
"""

import os
import time
import redis
import logging

BASE_DIR = os.path.expanduser("~/.openclaw")
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
LOCK_DIR = BASE_DIR

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

LOG_FILE = "system_guard.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

MAX_TRANSCRIPTS = 50
MAX_DAYS = 7

def cleanup_locks():
    """清理孤立 lock 文件"""
    for file in os.listdir(LOCK_DIR):
        if file.endswith(".lock"):
            path = os.path.join(LOCK_DIR, file)
            if os.path.exists(path):
                os.remove(path)
                logging.info(f"Removed orphan lock: {file}")

def cleanup_transcripts():
    """清理超量/超期 transcript"""
    if not os.path.exists(TRANSCRIPT_DIR):
        return
    
    files = sorted(
        [os.path.join(TRANSCRIPT_DIR, f) for f in os.listdir(TRANSCRIPT_DIR)],
        key=lambda x: os.path.getmtime(x)
    )
    
    # 超过最大数量删除最旧
    while len(files) > MAX_TRANSCRIPTS:
        old = files.pop(0)
        os.remove(old)
        logging.info(f"Removed old transcript: {old}")
    
    # 超过 7 天删除
    now = time.time()
    for file in files:
        if now - os.path.getmtime(file) > MAX_DAYS * 86400:
            os.remove(file)
            logging.info(f"Removed expired transcript: {file}")

def cleanup_tasks():
    """清理超时任务 (24小时)"""
    for key in r.scan_iter("task:*"):
        created_at = r.hget(key, "created_at")
        status = r.hget(key, "status")
        if created_at and status in ["pending", "running"]:
            if time.time() - float(created_at) > 86400:
                r.hset(key, "status", "failed")
                r.hset(key, "error", "Task expired")
                logging.info(f"Expired task: {key}")

if __name__ == "__main__":
    cleanup_locks()
    cleanup_transcripts()
    cleanup_tasks()
    logging.info("System guard cleanup completed.")
