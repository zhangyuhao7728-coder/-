#!/usr/bin/env python3
"""
AI Coding Academy - Web应用入口
"""
import streamlit as st
import sys
import os

# 添加路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 页面配置
st.set_page_config(
    page_title="🎓 AI Coding Academy",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 侧边栏
st.sidebar.title("🎓 AI Coding Academy")
st.sidebar.markdown("---")

# 菜单
menu = st.sidebar.selectbox(
    "功能菜单",
    ["🏠 首页", "📚 学习路径", "📝 每日任务", "💻 在线代码", "🤖 AI导师", "📊 学习进度", "🏆 挑战", "🐛 Debug训练"]
)

# 首页
if menu == "🏠 首页":
    st.title("🎓 AI Coding Academy")
    st.markdown("### AI驱动的Python学习平台")
    
    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("等级", "Lv.1", "↑1")
    with col2:
        st.metric("学习时间", "0分钟", "+30")
    with col3:
        st.metric("解题数", "0", "+5")
    with col4:
        st.metric("项目数", "0", "+1")
    
    st.markdown("---")
    
    # 快速开始
    st.subheader("🚀 快速开始")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 开始学习"):
            st.success("开始今天的Python学习！")
    with col2:
        if st.button("💻 写代码"):
            st.info("进入代码实验室")
    with col3:
        if st.button("🤖 问AI导师"):
            st.info("向AI导师提问")

# 学习路径
elif menu == "📚 学习路径":
    st.title("📚 学习路径")
    
    paths = [
        {"name": "Python基础", "duration": "4周", "desc": "变量、函数、循环", "progress": 0},
        {"name": "Python进阶", "duration": "4周", "desc": "装饰器、OOP、异步", "progress": 0},
        {"name": "算法与数据结构", "duration": "4周", "desc": "数组、链表、树", "progress": 0},
        {"name": "AI/ML入门", "duration": "4周", "desc": "NumPy、PyTorch", "progress": 0},
    ]
    
    for path in paths:
        with st.expander(f"{path['name']} ({path['duration']})"):
            st.progress(path['progress'] / 100)
            st.caption(f"{path['desc']} - 进度: {path['progress']}%")
            if st.button(f"开始学习", key=path['name']):
                st.success(f"开始 {path['name']}!")

# 每日任务
elif menu == "📝 每日任务":
    st.title("📝 今日任务")
    
    tasks = [
        {"title": "学习Python基础: 变量和数据类型", "time": "20分钟", "points": 10},
        {"title": "完成5道基础算法题", "time": "30分钟", "points": 20},
        {"title": "编写Hello World练习", "time": "10分钟", "points": 5},
        {"title": "复习昨天知识", "time": "15分钟", "points": 5},
    ]
    
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.checkbox("", key=f"task_{i}")
        with col2:
            st.markdown(f"**{task['title']}**")
            st.caption(f"⏱️ {task['time']} | +{task['points']}分")
        with col3:
            st.write("")
            if st.button("开始", key=f"do_{i}"):
                st.balloons()
                st.success("完成!")
    
    st.markdown("---")
    st.metric("今日目标", f"{len(tasks)}个任务", f"+{sum(t['points'] for t in tasks)}分")

# 在线代码
elif menu == "💻 在线代码":
    st.title("💻 在线代码实验室")
    
    # 代码输入
    code = st.text_area(
        "Python代码",
        "print('Hello, Python!')\n\n# 在这里编写你的代码",
        height=300,
        help="输入Python代码并运行"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        run_btn = st.button("▶️ 运行代码", type="primary")
    with col2:
        clear_btn = st.button("🗑️ 清空")
    
    if clear_btn:
        code = ""
        st.rerun()
    
    if run_btn and code:
        st.markdown("### 📤 运行结果")
        
        # 运行代码
        import subprocess
        import tempfile
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ["python3", temp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.stdout:
                st.code(result.stdout, language="output")
            if result.stderr:
                st.error(result.stderr)
            
            os.unlink(temp_file)
            
        except subprocess.TimeoutExpired:
            st.error("❌ 代码执行超时")
        except Exception as e:
            st.error(f"❌ 错误: {e}")

# AI导师
elif menu == "🤖 AI导师":
    st.title("🤖 AI导师")
    
    # 问题输入
    question = st.text_input("💬 输入你的问题", placeholder="例如: 什么是Python函数?")
    
    if st.button("🔍 提问", type="primary") and question:
        with st.spinner("AI正在思考..."):
            # 模拟AI回答
            import requests
            
            try:
                resp = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "qwen2.5:14b", "prompt": f"作为Python导师，简洁回答: {question}", "stream": False},
                    timeout=30
                )
                
                if resp.status_code == 200:
                    answer = resp.json().get("response", "")
                    st.success("✅ AI回答:")
                    st.markdown(answer)
                else:
                    st.warning("AI暂时无法回答，请检查Ollama服务")
            except:
                st.warning("AI服务暂不可用")
    
    st.markdown("---")
    
    # 常见问题
    st.subheader("💡 常见问题")
    
    faqs = [
        ("什么是变量?", "变量是用来存储数据的容器"),
        ("什么是函数?", "函数是可以重复使用的代码块"),
        ("什么是列表?", "列表是有序的数据集合"),
    ]
    
    for q, a in faqs:
        with st.expander(q):
            st.markdown(a)

# 学习进度
elif menu == "📊 学习进度":
    st.title("📊 学习进度")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 统计")
        st.metric("总学习时间", "0分钟")
        st.metric("解题数", "0道")
        st.metric("项目数", "0个")
        st.metric("连续学习", "0天")
    
    with col2:
        st.subheader("🌳 技能树")
        skills = [
            ("Python基础", 100),
            ("函数", 50),
            ("列表", 30),
            ("字典", 0),
            ("循环", 0),
        ]
        
        for skill, progress in skills:
            st.markdown(f"**{skill}**")
            st.progress(progress / 100)
            st.caption(f"{progress}%")

# 挑战
elif menu == "🏆 挑战":
    st.title("🏆 编程挑战")
    
    challenges = [
        {"title": "两数之和", "difficulty": "easy", "points": 10, "desc": "给定数组和目标值，找出两数之和"},
        {"title": "反转链表", "difficulty": "medium", "points": 30, "desc": "反转单链表"},
        {"title": "LRU缓存", "difficulty": "hard", "points": 50, "desc": "设计LRU缓存"},
    ]
    
    for ch in challenges:
        diff_color = "🟢" if ch["difficulty"] == "easy" else "🟡" if ch["difficulty"] == "medium" else "🔴"
        
        with st.expander(f"{diff_color} {ch['title']} (+{ch['points']}分)"):
            st.markdown(ch["desc"])
            if st.button(f"开始挑战", key=ch["title"]):
                st.success("挑战开始!")

# Debug训练
elif menu == "🐛 Debug训练":
    st.title("🐛 Debug训练")
    
    bugs = [
        {"title": "Off-by-one错误", "code": "for i in range(1, 10):\n    print(i)", "hint": "range范围是左闭右开"},
        {"title": "变量作用域", "code": "x = 10\ndef foo():\n    x = x + 1\n    return x", "hint": "需要使用global关键字"},
    ]
    
    for bug in bugs:
        with st.expander(f"🔧 {bug['title']}"):
            st.code(bug["code"], language="python")
            st.info(f"💡 提示: {bug['hint']}")
            
            answer = st.text_input("修复方案:", key=bug["title"])
            if st.button("提交", key=f"submit_{bug['title']}"):
                if answer:
                    st.success("提交成功!")

# 页脚
st.markdown("---")
st.caption("🎓 AI Coding Academy v1.0 | AI驱动的Python学习平台")
