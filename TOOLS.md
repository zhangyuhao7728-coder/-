# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 公众号文章助手

位置：`~/项目/Ai学习系统/projects/公众号文章助手/`

### 快速使用

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手
```

### 核心功能

| 功能 | 命令 |
|------|------|
| 一键生成文章 | `python publish_pipeline.py --topic "主题"` |
| 优化标题 | `python tools/文章优化.py --title "标题" --variants` |
| 风格分析 | `python tools/风格分析.py --file article.md --preview` |
| 生成封面 | `python tools/生成封面.py --title "标题" --template tech` |
| 公众号排版 | `python formatter/markdown_to_wechat.py input.md output.html` |

### 示例

```bash
# 一键生成
python publish_pipeline.py --topic "AI安全" --style 余豪风格

# 优化标题
python tools/文章优化.py --title "AI教程" --variants

# 分析风格
python tools/风格分析.py --file ~/Desktop/AI安全文章.md --preview

# 生成封面
python tools/生成封面.py --title "我的文章" --template tech
```

---

## 其他工具

### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
