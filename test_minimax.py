import anthropic
import httpx

# 强制禁用系统代理
http_client = httpx.Client(trust_env=False)

client = anthropic.Anthropic(
    base_url="https://api.minimax.io/anthropic",
    api_key="sk-api-famwp1gWcOGdldsemWdw0nqZoFNGYZ0seOO0iaqgpUS8b1LHKdIpD05SMS8cMuuTMiTUMc7xEnbDGdpIbrdywQoO94CTedRg-WN6MiPbhN7x7pC65gwTNkA",
    http_client=http_client
)

response = client.messages.create(
    model="MiniMax-M2.5",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "用一句话解释人工智能"}
    ]
)

print(response.content[0].text)
