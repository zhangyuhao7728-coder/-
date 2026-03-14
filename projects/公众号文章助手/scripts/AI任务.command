#!/bin/bash

echo "========================================"
echo "🚀 AI任务助手"
echo "========================================"
echo ""
echo "请输入任务描述："
read task

echo ""
echo "正在发送任务..."
echo ""

# 通过Telegram发送任务（如果可用）
# 或者创建任务文件

TASK_FILE=~/项目/Ai学习系统/projects/公众号文章助手/tasks/$(date +%Y%m%d%H%M%S)_task.txt

mkdir -p ~/项目/Ai学习系统/projects/公众号文章助手/tasks/

echo "$task" > "$TASK_FILE"

echo "✅ 任务已保存: $TASK_FILE"
echo ""
echo "任务内容:"
cat "$TASK_FILE"

echo ""
echo "========================================"
echo "任务已提交！"
echo "========================================"

read -p "按回车键退出..."
