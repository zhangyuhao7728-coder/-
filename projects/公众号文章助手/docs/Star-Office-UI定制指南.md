# Star-Office-UI 像素人物定制指南

## 定制方法

### 方法1：通过网页侧边栏（推荐）

1. 打开 http://127.0.0.1:19000
2. 点击右侧 **侧边栏按钮**
3. 在侧边栏中可以自定义：

| 功能 | 说明 |
|------|------|
| 角色形象 | 上传/更换AI角色图片 |
| 场景背景 | 更换办公室背景 |
| 装饰物品 | 添加植物、宠物等 |
| AI生图 | 用Gemini生成新背景 |

### 方法2：配置文件

编辑 `asset-positions.json` 自定义物品位置：

```json
{
  "我的角色.webp": {
    "x": 100.0,
    "y": 200.0,
    "scale": 1.0
  }
}
```

### 方法3：上传素材

在 `assets/` 目录添加图片文件，支持格式：
- PNG
- WebP
- GIF（动画）

---

## 状态说明

| 状态 | 行为 |
|------|------|
| idle | 休息/待机 |
| writing | 写作中 |
| researching | 研究中 |
| executing | 执行中 |
| syncing | 同步中 |
| error | 报错/Bug区 |

---

## API控制状态

```bash
# 设置状态
curl -X POST http://127.0.0.1:19000/api/state \
  -H "Content-Type: application/json" \
  -d '{"state":"writing","detail":"写文章中"}'
```

---

*2026-03-14*
