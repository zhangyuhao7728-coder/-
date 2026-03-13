#!/usr/bin/env python3
"""
Python AI 学习系统 v4.0 - 主入口
"""
import sys
import os

# 添加路径
sys.path.insert(0, '/Users/zhangyuhao/项目/Ai学习系统/learning')

# 颜色定义
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RED = '\033[91m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_banner():
    print(f"""
{CYAN}╔═══════════════════════════════════════════════════════╗
║                                                       ║
║    🐍 Python AI 学习系统 v4.0                        ║
║    AI驱动自适应学习平台                             ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝{RESET}
    """)

def print_menu():
    print(f"""
{BOLD}请选择功能:{RESET}

{GREEN}📚 学习模块{RESET}
  1. 开始学习 (每日任务)
  2. 学习路径
  3. 技能树
  4. 每日任务

{BLUE}🏆 训练模块{RESET}
  5. 编程竞技场
  6. Debug训练
  7. 系统设计训练
  8. 项目训练

{YELLOW}🔍 分析模块{RESET}
  9. 学习统计
  10. 弱点分析
  11. AI代码审查

{CYAN}🌐 面板{RESET}
  12. 启动Web仪表盘
  13. 启动Streamlit面板
  14. 查看学习报告

{RED}❌ 退出{RESET}
  0. 退出
    """)

def main():
    os.system('clear')
    print_banner()
    
    while True:
        print_menu()
        choice = input(f"{BOLD}请选择 (0-14): {RESET}")
        
        if choice == '0':
            print(f"{CYAN}再见！继续学习吧！{RESET}")
            break
        
        elif choice == '1':
            print(f"\n{GREEN}=== 每日学习 ==={RESET}")
            from scripts.start_learning import start_learning
            start_learning()
        
        elif choice == '2':
            print(f"\n{GREEN}=== 学习路径 ==={RESET}")
            from learning_engine.learning_path import get_learning_path
            lp = get_learning_path()
            for path in lp.get_all_paths():
                print(f"  📚 {path['name']} ({path['duration']})")
        
        elif choice == '3':
            print(f"\n{GREEN}=== 技能树 ==={RESET}")
            from progress.skill_tree import get_skill_tree
            tree = get_skill_tree()
            tree.print_tree()
        
        elif choice == '4':
            print(f"\n{GREEN}=== 今日任务 ==={RESET}")
            from learning_engine.task_scheduler import get_today_plan
            print(get_today_plan())
        
        elif choice == '5':
            print(f"\n{BLUE}=== 编程竞技场 ==={RESET}")
            from coding_arena.arena_engine import get_arena
            arena = get_arena()
            ch = arena.start_challenge()
            print(f"挑战: {ch['title']}")
            print(f"难度: {ch['difficulty']}")
            print(f"分数: +{ch['points']}")
        
        elif choice == '6':
            print(f"\n{BLUE}=== Debug训练 ==={RESET}")
            from debugging_trainer.trainer import get_debugging_trainer
            debug = get_debugging_trainer()
            ex = debug.get_exercise()
            print(f"练习: {ex['title']}")
            print(f"代码:\n{ex['buggy_code']}")
            print(f"提示: {ex['hint']}")
        
        elif choice == '7':
            print(f"\n{BLUE}=== 系统设计 ==={RESET}")
            from system_design.trainer import get_system_design_trainer
            design = get_system_design_trainer()
            prob = design.get_problem()
            print(f"题目: {prob['title']}")
            print(f"难度: {prob['difficulty']}")
            for q in prob.get('questions', []):
                print(f"  - {q}")
        
        elif choice == '8':
            print(f"\n{BLUE}=== 项目训练 ==={RESET}")
            from projects.project_trainer import get_project_trainer
            trainer = get_project_trainer()
            print("初级项目:")
            for p in trainer.get_projects("beginner"):
                print(f"  - {p['name']}: {p['description']}")
        
        elif choice == '9':
            print(f"\n{YELLOW}=== 学习统计 ==={RESET}")
            from progress.learning_stats import get_learning_stats
            stats = get_learning_stats()
            stats.print_summary()
        
        elif choice == '10':
            print(f"\n{YELLOW}=== 弱点分析 ==={RESET}")
            from learning_analytics.weakness_detector import get_weakness_detector
            detector = get_weakness_detector()
            # 添加一些示例错误
            detector.add_error("语法错误", "变量")
            detector.add_error("逻辑错误", "循环")
            weaknesses = detector.detect_weakness()
            for w in weaknesses:
                print(f"  ⚠️ {w['skill']}: {w['advice']}")
        
        elif choice == '11':
            print(f"\n{YELLOW}=== AI代码审查 ==={RESET}")
            from ai_code_reviewer.reviewer import get_ai_code_reviewer
            reviewer = get_ai_code_reviewer()
            code = "def hello():\n    x = 1\n    print(x)"
            result = reviewer.review(code)
            print(f"评分: {result['score']}")
            print(f"问题: {result['issues']}")
        
        elif choice == '12':
            print(f"\n{CYAN}=== 启动Web仪表盘 ==={RESET}")
            print("请在浏览器打开:")
            print(f"  file://{os.path.expanduser('~')}/项目/Ai学习系统/learning/dashboard/index_v2.html")
        
        elif choice == '13':
            print(f"\n{CYAN}=== 启动Streamlit面板 ==={RESET}")
            print("运行命令:")
            print(f"  streamlit run {os.path.expanduser('~')}/项目/Ai学习系统/learning/dashboard/streamlit_dashboard_v2.py")
        
        elif choice == '14':
            print(f"\n{CYAN}=== 学习报告 ==={RESET}")
            from progress.learning_stats import get_learning_stats
            stats = get_learning_stats()
            total = stats.get_total()
            print(f"""
📊 学习报告
━━━━━━━━━━━━━━━━━━
🕐 总学习时间: {total['total_time']}分钟
📝 解题数: {total['problems']}道
💻 项目数: {total['projects']}个
⭐ 等级: Lv.{stats.get_level()}
━━━━━━━━━━━━━━━━━━
            """)
        
        else:
            print(f"{RED}无效选择，请重试{RESET}")
        
        input(f"\n按回车继续...")


if __name__ == "__main__":
    main()
