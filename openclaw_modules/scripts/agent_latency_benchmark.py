#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例26：多Agent网络延迟基准测试
测量Agent网格通信延迟
"""

import time
import json
import os
from datetime import datetime
from statistics import median, quantiles

# 配置
RESULTS_FILE = os.path.expanduser("~/.openclaw/workspace/memory/agent_latency.json")
MAX_AGENTS = 10
TEST_ROUNDS = 5

def measure_agent_latency(agent_count):
    """测量Agent间延迟"""
    # 模拟Agent间通信延迟
    # 实际环境中需要通过实际Agent通信来测量
    
    delays = []
    for _ in range(TEST_ROUNDS):
        # 模拟延迟 (ms)
        base_latency = 50  # 基础延迟
        network_overhead = agent_count * 5  # 随节点增加
        random_factor = 10  # 随机波动
        
        delay = base_latency + network_overhead + random_factor
        delays.append(delay)
    
    return delays

def run_benchmark():
    """运行基准测试"""
    print("\n🌐 多Agent网络延迟基准测试")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"测试轮数: {TEST_ROUNDS}")
    print(f"最大Agent数: {MAX_AGENTS}")
    print("="*50)
    
    results = []
    
    # 测试不同Agent数量
    for count in range(1, MAX_AGENTS + 1):
        delays = measure_agent_latency(count)
        
        avg_delay = sum(delays) / len(delays)
        p50 = median(delays)
        
        # 计算P95/P99
        if len(delays) >= 4:
            try:
                p = quantiles(delays, n=100)
                p95 = p[94]
                p99 = p[98]
            except:
                p95 = max(delays)
                p99 = max(delays)
        else:
            p95 = max(delays)
            p99 = max(delays)
        
        result = {
            "agent_count": count,
            "avg_latency_ms": round(avg_delay, 2),
            "p50_ms": round(p50, 2),
            "p95_ms": round(p95, 2),
            "p99_ms": round(p99, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        results.append(result)
        
        print(f"\n{count} Agent(s):")
        print(f"   平均: {result['avg_latency_ms']}ms")
        print(f"   P50:  {result['p50_ms']}ms")
        print(f"   P95:  {result['p95_ms']}ms")
        print(f"   P99:  {result['p99_ms']}ms")
    
    # 保存结果
    save_results(results)
    
    # 检测异常
    detect_anomalies(results)
    
    return results

def save_results(results):
    """保存结果"""
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    
    # 加载历史
    history = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            history = json.load(f)
    
    # 添加新结果
    history.extend(results)
    
    # 只保留最近100条
    history = history[-100:]
    
    with open(RESULTS_FILE, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"\n✅ 结果已保存到: {RESULTS_FILE}")

def detect_anomalies(results):
    """检测异常"""
    if len(results) < 2:
        return
    
    # 检查延迟突变
    latest = results[-1]
    previous = results[-2]
    
    latency_jump = latest["avg_latency_ms"] - previous["avg_latency_ms"]
    
    if latency_jump > 30:  # 30ms突变阈值
        print(f"\n⚠️ 检测到延迟突变!")
        print(f"   {previous['agent_count']} → {latest['agent_count']} Agent(s)")
        print(f"   延迟增加: +{latency_jump:.1f}ms")
    else:
        print(f"\n✅ 延迟正常，无异常")

def main():
    run_benchmark()

if __name__ == "__main__":
    run_benchmark()
