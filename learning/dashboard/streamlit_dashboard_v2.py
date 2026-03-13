#!/usr/bin/env python3
"""
Python学习系统 - 完整版仪表盘
"""
import streamlit as st
import sys
import os

# 添加路径
sys.path.insert(0, '/Users/zhangyuhao/项目/Ai学习系统/learning')

# 页面配置
st.set_page_config(
    page_title="🐍 Python AI 学习系统",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 导入模块
from progress.learning_stats import get_learning_stats
from progress.skill_tree import get_skill_tree
from learning_engine.study_planner import get_study_planner
from learning_engine.task_scheduler import generate_daily_tasks
from coding_arena.arena_engine import get_arena
from debugging_trainer.trainer import get_debugging_trainer
from system_design.trainer import get_system_design_trainer

# 侧边栏
st.sidebar.title("🎓 学习系统")
st.sidebar.markdown("---")

# 菜单
menu = st.sidebar.selectbox(
    "选择功能",
    ["🏠 首页", "📚 学习路径", "📋 每日任务", "🌳 技能树", "🏆 竞技场", "🐛 Debug训练", "📐 系统设计", "📊 统计"]
)

# 加载数据
stats = get_learning_stats()
total = stats.get_total()
tree = get_skill_tree()
planner = get_study_planner()
tasks = generate_daily_tasks("beginner")

# 首页
if menu == "🏠 首页":
    st.title("🐍 Python AI 学习系统 v4.0")
    st.markdown("### AI驱动自适应学习平台")
    
    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("等级", f"Lv.{stats.get_level()}", "↑1")
    with col2:
        st.metric("学习时间", f"{total['total_time']}分钟", "+30")
    with col3:
        st.metric("解题数", total['problems'], "+5")
    with col4:
        st.metric("项目数", total['projects'], "+1")
    
    st.markdown("---")
    
    # 今日任务
    st.subheader("📋 今日任务")
    today_task = planner.get_today_task()
    st.info(f"**{today_task['task']}**")
    
    # 快速开始
    st.subheader("🚀 快速开始")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎯 开始学习"):
            st.success("开始今天的Python学习！")
    with col2:
        if st.button("🏆 参加挑战"):
            arena = get_arena()
            ch = arena.start_challenge()
            st.info(f"挑战: {ch['title']}")
    with col3:
        if st.button("🐛 Debug训练"):
            debug = get_debugging_trainer()
            ex = debug.get_exercise()
            st.info(f"练习: {ex['title']}")

# 学习路径
elif menu == "📚 学习路径":
    st.title("📚 学习路径")
    
    paths = [
        {"name": "Python基础", "duration": "4周", "progress": 0, "color": "blue"},
        {"name": "Python进阶", "duration": "4周", "progress": 0, "color": "green"},
        {"name": "算法与数据结构", "duration": "4周", "progress": 0, "color": "orange"},
        {"name": "AI/ML入门", "duration": "4周", "progress": 0, "color": "red"},
        {"name": "数据技能", "duration": "3周", "progress": 0, "color": "purple"},
    ]
    
    for path in paths:
        with st.expander(f"{path['name']} ({path['duration']})"):
            st.progress(path['progress'] / 100)
            st.caption(f"进度: {path['progress']}%")
            st.button(f"开始学习", key=path['name'])

# 每日任务
elif menu == "📋 每日任务":
    st.title("📋 今日任务")
    
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.checkbox("", key=f"task_{i}")
        with col2:
            st.markdown(f"**{task['title']}**")
            st.caption(f"⏱️ {task['duration']} | +{task['points']}分")
        with col3:
            st.write("")
            if st.button("开始", key=f"do_{i}"):
                st.success("开始执行！")
    
    st.markdown("---")
    st.metric("今日目标", f"{len(tasks)}个任务", f"+{sum(t['points'] for t in tasks)}分")

# 技能树
elif menu == "🌳 技能树":
    st.title("🌳 技能树")
    
    skills = tree.skills
    unlocked = tree.get_unlocked()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for skill, info in skills.items():
            status = "✅" if skill in unlocked else "🔒"
            mastery = info.get("mastery", 0)
            
            st.markdown(f"{status} **{skill}**")
            st.progress(mastery / 100)
    
    with col2:
        st.subheader("技能详情")
        st.info("解锁更多技能需要通过学习和完成任务来提升掌握度！")

# 竞技场
elif menu == "🏆 竞技场":
    st.title("🏆 编程竞技场")
    
    arena = get_arena()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 挑战")
        challenge_type = st.selectbox("选择类型", ["algorithm", "optimization", "bugfix", "architecture"])
        
        if st.button("开始挑战"):
            ch = arena.start_challenge(challenge_type)
            st.success(f"挑战: {ch['title']} (+{ch['points']}分)")
    
    with col2:
        st.subheader("📊 状态")
        status = arena.get_status()
        if status.get("active"):
            st.info(f"进行中: {status.get('challenge')}")
            st.metric("剩余时间", f"{status.get('remaining', 0)}秒")
        else:
            st.info("暂无进行中的挑战")

# Debug训练
elif menu == "🐛 Debug训练":
    st.title("🐛 Debug训练")
    
    debug = get_debugging_trainer()
    ex = debug.get_exercise()
    
    st.subheader("当前练习")
    st.error(f"**{ex['title']}**")
    
    st.code(ex['buggy_code'], language="python")
    
    st.info(f"💡 提示: {ex['hint']}")
    
    solution = st.text_input("请输入修复方案:")
    
    if st.button("提交"):
        result = debug.check_solution(solution)
        if result['correct']:
            st.success("✅ 回答正确！")
        else:
            st.warning("❌ 再试一次")

# 系统设计
elif menu == "📐 系统设计":
    st.title("📐 系统设计训练")
    
    design = get_system_design_trainer()
    problem = design.get_problem()
    
    st.subheader("设计题目")
    st.info(f"**{problem['title']}**")
    st.caption(f"难度: {problem['difficulty']}")
    
    st.subheader("需要考虑的问题")
    for q in problem.get('questions', []):
        st.markdown(f"- {q}")
    
    st.subheader("你的设计")
    design_input = st.text_area("描述你的设计方案:")
    
    if st.button("提交设计"):
        result = design.evaluate_design(design_input)
        st.success(f"评分: {result['score']}/100")
        st.info(f"反馈: {result['feedback']}")

# 统计
elif menu == "📊 统计":
    st.title("📊 学习统计")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("总览")
        st.metric("总学习时间", f"{total['total_time']}分钟")
        st.metric("解题数", total['problems'])
        st.metric("项目数", total['projects'])
        st.metric("技能数", len(total.get('skills', {})))
    
    with col2:
        st.subheader("效率")
        analyzer = __import__('learning_analytics.performance_analyzer', fromlist=['get_performance_analyzer']).get_performance_analyzer()
        eff = analyzer.analyze(total)
        st.metric("学习效率", f"{eff['efficiency']}")
        st.info(f"评级: {eff['rating']}")

# 页脚
st.markdown("---")
st.caption("🐍 Python AI 学习系统 v4.0 | AI驱动自适应学习")
