# 🤖 AI 智能返利系统

> 状态: 🛑 待重启

> 基于 AI 的淘宝/京东商品搜索 + 返利链接生成

## 📋 项目简介

通过 AI 对话方式搜索商品，自动生成返利链接，用户购买后可获得佣金。

## 🚀 快速开始

```bash
cd ~/项目/AI返利系统
npm start
```

访问: http://localhost:3001

## 📡 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/affiliate/search` | GET | 搜索商品+返利链接 |
| `/api/affiliate/link` | POST | 生成返利链接 |

## 🔧 配置

编辑 `config.json`:

```json
{
  "affiliate": {
    "alimama": {
      "pid": "你的PID",
      "enabled": true
    }
  }
}
```

##

```
用户: "帮我搜i 💰 商业流程Phone"
  ↓
AI返回: 商品列表 + 返利链接
  ↓
用户点击购买
  ↓
获得佣金
```

---

**PID**: mm_10013873396_3397400377_116242050304
