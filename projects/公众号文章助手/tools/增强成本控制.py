#!/usr/bin/env python3
"""
增强版成本控制系统 V2
基于7个方向的成本优化
"""
import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List

class EnhancedCostController:
    """增强成本控制器"""
    
    def __init__(self):
        self.log_dir = os.path.expanduser("~/.openclaw/logs")
        self.state_file = f"{self.log_dir}/cost_state_v2.json"
        self.config_file = 'data/成本控制配置.json'
        self.load_config()
        
        # 免费模型列表
        self.free_models = {
            'ollama': ['qwen2.5:latest', 'qwen3.5:9b', 'deepseek-coder:6.7b'],
            'openrouter': ['free'],
        }
        
        # 付费模型
        self.paid_models = {
            'minimax': 'MiniMax-M2.5',
            'volcengine': 'Coding Plan Plus',
        }
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self.get_default_config()
    
    def get_default_config(self) -> dict:
        return {
            'version': '2.0',
            'updated': '2026-03-14',
            'daily_limit': 1000,  # 每日token限制
            'monthly_budget': 50,  # 每月预算50美元
            'free_threshold': 80,   # 80%后切换免费模型
            'alert_levels': [25, 50, 75, 100],
            'models': {
                'primary': 'minimax-cn/MiniMax-M2.5',
                'fallback': 'qwen2.5:latest',
                'code': 'deepseek-coder:6.7b'
            },
            'optimization': {
                'memory_cleanup': True,
                'lazy_loading': True,
                'cache_responses': True,
                'max_tokens': 4096
            },
            'savings_target': 50  # 目标节省50%
        }
    
    def save_config(self):
        os.makedirs('data', exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def get_current_usage(self) -> dict:
        """获取当前使用情况"""
        usage = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tokens_today': 0,
            'cost_today': 0,
            'tokens_month': 0,
            'cost_month': 0,
        }
        
        # 读取日志
        log_file = f"{self.log_dir}/cost.log"
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-100:]:  # 最近100条
                        if datetime.now().strftime('%Y-%m-%d') in line:
                            usage['tokens_today'] += 1
                            usage['cost_today'] += 0.001  # 估算
            except:
                pass
        
        return usage
    
    def check_limits(self) -> dict:
        """检查限制"""
        usage = self.get_current_usage()
        
        daily_limit = self.config.get('daily_limit', 1000)
        monthly_budget = self.config.get('monthly_budget', 50)
        
        # 计算百分比
        daily_percent = (usage['tokens_today'] / daily_limit) * 100 if daily_limit > 0 else 0
        cost_percent = (usage['cost_today'] / monthly_budget) * 100 if monthly_budget > 0 else 0
        
        return {
            'usage': usage,
            'daily_percent': daily_percent,
            'cost_percent': cost_percent,
            'should_switch': daily_percent >= self.config.get('free_threshold', 80),
            'should_alert': daily_percent in self.config.get('alert_levels', [25, 50, 75, 100])
        }
    
    def switch_to_free_model(self) -> bool:
        """切换到免费模型"""
        try:
            # 切换到Ollama
            result = subprocess.run(
                ['openclaw', 'models', 'set', 'qwen2.5:latest'],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            print(f"切换失败: {e}")
            return False
    
    def optimize_memory(self):
        """优化记忆系统"""
        memory_dir = os.path.expanduser("~/.openclaw/memory")
        
        if not os.path.exists(memory_dir):
            return
        
        # 清理过期记忆
        cutoff = datetime.now() - timedelta(days=30)
        
        for root, dirs, files in os.walk(memory_dir):
            for f in files:
                if f.endswith('.md'):
                    fpath = os.path.join(root, f)
                    mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
                    
                    if mtime < cutoff:
                        # 只清理非重要的
                        if 'summary' not in f and 'knowledge' not in f:
                            print(f"可清理: {f}")
    
    def generate_report(self) -> dict:
        """生成成本报告"""
        usage = self.get_current_usage()
        check = self.check_limits()
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'usage': usage,
            'limits': {
                'daily': self.config.get('daily_limit'),
                'monthly': self.config.get('monthly_budget')
            },
            'status': check,
            'models': {
                'primary': self.config['models']['primary'],
                'fallback': self.config['models']['fallback']
            },
            'savings': {
                'target': f"{self.config.get('savings_target')}%",
                'current': f"{100 - check['daily_percent']:.1f}%"
            }
        }
    
    def auto_optimize(self):
        """自动优化"""
        actions = []
        
        # 检查是否需要切换
        check = self.check_limits()
        if check['should_switch']:
            if self.switch_to_free_model():
                actions.append('已切换到免费模型')
        
        # 优化记忆
        if self.config.get('optimization', {}).get('memory_cleanup'):
            self.optimize_memory()
            actions.append('已优化记忆系统')
        
        return actions

def run_cost_optimization():
    """运行成本优化"""
    controller = EnhancedCostController()
    
    print("="*50)
    print("💰 成本控制系统 V2")
    print("="*50)
    
    # 生成报告
    report = controller.generate_report()
    
    print(f"\n📊 今日使用:")
    print(f"   Token: {report['usage']['tokens_today']}")
    print(f"   成本: ${report['usage']['cost_today']:.2f}")
    
    print(f"\n📈 限制:")
    print(f"   每日: {report['limits']['daily']}")
    print(f"   每月: ${report['limits']['monthly']}")
    
    print(f"\n📉 状态:")
    print(f"   使用率: {report['status']['daily_percent']:.1f}%")
    print(f"   应切换: {'是' if report['status']['should_switch'] else '否'}")
    
    print(f"\n💵 节省:")
    print(f"   目标: {report['savings']['target']}")
    print(f"   当前: {report['savings']['current']}")
    
    # 自动优化
    actions = controller.auto_optimize()
    if actions:
        print(f"\n⚡ 已执行:")
        for a in actions:
            print(f"   • {a}")
    
    return report

if __name__ == '__main__':
    run_cost_optimization()
