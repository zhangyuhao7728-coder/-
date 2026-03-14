# 🎓 AI Coding Academy

AI驱动的Python学习平台

## 🚀 快速启动

### 方式1: 启动脚本
```bash
open ~/项目/ai-coding-academy/start_app.sh
```

### 方式2: 命令行
```bash
streamlit run ~/项目/ai-coding-academy/app/app.py
```

### 方式3: 桌面应用 (macOS)

#### 创建桌面应用步骤:

1️⃣ **打开Automator**
```bash
open -a Automator
```

2️⃣ **新建Application**
- 文件 → 新建
- 选择 "应用程序"

3️⃣ **添加操作**
- 搜索 "Run Shell Script"
- 拖到右侧

4️⃣ **输入脚本**
```bash
/Users/zhangyuhao/项目/ai-coding-academy/start_app.sh
```

5️⃣ **保存**
- 文件 → 存储
- 名称: AI Coding Academy
- 保存到: 应用程序

## 📁 项目结构

```
ai-coding-academy/
├── app/
│   └── app.py          # Streamlit主应用
├── code_lab/
│   └── code_runner.py  # 代码运行器
├── progress/
│   └── progress_tracker.py
├── scripts/
│   └── daily_tasks.py
└── start_app.sh        # 启动脚本
```

## 🔧 功能

- 📚 学习路径
- 📝 每日任务
- 💻 在线代码运行
- 🤖 AI导师
- 📊 学习进度
- 🏆 编程挑战

## 🌐 访问

启动后访问: http://localhost:8501
