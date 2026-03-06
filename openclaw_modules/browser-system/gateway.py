#!/usr/bin/env python3
"""
Browser System Gateway - 简洁版 5 接口
"""

import uuid
import json
import time
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import REDIS_URL, GATEWAY_PORT

app = FastAPI()
r = redis.Redis.from_url(REDIS_URL)

# ===== 数据模型 =====

class TaskRequest(BaseModel):
    url: str
    action: str = "visit"

class TaskResponse(BaseModel):
    task_id: str
    status: str

# ===== 任务状态 =====
# pending → running → done / failed

def create_task_entry(task_id: str, url: str) -> dict:
    """创建任务条目"""
    return {
        "task_id": task_id,
        "url": url,
        "status": "pending",
        "created_at": int(time.time()),
        "result": None,
        "error": None
    }

# ===== 5 个接口 =====

@app.post("/task", response_model=TaskResponse)
def create_task(req: TaskRequest):
    """1. POST /task → 提交浏览任务"""
    task_id = str(uuid.uuid4())[:8]
    
    # 存储任务详情
    task = create_task_entry(task_id, req.url)
    r.set(f"task:{task_id}", json.dumps(task))
    
    # 加入队列
    r.lpush("browser_queue", f"{task_id}|{req.url}")
    
    return TaskResponse(task_id=task_id, status="pending")

@app.get("/result/{task_id}")
def get_result(task_id: str):
    """2. GET /result/<task_id> → 查询结果"""
    task_data = r.get(f"task:{task_id}")
    
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = json.loads(task_data)
    return task

@app.get("/queue_status")
def queue_status():
    """3. GET /queue_status → 队列状态"""
    return {
        "queue_length": r.llen("browser_queue"),
        "processing": r.get("processing") or 0
    }

@app.get("/health")
def health():
    """4. GET /health → 节点健康"""
    try:
        r.ping()
        return {"status": "ok", "redis": "connected"}
    except:
        return {"status": "error", "redis": "disconnected"}

@app.delete("/task/{task_id}")
def cancel_task(task_id: str):
    """5. DELETE /task/<task_id> → 取消任务"""
    task_data = r.get(f"task:{task_id}")
    
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = json.loads(task_data)
    task["status"] = "cancelled"
    r.set(f"task:{task_id}", json.dumps(task))
    
    return {"task_id": task_id, "status": "cancelled"}

# ===== 根路径 =====
@app.get("/")
def root():
    return {
        "service": "Browser Gateway",
        "endpoints": [
            "POST /task",
            "GET /result/{task_id}",
            "GET /queue_status",
            "GET /health",
            "DELETE /task/{task_id}"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=GATEWAY_PORT)
