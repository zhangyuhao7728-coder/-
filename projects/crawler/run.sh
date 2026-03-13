#!/bin/bash
# 爬虫启动器

cd "$(dirname "$0")"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 检查依赖
python3 -c "import requests, bs4" 2>/dev/null || {
    echo "📦 安装依赖..."
    pip install requests beautifulsoup4
}

echo "🚀 启动爬虫..."
echo ""

# 默认：爬取3页，保存为 JSON
if [ "$1" == "all" ]; then
    # 爬取全部页面
    python3 crawler.py -p 0 -f all
elif [ "$1" == "test" ]; then
    # 测试：只爬1页
    python3 crawler.py -p 1
elif [ "$1" == "3pages" ]; then
    # 爬3页
    python3 crawler.py -p 3
else
    # 默认
    python3 crawler.py -p 3
fi
