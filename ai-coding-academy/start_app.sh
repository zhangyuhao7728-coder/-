#!/bin/bash
# AI Coding Academy 启动脚本
# 支持虚拟环境和直接运行

# 项目路径
PROJECT_DIR="/Users/zhangyuhao/项目/ai-coding-academy"
APP_FILE="$PROJECT_DIR/app/app.py"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎓 启动 AI Coding Academy...${NC}"

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"

# 检查Streamlit
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}📦 安装 Streamlit...${NC}"
    pip install streamlit
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Streamlit 安装失败${NC}"
        exit 1
    fi
fi

echo "✅ Streamlit: $(python3 -c 'import streamlit; print(streamlit.__version__)')"

# 检查Ollama
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "✅ Ollama: 运行中"
else
    echo -e "${YELLOW}⚠️ Ollama 未运行 (可选)${NC}"
    echo "   启动命令: ollama serve"
fi

# 检查Gateway
if curl -s http://127.0.0.1:18789/health &> /dev/null; then
    echo "✅ Gateway: 运行中"
else
    echo -e "${YELLOW}⚠️ Gateway 未运行 (可选)${NC}"
fi

echo ""
echo -e "${GREEN}🚀 启动Web应用...${NC}"
echo "   地址: http://localhost:8501"
echo "   按 Ctrl+C 停止"
echo ""

# 启动Streamlit
cd "$PROJECT_DIR"
streamlit run "$APP_FILE" \
    --server.port 8501 \
    --server.address localhost \
    --server.headless true \
    --browser.gatherUsageStats false
