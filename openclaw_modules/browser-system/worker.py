#!/usr/bin/env python3
"""
Browser Worker - Redis 队列消费者
"""

import asyncio
import json
import time
import redis
from playwright.async_api import async_playwright
from config import REDIS_URL, MAX_CONCURRENCY, TASK_TIMEOUT

r = redis.Redis.from_url(REDIS_URL)
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

async def process_task(browser, task_data):
    """处理单个任务"""
    task_id, url = task_data.decode().split("|")
    
    async with semaphore:
        context = await browser.new_context()
        page = await context.new_page()

        start_time = time.time()

        # 设置状态为 running
        task = json.loads(r.get(f"task:{task_id}").decode())
        task["status"] = "running"
        task["started_at"] = int(time.time())
        r.set(f"task:{task_id}", json.dumps(task))

        try:
            await page.goto(url, timeout=TASK_TIMEOUT)
            content = await page.content()
            
            # 更新任务状态 - done
            task = json.loads(r.get(f"task:{task_id}").decode())
            task["status"] = "done"
            task["result"] = content[:1000]  # 截取部分结果
            task["completed_at"] = int(time.time())
            task["duration_ms"] = int((time.time() - start_time) * 1000)
            r.set(f"task:{task_id}", json.dumps(task))
            
            print(f"✅ {task_id} | {url} | {len(content)} bytes | {task['duration_ms']}ms")
            
        except Exception as e:
            # 更新任务为 failed
            task = json.loads(r.get(f"task:{task_id}").decode())
            task["status"] = "failed"
            task["error"] = str(e)
            task["completed_at"] = int(time.time())
            task["duration_ms"] = int((time.time() - start_time) * 1000)
            r.set(f"task:{task_id}", json.dumps(task))
            
            print(f"❌ {task_id} failed: {e}")
            
        finally:
            await context.close()

async def worker_loop():
    """Worker 循环"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        print("🚀 Worker 启动，等待任务...")
        
        while True:
            try:
                # 阻塞等待任务
                task = r.brpop("browser_queue", timeout=5)
                
                if task:
                    await process_task(browser, task[1])
                    
            except Exception as e:
                print(f"Worker error: {e}")
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(worker_loop())
