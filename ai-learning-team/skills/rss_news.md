# RSS 新闻聚合 Skill

## 用途
获取 AI、科技、开发类新闻，自动翻译成中文并分类推送

## 触发词
- "获取新闻"
- "科技新闻"
- "AI新闻"
- "今日新闻"
- "新闻聚合"

## 参数
- `数量`: 获取几条新闻 (默认3)
- `分类`: AI/科技/开发/部署/全部

## 使用示例
- "获取3条AI新闻"
- "获取科技新闻"
- "获取最新新闻"

## 数据源
- Hacker News
- OpenAI Blog
- Anthropic
- Google AI
- Meta AI
- DeepMind
- OpenClaw
- Cloudflare
- Hugging Face
- Vercel
- DEV Community
- 36kr

## 功能
- [x] RSS源获取
- [x] 智能去重(80%相似度)
- [x] 本地模型翻译
- [x] 智能分类
- [x] 定时推送(每天7:30)

## 添加新闻源
修改脚本中的 RSS_SOURCES 列表

## 状态
- 定时: 每天 7:30
- 模式: 本地模型免费
