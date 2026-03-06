from openai import OpenAI
import os

# 强烈建议你已经 export 过 API_KEY
# 如果没设置，可以临时写在这里：
# os.environ["OPENAI_API_KEY"] = "sk-cp-no567420hQwdNDBJEV9-TG-y46h6_X9ubSppY-7DQz8D2XStFeJwtR1JibfWZQBFMVQaibM7QJcRtQzFgzkPcaZg7rX3FkhKs3Fgrjf7Ev8KWmYz8lbebzQ"
# os.environ["OPENAI_BASE_URL"] = "https://api.minimaxi.com/v1"

client = OpenAI()

response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好，请简单介绍自己"},
    ],
    extra_body={"reasoning_split": True},
    temperature=1.0,
)

print("=== Response ===")
print(response.choices[0].message.content)
