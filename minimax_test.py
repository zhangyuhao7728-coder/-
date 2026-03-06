import requests
import json

api_key = "sk-api-whSA3hi6Rj7TcUA3xl055F9O3cNQQDYPJwQxQBk65sPXkF4liIjZsfhDMd3qPkxRJQKQ0EaIyCo_hcIFrvSWkW8xrNzMgl92oipudXn9NXqynsGiz-uQteg"
payload = {"model": "abab6.5s-chat", "messages": [{"role": "user", "content": "你好"}]}
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

urls = {
    "OpenAI兼容": "https://api.minimax.chat/v1/chat/completions",
    "MiniMax原生": "https://api.minimax.chat/v1/text/chatcompletion_v2"
}

for name, url in urls.items():
    print(f"正在测试: {name}...")
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"  状态码: {r.status_code}")
        print(f"  响应: {r.text[:100]}...")
    except Exception as e:
        print(f"  异常: {e}")
