#!/bin/bash
# =============================================================================
# Browser System 启动脚本
# =============================================================================

cd "$(dirname "$0")"

echo "🛡 Running system guard..."
nohup python3 system_guard.py > logs/guard.log 2>&1 &

echo "🚀 Starting worker..."
while true; do
    python3 worker.py
    echo "⚠ Worker crashed. Restarting..."
    sleep 2
done
