#!/bin/bash
# 自动清理上下文脚本

echo "清理memory文件..."

# 只保留最近7天的memory
find ~/.openclaw/workspace/memory/ -name "*.md" -mtime +7 -exec rm {} \;

echo "完成!"
