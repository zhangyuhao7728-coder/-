#!/usr/bin/env python3
"""
LLM Control Panel - 模型监控面板
功能：
1. 模型状态
2. 调用统计
3. 费用监控
4. 错误率追踪
"""
import os
import json
from datetime import datetime


class LLMPanel:
    """LLM 控制面板"""
    
    STATS_DIR = os.path.expanduser("~/项目/Ai学习系统/ai-control-plane/stats")
    
    # 模型配置
    MODELS = {
        "qwen2.5:latest": {"type": "local", "cost": 0},
        "qwen2.5:7b": {"type": "local", "cost": 0},
        "qwen3.5:9b": {"type": "local", "cost": 0},
        "deepseek-coder:6.7b": {"type": "local", "cost": 0},
        "minimax/MiniMax-M2.5": {"type": "cloud", "cost": 0.002},
        "volcengine/doubao-seed-code": {"type": "cloud", "cost": 0.001},
    }
    
    def __init__(self):
        self.stats = self._load_stats()
    
    def _load_stats(self) -> dict:
        """加载统计数据"""
        stats = {}
        
        # 加载 usage
        usage_file = os.path.join(self.STATS_DIR, "usage.json")
        if os.path.exists(usage_file):
            with open(usage_file, 'r') as f:
                stats['usage'] = json.load(f)
        else:
            stats['usage'] = {}
        
        # 加载 model_usage
        model_file = os.path.join(self.STATS_DIR, "model_usage.json")
        if os.path.exists(model_file):
            with open(model_file, 'r') as f:
                stats['model_usage'] = json.load(f)
        else:
            stats['model_usage'] = {}
        
        # 加载 cost
        cost_file = os.path.join(self.STATS_DIR, "cost.json")
        if os.path.exists(cost_file):
            with open(cost_file, 'r') as f:
                stats['cost'] = json.load(f)
        else:
            stats['cost'] = {}
        
        return stats
    
    def get_model_status(self) -> dict:
        """获取模型状态"""
        import requests
        
        status = {}
        
        # 检查 Ollama
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=3)
            if r.status_code == 200:
                ollama_models = [m['name'] for m in r.json().get('models', [])]
                for model in self.MODELS:
                    if 'qwen' in model or 'deepseek' in model:
                        status[model] = {
                            'available': model in ollama_models,
                            'status': 'online' if model in ollama_models else 'offline'
                        }
        except:
            for model in self.MODELS:
                if 'qwen' in model or 'deepseek' in model:
                    status[model] = {'available': False, 'status': 'offline'}
        
        # 云模型 (简化)
        for model in ['minimax/MiniMax-M2.5', 'volcengine/doubao-seed-code']:
            status[model] = {'available': True, 'status': 'online'}
        
        return status
    
    def get_today_stats(self) -> dict:
        """获取今日统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        usage = self.stats['usage'].get(today, {})
        
        return {
            'calls': usage.get('calls', 0),
            'tokens': usage.get('tokens', 0),
            'success': usage.get('success', 0),
            'failed': usage.get('failed', 0),
            'success_rate': (usage.get('success', 0) / usage.get('calls', 1)) * 100
        }
    
    def get_model_stats(self) -> list:
        """获取模型统计"""
        model_data = self.stats.get('model_usage', {})
        
        results = []
        
        for model, config in self.MODELS.items():
            data = model_data.get(model, {})
            calls = data.get('calls', 0)
            success = data.get('success', 0)
            
            results.append({
                'name': model,
                'type': config['type'],
                'cost': config['cost'],
                'calls': calls,
                'tokens': data.get('tokens', 0),
                'success': success,
                'failed': data.get('failed', 0),
                'success_rate': (success / calls * 100) if calls > 0 else 0,
            })
        
        return results
    
    def get_cost_stats(self) -> dict:
        """获取费用统计"""
        cost_data = self.stats.get('cost', {})
        today = datetime.now().strftime("%Y-%m-%d")
        
        return {
            'today': cost_data.get(today, 0),
            'total': sum(cost_data.values()),
        }
    
    def print_panel(self):
        """打印面板"""
        # 标题
        print("╔══════════════════════════════════════════════════════════╗")
        print("║           LLM Control Panel - 模型监控面板                  ║")
        print("╚══════════════════════════════════════════════════════════╝")
        
        # 模型状态
        print("\n┌─────────────────────────────────────────────────────────┐")
        print("│ 📊 模型状态                                              │")
        print("└─────────────────────────────────────────────────────────┘")
        
        model_status = self.get_model_status()
        
        for model, config in self.MODELS.items():
            status = model_status.get(model, {}).get('status', 'unknown')
            icon = "✅" if status == 'online' else "❌"
            model_type = "🖥️ 本地" if config['type'] == 'local' else "☁️ 云"
            
            print(f"  {icon} {model}")
            print(f"      {model_type} | {status}")
        
        # 今日统计
        print("\n┌─────────────────────────────────────────────────────────┐")
        print("│ 📈 今日统计                                              │")
        print("└─────────────────────────────────────────────────────────┘")
        
        today = self.get_today_stats()
        
        print(f"  调用次数: {today['calls']}")
        print(f"  Token消耗: {today['tokens']:,}")
        print(f"  成功: {today['success']} | 失败: {today['failed']}")
        print(f"  成功率: {today['success_rate']:.1f}%")
        
        # 费用
        print("\n┌─────────────────────────────────────────────────────────┐")
        print("│ 💰 费用                                                  │")
        print("└─────────────────────────────────────────────────────────┘")
        
        cost = self.get_cost_stats()
        
        print(f"  今日: ¥{cost['today']:.4f}")
        print(f"  总计: ¥{cost['total']:.4f}")
        
        # 模型详情
        print("\n┌─────────────────────────────────────────────────────────┐")
        print("│ 📋 模型详情                                              │")
        print("└─────────────────────────────────────────────────────────┘")
        
        for m in self.get_model_stats():
            icon = "✅" if m['calls'] > 0 else "○"
            print(f"  {icon} {m['name']}")
            print(f"      调用: {m['calls']} | Tokens: {m['tokens']:,} | 成功率: {m['success_rate']:.0f}%")
        
        # 时间
        print(f"\n更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "="*60)
    
    def export_json(self) -> dict:
        """导出JSON"""
        return {
            'timestamp': datetime.now().isoformat(),
            'model_status': self.get_model_status(),
            'today_stats': self.get_today_stats(),
            'cost': self.get_cost_stats(),
            'models': self.get_model_stats(),
        }


# 全局实例
_panel = None

def get_llm_panel() -> LLMPanel:
    global _panel
    if _panel is None:
        _panel = LLMPanel()
    return _panel


# 测试
if __name__ == "__main__":
    panel = get_llm_panel()
    panel.print_panel()
