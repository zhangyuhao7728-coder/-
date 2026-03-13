#!/usr/bin/env python3
"""
Streamlit Dashboard - Streamlit面板
"""
import streamlit as st
import sys
sys.path.insert(0, '/Users/zhangyuhao/项目/Ai学习系统/learning')

from progress.learning_stats import get_learning_stats
from progress.skill_tree import get_skill_tree
from learning_engine.study_planner import get_study_planner


def main():
    """Streamlit面板"""
    
    st.set_page_config(page_title="Python学习面板", page_icon="🐍")
    
    st.title("🐍 Python学习系统")
    st.markdown("AI驱动自适应学习平台")
    
    # 统计
    stats = get_learning_stats()
    total = stats.get_total()
    
    # 指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("等级", f"Lv.{stats.get_level()}")
    col2.metric("学习时间", f"{total['total_time']}分钟")
    col3.metric("解题数", total['problems'])
    col4.metric("项目数", total['projects'])
    
    # 学习进度
    st.subheader("📚 学习进度")
    progress = st.progress(0)
    st.caption("Python基础 - 0%")
    
    # 技能树
    st.subheader("🌳 技能树")
    tree = get_skill_tree()
    skills = tree.get_unlocked()
    for skill in skills[:5]:
        st.success(f"✅ {skill}")
    
    # 今日任务
    st.subheader("📋 今日任务")
    planner = get_study_planner()
    task = planner.get_today_task()
    st.info(f"**{task['task']}**")


if __name__ == "__main__":
    main()
