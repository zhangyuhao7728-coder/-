# =============================================================================
# Skill: Browser API - 浏览器控制
# =============================================================================

## 基本信息
- **ID**: browser_api
- **Name**: Browser_Controller
- **Agent**: 所有 Agent 均可使用

## 简介
通过 HTTP API 控制浏览器集群，执行自动化网页操作

## 依赖
- browser_cluster 服务 (Docker)
- Playwright

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 服务状态 |
| `/browser/{instance_id}` | POST | 执行浏览器操作 |
| `/browser/{instance_id}/screenshot` | GET | 获取截图 |
| `/browser/{instance_id}/cookies` | POST | 设置 Cookies |
| `/instances` | GET | 列出实例 |
| `/instances/{instance_id}/close` | POST | 关闭实例 |

## 支持的操作

| 操作 | 参数 | 说明 |
|------|------|------|
| `navigate` | url | 访问 URL |
| `click` | selector | 点击元素 |
| `fill` | selector, value | 填写表单 |
| `screenshot` | - | 截图 |
| `get_html` | - | 获取页面 HTML |
| `evaluate` | script | 执行 JS |
| `wait_for_selector` | selector | 等待元素 |

## 使用示例

### 1. 访问网页
```bash
curl -X POST http://localhost:8000/browser/1 \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.google.com",
    "action": "navigate"
  }'
```

### 2. 截图
```bash
curl -X GET http://localhost:8000/browser/1/screenshot
```

### 3. 登录并操作
```bash
# 1. 访问登录页
curl -X POST http://localhost:8000/browser/1 \
  -d '{"url": "https://twitter.com/login", "action": "navigate"}'

# 2. 填写用户名
curl -X POST http://localhost:8000/browser/1 \
  -d '{"action": "fill", "selector": "input[name=username]", "value": "your_user"}'

# 3. 填写密码
curl -X POST http://localhost:8000/browser/1 \
  -d '{"action": "fill", "selector": "input[name=password]", "value": "your_pass"}'

# 4. 点击登录
curl -X POST http://localhost:8000/browser/1 \
  -d '{"action": "click", "selector": "button[type=submit]"}'
```

## 在 Agent 中的使用

### Engineer Skill
```python
# 使用浏览器自动化
async def auto_fill_form():
    await browser_api.navigate("https://example.com")
    await browser_api.fill("input[name=email]", "test@example.com")
    await browser_api.click("button[type=submit]")
    screenshot = await browser_api.screenshot()
    return screenshot
```

### Researcher Skill
```python
# 抓取动态网页
async def fetch_dynamic_page(url: str):
    await browser_api.navigate(url)
    html = await browser_api.get_html()
    return html
```

## 注意事项

1. **实例管理**: 用完记得关闭实例释放资源
2. **Cookies**: 重要网站建议预先配置 Cookies
3. **反爬**: 建议使用代理 + 真实 User-Agent
4. **并发**: 建议最多 5 个并发实例

## Docker 启动

```bash
cd browser_cluster
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

## 故障排查

| 问题 | 解决 |
|------|------|
| 浏览器启动失败 | 检查 Docker 资源 |
| 无法连接 | 确认端口 8000 开放 |
| 被反爬 | 更换 IP / 使用代理 |
| 截图模糊 | 调整 viewport 参数 |
