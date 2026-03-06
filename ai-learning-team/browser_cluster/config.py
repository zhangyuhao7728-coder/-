#!/usr/bin/env python3
"""
Browser Cluster Config
"""

import os

# 并发配置
MAX_CONCURRENT = 2

# 浏览器配置
HEADLESS = True

# 超时配置
PAGE_TIMEOUT = 30000  # 毫秒

# Cookie 存储路径
COOKIE_PATH = "auth/cookies.json"

# API 配置
API_HOST = "0.0.0.0"
API_PORT = 8000

# 日志配置
LOG_LEVEL = "INFO"
