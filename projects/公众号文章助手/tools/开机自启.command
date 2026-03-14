#!/bin/bash
# OpenClaw开机自动启动

echo "🚀 启动OpenClaw Gateway..."
openclaw gateway install
openclaw gateway start

# 启动守护进程
cd ~/项目/Ai学习系统/projects/公众号文章助手
nohup python3 tools/后台守护.py > /dev/null 2>&1 &

echo "✅ OpenClaw已启动"
