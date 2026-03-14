#!/usr/bin/env python3
"""
OpenClaw CLI 助手
快速执行常用命令
"""
import subprocess
import sys
import os

# CLI命令字典
CLI_COMMANDS = {
    # 基础命令
    'onboard': {
        'cmd': 'openclaw onboard',
        'desc': '重新运行入门引导'
    },
    'tui': {
        'cmd': 'openclaw tui',
        'desc': '启动终端UI'
    },
    'dashboard': {
        'cmd': 'openclaw dashboard',
        'desc': '启动仪表板'
    },
    
    # 模型管理
    'models': {
        'cmd': 'openclaw models',
        'desc': '模型管理'
    },
    'models-list': {
        'cmd': 'openclaw models list',
        'desc': '列出所有模型'
    },
    'models-set': {
        'cmd': 'openclaw models set',
        'desc': '切换模型 (需要参数)'
    },
    
    # 网关管理
    'status': {
        'cmd': 'openclaw gateway status',
        'desc': '查看网关状态'
    },
    'start': {
        'cmd': 'openclaw gateway start',
        'desc': '启动网关'
    },
    'stop': {
        'cmd': 'openclaw gateway stop',
        'desc': '停止网关'
    },
    'restart': {
        'cmd': 'openclaw gateway restart',
        'desc': '重启网关'
    },
    
    # 安全
    'audit': {
        'cmd': 'openclaw security audit --deep',
        'desc': '安全审计'
    },
    
    # 配置
    'config': {
        'cmd': 'openclaw configure',
        'desc': '配置OpenClaw'
    },
    
    # 帮助
    'help': {
        'cmd': 'openclaw help',
        'desc': '查看帮助'
    },
    'version': {
        'cmd': 'openclaw --version',
        'desc': '查看版本'
    },
}

def print_commands():
    """打印所有命令"""
    print("\n📖 OpenClaw CLI 常用命令")
    print("="*50)
    
    categories = {
        '基础命令': ['onboard', 'tui', 'dashboard'],
        '模型管理': ['models', 'models-list', 'models-set'],
        '网关管理': ['status', 'start', 'stop', 'restart'],
        '安全': ['audit'],
        '配置': ['config', 'version'],
    }
    
    for cat, cmds in categories.items():
        print(f"\n【{cat}】")
        for name in cmds:
            if name in CLI_COMMANDS:
                cmd = CLI_COMMANDS[name]
                print(f"  {name:15} - {cmd['desc']}")

def run_command(cmd_name: str, *args):
    """运行命令"""
    if cmd_name not in CLI_COMMANDS:
        print(f"❌ 未知命令: {cmd_name}")
        print("\n可用命令:")
        for name, info in CLI_COMMANDS.items():
            print(f"  {name}: {info['desc']}")
        return
    
    cmd_info = CLI_COMMANDS[cmd_name]
    cmd = cmd_info['cmd']
    
    # 添加参数
    if args:
        cmd = f"{cmd} {' '.join(args)}"
    
    print(f"🚀 执行: {cmd}")
    print("-"*50)
    
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ 命令执行超时")
    except Exception as e:
        print(f"❌ 执行错误: {e}")

def main():
    if len(sys.argv) < 2:
        print_commands()
        print("\n" + "="*50)
        print("📝 用法:")
        print("  python openclaw_cli.py <命令> [参数]")
        print("\n示例:")
        print("  python openclaw_cli.py status")
        print("  python openclaw_cli.py models-list")
        print("  python openclaw_cli.py models-set minimax-cn/MiniMax-M2.5")
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    run_command(cmd, *args)

if __name__ == '__main__':
    main()
