#!/usr/bin/env python3
"""
成本控制模块
"""

import json
import time
from datetime import datetime, timedelta
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 成本配置
DAILY_LIMIT = 1000  # 每日限制
MONTHLY_BUDGET = 50  # 每月预算 (美元)

def get_usage():
    """获取使用量"""
    return {
        "today_tokens": r.get("cost:tokens:today") or 0,
        "monthly_tokens": r.get("cost:tokens:month") or 0,
        "today_cost": r.get("cost:daily") or 0,
        "monthly_cost": r.get("cost:monthly") or 0
    }

def check_limits():
    """检查是否超限"""
    usage = get_usage()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "daily_limit": DAILY_LIMIT,
        "monthly_budget": MONTHLY_BUDGET,
        "usage": usage,
        "status": "ok"
    }
    
    # 检查每日限制
    if int(usage.get("today_tokens", 0)) > DAILY_LIMIT:
        result["status"] = "warning"
        result["alert"] = "今日Token超限"
    
    # 检查每月预算
    monthly_cost = float(usage.get("monthly_cost", 0))
    if monthly_cost > MONTHLY_BUDGET:
        result["status"] = "critical"
        result["alert"] = "本月预算超支"
    
    return result

def record_usage(tokens, cost):
    """记录使用量"""
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")
    
    # 累计今日
    r.incrby("cost:tokens:today", tokens)
    r.set(f"cost:tokens:{today}", r.get("cost:tokens:today") or 0)  # 持久化
    r.incrbyfloat("cost:daily", cost)
    
    # 累计本月
    r.incrby("cost:tokens:month", tokens)
    r.set(f"cost:tokens:{month}", r.get("cost:tokens:month") or 0)
    r.incrbyfloat("cost:monthly", cost)
    
    # 设置过期
    r.expire(f"cost:tokens:{today}", 86400 * 2)
    r.expire(f"cost:tokens:{month}", 86400 * 32)

def reset_daily():
    """重置每日"""
    r.set("cost:tokens:today", 0)
    r.set("cost:daily", 0)

def reset_monthly():
    """重置每月"""
    r.set("cost:tokens:month", 0)
    r.set("cost:monthly", 0)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "check":
            print(json.dumps(check_limits(), indent=2))
        elif cmd == "usage":
            print(json.dumps(get_usage(), indent=2))
        elif cmd == "reset":
            reset_daily()
            print("已重置")
        else:
            print("Commands: check, usage, reset")
    else:
        print(json.dumps(check_limits(), indent=2))
