"""
Organization Core HTTP Server
FastAPI + EventBus + Task Queue + SQLite 持久化 + Risk Manager
Stability Edition v2.3.0
"""

import logging
import json
import psutil
import os
import threading
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import time

from organization_core.core_runtime import OrganizationCore
from organization_core.agents import (
    ceo_handle,
    planner_handle,
    researcher_handle,
    engineer_handle,
    reviewer_handle,
    analyst_handle
)
from organization_core.persistence.db import init_db
from persistence.database import Database, get_database
from config.budget_config import BUDGET_CONFIG
from risk_manager import RiskManager

# ===== 结构化日志配置 =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("org_core")

def log_event(level: str, event: dict):
    """结构化日志"""
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "level": level,
        **event
    }
    logger.info(json.dumps(log_data))

# ===== 健康监控线程 =====
class SystemMonitor:
    """系统健康监控"""
    
    def __init__(self, interval: int = 600):  # 10分钟
        self.interval = interval
        self.running = False
        self.thread = None
        self.process = psutil.Process(os.getpid())
    
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("SystemMonitor started (interval: 600s)")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def _monitor_loop(self):
        while self.running:
            try:
                mem_info = self.process.memory_info()
                cpu_percent = self.process.cpu_percent()
                
                log_event("INFO", {
                    "type": "system_health",
                    "memory_mb": mem_info.rss / 1024 / 1024,
                    "cpu_percent": cpu_percent,
                    "threads": self.process.num_threads()
                })
            except Exception as e:
                logger.error(f"Monitor error: {e}")
            
            time.sleep(self.interval)

# 启动系统监控
system_monitor = SystemMonitor()

# 初始化数据库
init_db()

# 创建数据库和 Risk Manager 实例
db = get_database()
risk_manager = RiskManager(db, BUDGET_CONFIG)

# 创建 FastAPI 应用
app = FastAPI(
    title="Organization Core API",
    description="AI Learning Team - 事件驱动 + 任务队列 + 持久化 + 风险管理 + 稳定性",
    version="2.3.0"
)

# ===== 全局异常处理 (必须在 app 创建后) =====
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常拦截"""
    error_info = {
        "path": str(request.url),
        "method": request.method,
        "error": str(exc),
        "type": type(exc).__name__
    }
    
    log_event("ERROR", {
        "type": "exception",
        **error_info
    })
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "SYSTEM_ERROR",
            "message": "An internal error occurred"
        }
    )

# 创建 Organization Core 实例 (4 workers)
core = OrganizationCore(max_workers=4, risk_manager=risk_manager)

# 注册所有 Agent
core.register_agent("ceo", ceo_handle)
core.register_agent("planner", planner_handle)
core.register_agent("researcher", researcher_handle)
core.register_agent("engineer", engineer_handle)
core.register_agent("reviewer", reviewer_handle)
core.register_agent("analyst", analyst_handle)


# ========== 数据模型 ==========

class Message(BaseModel):
    """消息模型"""
    content: str
    sender: Optional[str] = None
    channel: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageSync(BaseModel):
    """同步消息模型"""
    content: str
    sender: Optional[str] = None
    channel: Optional[str] = None


class Response(BaseModel):
    """响应模型"""
    status: str
    task_id: Optional[int] = None
    agent: str
    message: str
    data: Optional[Dict[str, Any]] = None


# ========== API 路由 ==========

@app.get("/")
def root():
    """健康检查"""
    return {
        "status": "ok",
        "service": "Organization Core",
        "version": "2.3.0",
        "agents": core.list_agents()
    }


@app.get("/health")
def health():
    """健康检查"""
    return {"status": "healthy"}


@app.get("/agents")
def list_agents():
    """列出所有已注册的 Agent"""
    return {
        "agents": core.list_agents(),
        "count": len(core.list_agents())
    }


@app.get("/stats")
def get_stats():
    """获取队列统计"""
    return core.get_stats()


@app.get("/tasks")
def list_tasks(status: str = None, limit: int = 100):
    """列出任务"""
    tasks = core.list_tasks(status, limit)
    return {
        "tasks": tasks,
        "count": len(tasks)
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """获取任务详情"""
    task = core.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/message", response_model=Response)
def receive_message(message: Message):
    """异步接收消息 - 通过任务队列"""
    try:
        # 检查风险锁定
        agent = core.scheduler.decide(message.model_dump())
        
        if risk_manager.is_locked(agent):
            raise HTTPException(
                status_code=403,
                detail=f"[SECURITY] {agent} is locked due to CRITICAL risk"
            )
        
        # 构建消息字典
        msg_dict = message.model_dump()
        
        # 通过 EventBus 发送消息（非阻塞）
        core.receive_message(msg_dict)
        
        return Response(
            status="queued",
            task_id=None,
            agent=agent,
            message="Message queued for async processing"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/message/sync", response_model=Response)
def receive_message_sync(message: MessageSync):
    """同步接收消息 - 直接执行"""
    try:
        # 检查风险锁定
        agent = core.scheduler.decide(message.model_dump())
        
        if risk_manager.is_locked(agent):
            raise HTTPException(
                status_code=403,
                detail=f"[SECURITY] {agent} is locked due to CRITICAL risk"
            )
        
        msg_dict = message.model_dump()
        
        # 同步执行
        result = core.receive_message_sync(msg_dict)
        
        return Response(
            status="completed",
            agent=agent,
            message="Message processed synchronously",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/route")
def route_message(message: Message):
    """手动路由消息"""
    try:
        msg_dict = message.model_dump()
        
        # 直接调度
        agent_name = core.scheduler.decide(msg_dict)
        
        # 检查风险
        if risk_manager.is_locked(agent_name):
            raise HTTPException(
                status_code=403,
                detail=f"[SECURITY] {agent_name} is locked due to CRITICAL risk"
            )
        
        # 入队
        task_id = core.task_queue.enqueue(
            msg_dict["content"], 
            agent_name,
            {"sender": msg_dict.get("sender"), "channel": msg_dict.get("channel")}
        )
        
        return {
            "status": "queued",
            "task_id": task_id,
            "agent": agent_name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Risk Management 端点 ==========

@app.get("/risk")
def get_risk_summary(agent: str = None):
    """获取风险摘要"""
    return risk_manager.get_risk_summary(agent)


@app.get("/risk/events")
def get_risk_events(agent: str = None, limit: int = 100):
    """获取风险事件列表"""
    events = db.get_risk_events(agent, limit)
    return {
        "events": events,
        "count": len(events)
    }


@app.get("/risk/locked")
def get_locked_agents():
    """获取被锁定的 Agent"""
    locked = []
    for agent in BUDGET_CONFIG.keys():
        if risk_manager.is_locked(agent):
            locked.append(agent)
    return {"locked": locked}


@app.post("/risk/check")
def check_risk(agent: str):
    """手动检查风险"""
    risk_manager.check(agent)
    return {
        "agent": agent,
        "locked": risk_manager.is_locked(agent),
        "budget": risk_manager.get_budget(agent)
    }


@app.post("/risk/cost")
def record_cost(agent: str, cost: float = 10.0):
    """记录成本"""
    db.insert_cost(agent, cost)
    risk_manager.check(agent)
    return {
        "agent": agent,
        "cost_recorded": cost,
        "today_cost": db.get_today_cost(agent)
    }


@app.post("/risk/override")
def record_override(agent: str):
    """记录 Override"""
    db.insert_override(agent)
    risk_manager.check(agent)
    return {
        "agent": agent,
        "override_recorded": True,
        "today_count": db.get_today_override_count(agent)
    }


@app.get("/risk/budget")
def get_budgets():
    """获取所有预算配置"""
    return {"budgets": BUDGET_CONFIG}


@app.post("/risk/budget/{agent}")
def set_budget(agent: str, budget: float):
    """设置预算"""
    if agent not in BUDGET_CONFIG:
        raise HTTPException(status_code=404, detail="Agent not found")
    risk_manager.set_budget(agent, budget)
    return {"agent": agent, "budget": budget}


# ========== LLM 端点 ==========

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    provider: Optional[str] = None


@app.post("/llm/chat")
def llm_chat(request: ChatRequest):
    """直接调用 LLM (测试用)"""
    try:
        result = core.chat_with_llm(request.message, request.provider)
        return {
            "status": "ok",
            "message": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== 启动入口 ==========

def main():
    """启动服务器"""
    # 启动系统监控
    system_monitor.start()
    
    print("=" * 50)
    print("🚀 Starting Organization Core Server v2.3.0")
    print("=" * 50)
    print("📡 API: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print(f"🤖 Agents: {core.list_agents()}")
    print("📊 Features:")
    print("   - EventBus: ✅")
    print("   - Task Queue (限流+并发): ✅")
    print("   - SQLite Persistence (WAL): ✅")
    print("   - Worker Pool (超时保护): ✅")
    print("   - Risk Manager v3.0 (持久化): ✅")
    print("   - LLM Health Monitor: ✅")
    print("   - Global Exception Handler: ✅")
    print("   - Structured Logging: ✅")
    print("   - System Monitor: ✅")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
