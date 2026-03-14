#!/bin/bash
# AI Coding Academy Automator 启动脚本
# 用于创建macOS桌面应用

PROJECT_DIR="/Users/zhangyuhao/项目/ai-coding-academy"

# 激活Python环境(如果存在)
if [ -f "$PROJECT_DIR/venv/bin/activate" ]; then
    source "$PROJECT_DIR/venv/bin/activate"
fi

# 启动应用
cd "$PROJECT_DIR"
streamlit run "$PROJECT_DIR/app/app.py" --server.port 8501
