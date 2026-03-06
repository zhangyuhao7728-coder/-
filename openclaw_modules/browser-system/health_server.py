#!/usr/bin/env python3
"""
Health Server - 独立健康检查服务
"""

from fastapi import FastAPI
import psutil
import time
import redis

app = FastAPI()

START_TIME = time.time()
REDIS_URL = "redis://localhost:6379"
r = redis.Redis.from_url(REDIS_URL)

def count_chromium():
    count = 0
    for p in psutil.process_iter(['name']):
        try:
            if "Chromium" in p.info['name'] or "chrome" in p.info['name']:
                count += 1
        except:
            pass
    return count

def worker_alive():
    for p in psutil.process_iter(['cmdline']):
        try:
            if p.info['cmdline'] and "worker.py" in " ".join(p.info['cmdline']):
                return True
        except:
            pass
    return False

@app.get("/")
def root():
    return {"service": "Health Server", "version": "1.0.0"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime_seconds": int(time.time() - START_TIME),
        "memory_mb": psutil.Process().memory_info().rss // (1024 * 1024),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "worker_alive": worker_alive(),
        "browser_processes": count_chromium(),
        "redis_queue_length": r.llen("browser_queue")
    }

@app.get("/system")
def system():
    mem = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.5)
    return {
        "cpu_percent": cpu,
        "memory_percent": mem.percent,
        "memory_available_gb": mem.available / (1024**3),
        "disk_percent": psutil.disk_usage('/').percent
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
