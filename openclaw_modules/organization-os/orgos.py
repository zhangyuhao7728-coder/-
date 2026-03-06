"""
Organization OS - 核心系统（最终版）
"""

import yaml
import time
import json

from agent_bus import AgentBus
from router import route
from session_guard import guard, add_message
from logger import log

# 加载 Agent 配置
with open("agents.yaml") as f:
    agents = yaml.safe_load(f)["agents"]

# 加载路由配置
with open("openclaw.json") as f:
    config = json.load(f)

# 初始化
bus = AgentBus()

for a in agents:
    bus.register(a)

log("🔥 Organization OS started")

# 发送初始任务
bus.send("system", "ceo", "创建AI项目")

# 运行循环
cycle = 0
while cycle < 3:  # 运行 3 轮
    cycle += 1
    log(f"--- Cycle {cycle} ---")
    
    for name, meta in agents.items():
        msg = bus.receive(name)
        
        if msg:
            log(f"{name} received {msg}")
            
            # 选择模型
            model = route(meta)
            log(f"model -> {model['model']}")
            
            # 添加消息
            add_message({"agent": name, "msg": msg})
            
            # 检查 Session
            guard()
            
            # 转发到下一个 Agent
            bus.send(name, meta["next"], "继续任务")
    
    time.sleep(1)

log("✅ Organization OS finished")
