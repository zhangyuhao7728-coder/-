#!/usr/bin/env python3
"""
Browser System Config
"""

import os

# Redis 配置
REDIS_URL = "redis://localhost:6379"

# Gateway 配置
GATEWAY_HOST = "0.0.0.0"
GATEWAY_PORT = 8000

# Worker 配置 - 动态调整
MAX_CONCURRENCY = 3  # 默认并发数

# 浏览器配置
HEADLESS = True
PAGE_TIMEOUT = 30_000  # 毫秒

# 任务配置
MAX_QUEUE_SIZE = 100
TASK_TIMEOUT = 30_000  # 毫秒

# 基本系统预算与任务控制
DAILY_LIMIT = 1000
MONTHLY_BUDGET = 50

# 自动调整并发数的函数
def adjust_concurrency(queue_length):
    global MAX_CONCURRENCY
    if queue_length > 100:
        MAX_CONCURRENCY = 5
    else:
        MAX_CONCURRENCY = 3
    return MAX_CONCURRENCY

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# 确保目录存在
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
