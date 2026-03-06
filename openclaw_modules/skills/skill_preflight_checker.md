# 技能安装前安全预检 - 用例34

## 用途
安装新技能前进行安全检查，避免恶意代码

## 触发词
- "安全预检"
- "检查技能"
- "技能安全"

## 预检清单

### 1. 作者信誉检查
- 检查作者是否在可信列表
- 可信: openclaw, evolinkai, anthropic, claude, github

### 2. package.json检查
- 检查 scripts 字段
- 警惕 postinstall 脚本
- 检查可疑依赖

### 3. 危险代码模式
- eval(), exec()
- curl, wget
- rm -rf
- 访问 .ssh, .env

### 4. 文件访问检查
- 敏感目录访问
- 凭据文件访问

## 红灯信号 🔴
- postinstall 脚本
- 访问 ~/.ssh 或 ~/.env
- 作者信息不明

## 命令

| 命令 | 说明 |
|------|------|
| `安全预检` | 检查指定技能 |
| `安全预检 /path skill` | 自定义路径 |

## 示例

```bash
python scripts/skill_preflight_checker.py skills/github
python scripts/skill_preflight_checker.py /path/to/skill openclaw
```

## 状态
- ✅ 已安装
- ⏳ 可手动运行
