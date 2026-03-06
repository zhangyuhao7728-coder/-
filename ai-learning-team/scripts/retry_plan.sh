#!/bin/bash
# retry_plan.sh - 计划生成失败重试

cd ~/zhangyuhao/python/ai-learning-team

MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    echo "🔄 重试次数: $((RETRY_COUNT + 1))"
    
    ./scripts/daily_plan.sh
    
    if [ $? -eq 0 ]; then
        echo "✅ 重试成功"
        exit 0
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 10  # 等待10秒后重试
done

echo "❌ 重试失败，已达最大次数"
exit 1
