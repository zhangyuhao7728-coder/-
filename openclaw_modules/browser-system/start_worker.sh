#!/bin/bash

# 防止多实例
LOCK_FILE="logs/worker.lock"
if [ -f "$LOCK_FILE" ]; then
    echo "Worker already running."
    exit 0
fi
touch "$LOCK_FILE"

echo "🚀 Starting worker..."
echo "📊 Health Report:"
echo "==================="
echo "Timestamp: $(date)"
echo "Gateway: http://localhost:8000"
echo "Redis: localhost:6379"

# 发送健康报告（这里可以配置Telegram/飞书等）
curl -s http://localhost:8000/health 2>/dev/null && echo "" || echo "⚠️ Gateway异常"

# 监控并启动 worker
while true; do
    python3 worker.py
    echo "⚠ Worker crashed. Restarting in 2 seconds..."
    sleep 2
done
