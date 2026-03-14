#!/usr/bin/env python3
"""
OpenClaw功能扩展系统
基于10个效率技巧开发的功能模块
"""
import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List

class OpenClawEnhancer:
    """OpenClaw增强器"""
    
    def __init__(self):
        self.config_file = 'data/enhancer_config.json'
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'cli_commands': {},
            'cron_tasks': [],
            'tools': {},
            'skills': [],
            'mcp_servers': [],
        }
    
    def save_config(self):
        os.makedirs('data', exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    # ========== CLI命令管理 ==========
    def add_cli_command(self, name: str, command: str, description: str = ''):
        """添加CLI命令"""
        self.config['cli_commands'][name] = {
            'command': command,
            'description': description,
            'added_at': datetime.now().isoformat()
        }
        self.save_config()
    
    def list_cli_commands(self) -> List[dict]:
        """列出所有CLI命令"""
        return [
            {'name': k, **v} for k, v in self.config['cli_commands'].items()
        ]
    
    def execute_cli(self, name: str) -> str:
        """执行CLI命令"""
        if name in self.config['cli_commands']:
            cmd = self.config['cli_commands'][name]['command']
            return f"执行: {cmd}"
        return f"未知命令: {name}"
    
    # ========== Cron任务管理 ==========
    def add_cron_task(self, name: str, schedule: str, action: str, description: str = ''):
        """添加Cron任务"""
        self.config['cron_tasks'].append({
            'name': name,
            'schedule': schedule,
            'action': action,
            'description': description,
            'enabled': True,
            'added_at': datetime.now().isoformat()
        })
        self.save_config()
    
    def list_cron_tasks(self) -> List[dict]:
        """列出Cron任务"""
        return self.config.get('cron_tasks', [])
    
    # ========== 工具配置 ==========
    def add_tool(self, tool_name: str, config: dict):
        """添加工具"""
        self.config['tools'][tool_name] = {
            **config,
            'added_at': datetime.now().isoformat()
        }
        self.save_config()
    
    def list_tools(self) -> List[dict]:
        """列出工具"""
        return [
            {'name': k, **v} for k, v in self.config['tools'].items()
        ]
    
    # ========== MCP服务器管理 ==========
    def add_mcp_server(self, name: str, config: dict):
        """添加MCP服务器"""
        self.config['mcp_servers'].append({
            'name': name,
            **config,
            'added_at': datetime.now().isoformat()
        })
        self.save_config()
    
    def list_mcp_servers(self) -> List[dict]:
        """列出MCP服务器"""
        return self.config.get('mcp_servers', [])
    
    # ========== Skill管理 ==========
    def add_skill(self, name: str, description: str = '', config: dict = None):
        """添加Skill"""
        self.config['skills'].append({
            'name': name,
            'description': description,
            'config': config or {},
            'added_at': datetime.now().isoformat()
        })
        self.save_config()
    
    def list_skills(self) -> List[dict]:
        """列出Skills"""
        return self.config.get('skills', [])
    
    # ========== 预设功能 ==========
    def setup_default_features(self):
        """设置默认功能（基于10个技巧）"""
        
        # 1. CLI命令
        commands = [
            ('onboard', 'openclaw onboard', '重新运行入门引导'),
            ('tui', 'openclaw tui', '启动终端UI'),
            ('dashboard', 'openclaw dashboard', '启动仪表板'),
            ('models-list', 'openclaw models list', '列出所有模型'),
            ('models-set', 'openclaw models set <provider/model>', '切换模型'),
            ('gateway-status', 'openclaw gateway status', '查看网关状态'),
            ('security-audit', 'openclaw security audit --deep', '安全审计'),
            ('gateway-stop', 'openclaw gateway stop', '停止网关'),
            ('gateway-start', 'openclaw gateway start', '启动网关'),
            ('gateway-restart', 'openclaw gateway restart', '重启网关'),
        ]
        
        for name, cmd, desc in commands:
            self.add_cli_command(name, cmd, desc)
        
        # 2. 预设Cron任务模板
        cron_templates = [
            {
                'name': '每日新闻汇总',
                'schedule': '0 8 * * *',
                'action': '搜索最新AI新闻，发到飞书',
                'description': '每天早上8点汇总AI行业新闻'
            },
            {
                'name': '代码审查',
                'schedule': '0 9 * * 1-5',
                'action': '检查PR，自动审查代码',
                'description': '工作日早上9点自动审查代码'
            },
            {
                'name': '依赖检查',
                'schedule': '0 10 * * 0',
                'action': '检查项目依赖安全更新',
                'description': '每周检查依赖安全'
            },
            {
                'name': '错误监控',
                'schedule': '*/10 * * * *',
                'action': '监控错误日志，异常时报警',
                'description': '每10分钟检查错误率'
            },
            {
                'name': '每日总结',
                'schedule': '0 22 * * *',
                'action': '总结当天完成的任务',
                'description': '每天晚上10点提醒总结'
            },
        ]
        
        for task in cron_templates:
            self.add_cron_task(task['name'], task['schedule'], task['action'], task['description'])
        
        # 3. 预设工具
        tools = [
            {
                'name': 'web_search',
                'provider': 'perplexity',
                'model': 'perplexity/sonar-pro',
                'enabled': True,
                'description': '网页搜索工具'
            },
            {
                'name': 'tts',
                'provider': 'edge',
                'voice': 'zh-CN-XiaoxiaoNeural',
                'enabled': True,
                'description': '语音合成'
            },
            {
                'name': 'image',
                'provider': 'nano-banana',
                'model': 'gemini-3.1-flash-image-preview',
                'enabled': False,
                'description': 'AI生图'
            },
        ]
        
        for tool in tools:
            self.add_tool(tool['name'], tool)
        
        # 4. 预设MCP服务器
        mcp_servers = [
            {
                'name': 'apify',
                'description': '网页爬虫',
                'enabled': False,
            },
            {
                'name': 'filesystem',
                'description': '文件操作',
                'enabled': True,
            },
            {
                'name': 'github',
                'description': 'GitHub操作',
                'enabled': False,
            },
        ]
        
        for server in mcp_servers:
            self.add_mcp_server(server['name'], server)
        
        # 5. 预设Skills
        skills = [
            {
                'name': '第二大脑',
                'description': '快速记录笔记和任务'
            },
            {
                'name': '代码审查员',
                'description': '自动审查代码'
            },
            {
                'name': '新闻助手',
                'description': '汇总行业新闻'
            },
        ]
        
        for skill in skills:
            self.add_skill(skill['name'], skill['description'])
        
        print("✅ 默认功能已设置")
    
    def generate_config(self) -> dict:
        """生成OpenClaw配置"""
        config = {}
        
        # 添加工具配置
        if 'web_search' in self.config.get('tools', {}):
            tool = self.config['tools']['web_search']
            if tool.get('enabled'):
                config['tools'] = config.get('tools', {})
                config['tools']['web'] = {
                    'search': {
                        'enabled': True,
                        'provider': tool.get('provider', 'perplexity'),
                        'perplexity': {
                            'apiKey': '${PERPLEXITY_API_KEY}',
                            'model': tool.get('model', 'perplexity/sonar-pro'),
                        }
                    }
                }
        
        # 添加TTS配置
        if 'tts' in self.config.get('tools', {}):
            tool = self.config['tools']['tts']
            if tool.get('enabled'):
                config['messages'] = config.get('messages', {})
                config['messages']['tts'] = {
                    'auto': 'always',
                    'provider': tool.get('provider', 'edge'),
                    'edge': {
                        'enabled': True,
                        'voice': tool.get('voice', 'zh-CN-XiaoxiaoNeural'),
                    }
                }
        
        return config
    
    def report(self) -> dict:
        """生成报告"""
        return {
            'cli_commands': len(self.config.get('cli_commands', {})),
            'cron_tasks': len(self.config.get('cron_tasks', [])),
            'tools': len(self.config.get('tools', {})),
            'mcp_servers': len(self.config.get('mcp_servers', [])),
            'skills': len(self.config.get('skills', [])),
        }

def setup_enhancer():
    """设置增强器"""
    enhancer = OpenClawEnhancer()
    enhancer.setup_default_features()
    return enhancer

if __name__ == '__main__':
    print("="*50)
    print("🚀 OpenClaw功能扩展系统")
    print("="*50)
    
    # 设置默认功能
    enhancer = setup_enhancer()
    
    # 报告
    report = enhancer.report()
    print(f"\n📊 功能统计:")
    print(f"   CLI命令: {report['cli_commands']}")
    print(f"   Cron任务: {report['cron_tasks']}")
    print(f"   工具: {report['tools']}")
    print(f"   MCP服务器: {report['mcp_servers']}")
    print(f"   Skills: {report['skills']}")
    
    # 列出CLI命令
    print(f"\n📝 CLI命令:")
    for cmd in enhancer.list_cli_commands()[:5]:
        print(f"   {cmd['name']}: {cmd['command']}")
    
    # 列出Cron任务
    print(f"\n⏰ Cron任务:")
    for task in enhancer.list_cron_tasks()[:3]:
        print(f"   {task['name']}: {task['schedule']}")
