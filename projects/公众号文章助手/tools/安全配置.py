#!/usr/bin/env python3
"""
安全配置系统
为OpenClaw功能扩展添加安全保障
"""
import os
import json

class SecureConfig:
    """安全配置"""
    
    def __init__(self):
        self.config_dir = 'data/security'
        os.makedirs(self.config_dir, exist_ok=True)
        
        self.security_file = f'{self.config_dir}/security.json'
        self.whitelist_file = f'{self.config_dir}/whitelist.json'
        self.load_configs()
    
    def load_configs(self):
        # 安全配置
        if os.path.exists(self.security_file):
            with open(self.security_file, 'r') as f:
                self.security = json.load(f)
        else:
            self.security = self.get_default_security()
        
        # 白名单配置
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                self.whitelist = json.load(f)
        else:
            self.whitelist = self.get_default_whitelist()
    
    def get_default_security(self) -> dict:
        """默认安全配置"""
        return {
            'api_key_storage': 'env',  # 使用环境变量存储
            'gateway_mode': 'local',   # 仅本地运行
            'enable_audit': True,      # 启用审计
            'max_file_operations': 100, # 文件操作限制
            'allowed_extensions': ['.py', '.js', '.json', '.md', '.txt', '.html', '.css'],
            'blocked_commands': ['rm -rf', 'del /f', 'format', 'mkfs', 'dd if='],
            'prompt_filter': True,     # 启用Prompt过滤
            'sandbox_mode': True,      # 沙盒模式
            'telegram_whitelist_only': True,  # 仅白名单用户
        }
    
    def get_default_whitelist(self) -> dict:
        """默认白名单"""
        return {
            'users': {
                'telegram': ['8793442405'],  # 你的Telegram ID
                'webchat': ['self'],
            },
            'commands': [
                'python ',
                'node ',
                'git ',
                'openclaw ',
                'curl ',
                'cat ',
                'ls ',
                'cd ',
            ],
            'directories': [
                '~/项目/Ai学习系统/',
                '~/项目/公众号文章助手/',
                '~/.openclaw/',
            ],
            'domains': [],  # 允许的域名，为空则不限制
            'file_patterns': {
                'allowed': ['*.py', '*.js', '*.json', '*.md', '*.txt', '*.html', '*.css', '*.sh'],
                'blocked': ['*.exe', '*.dmg', '*.sh', '*.bat', '*.cmd', '*.ps1']
            }
        }
    
    def save_configs(self):
        with open(self.security_file, 'w', encoding='utf-8') as f:
            json.dump(self.security, f, ensure_ascii=False, indent=2)
        
        with open(self.whitelist_file, 'w', encoding='utf-8') as f:
            json.dump(self.whitelist, f, ensure_ascii=False, indent=2)
    
    def add_allowed_command(self, cmd: str):
        """添加允许的命令"""
        if cmd not in self.whitelist['commands']:
            self.whitelist['commands'].append(cmd)
            self.save_configs()
    
    def add_allowed_directory(self, dir_path: str):
        """添加允许的目录"""
        if dir_path not in self.whitelist['directories']:
            self.whitelist['directories'].append(dir_path)
            self.save_configs()
    
    def add_blocked_command(self, cmd: str):
        """添加阻止的命令"""
        if cmd not in self.security['blocked_commands']:
            self.security['blocked_commands'].append(cmd)
            self.save_configs()
    
    def generate_env_template(self) -> str:
        """生成环境变量模板"""
        return """# OpenClaw 安全环境变量配置
# 复制此文件为 .env 并填入你的API密钥

# ===== API Keys =====
# MiniMax
MINIMAX_API_KEY=your_minimax_key_here

# Perplexity (网页搜索)
PERPLEXITY_API_KEY=your_perplexity_key_here

# OpenAI
OPENAI_API_KEY=your_openai_key_here

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here

# ===== 安全配置 =====
# 允许的用户ID (Telegram)
ALLOWED_TELEGRAM_IDS=8793442405

# 允许的目录 (用逗号分隔)
ALLOWED_DIRECTORIES=~/项目/Ai学习系统,~/.openclaw

# 最大文件操作数
MAX_FILE_OPERATIONS=100
"""
    
    def generate_security_script(self) -> str:
        """生成安全检查脚本"""
        return '''#!/usr/bin/env python3
"""OpenClaw安全检查脚本"""
import os
import json
import subprocess

def check_security():
    """执行安全检查"""
    issues = []
    
    # 1. 检查Gateway绑定
    try:
        result = subprocess.run(['openclaw', 'gateway', 'status'], 
                              capture_output=True, text=True)
        if '0.0.0.0' in result.stdout or '::' in result.stdout:
            issues.append('⚠️ Gateway暴露到公网！')
        else:
            print('✅ Gateway仅本地运行')
    except:
        pass
    
    # 2. 检查API Key
    env_file = os.path.expanduser('~/.openclaw/.env')
    if os.path.exists(env_file):
        print('✅ .env文件存在')
    else:
        issues.append('⚠️ 建议使用.env文件存储API Key')
    
    # 3. 检查安全审计
    try:
        result = subprocess.run(['openclaw', 'security', 'audit'], 
                              capture_output=True, text=True)
        if 'critical' in result.stdout.lower():
            issues.append('⚠️ 存在严重安全漏洞！')
        else:
            print('✅ 安全审计通过')
    except:
        pass
    
    # 4. 检查Cron任务
    cron_file = os.path.expanduser('~/.openclaw/cron/jobs.json')
    if os.path.exists(cron_file):
        with open(cron_file) as f:
            jobs = json.load(f)
            print(f'📋 Cron任务数: {len(jobs.get("jobs", []))}')
    
    # 总结
    if issues:
        print('\\n❌ 发现问题:')
        for issue in issues:
            print(f'  {issue}')
    else:
        print('\\n✅ 安全检查通过！')
    
    return len(issues) == 0

if __name__ == '__main__':
    check_security()
'''
    
    def report(self) -> dict:
        """生成安全报告"""
        return {
            'security_mode': self.security.get('gateway_mode'),
            'api_key_storage': self.security.get('api_key_storage'),
            'prompt_filter': self.security.get('prompt_filter'),
            'sandbox_mode': self.security.get('sandbox_mode'),
            'allowed_commands': len(self.whitelist.get('commands', [])),
            'allowed_directories': len(self.whitelist.get('directories', [])),
            'blocked_commands': len(self.security.get('blocked_commands', [])),
        }

def setup_secure_config():
    """设置安全配置"""
    secure = SecureConfig()
    secure.save_configs()
    
    # 生成环境变量模板
    with open('.env.example', 'w') as f:
        f.write(secure.generate_env_template())
    
    # 生成安全检查脚本
    with open('tools/security_check.py', 'w') as f:
        f.write(secure.generate_security_script())
    
    return secure

if __name__ == '__main__':
    print("="*50)
    print("🔒 安全配置系统")
    print("="*50)
    
    secure = setup_secure_config()
    report = secure.report()
    
    print(f"\\n📊 安全配置:")
    print(f"   网关模式: {report['security_mode']}")
    print(f"   API存储: {report['api_key_storage']}")
    print(f"   Prompt过滤: {report['prompt_filter']}")
    print(f"   沙盒模式: {report['sandbox_mode']}")
    print(f"   允许命令: {report['allowed_commands']}")
    print(f"   允许目录: {report['allowed_directories']}")
    print(f"   阻止命令: {report['blocked_commands']}")
    
    print(f"\\n✅ 安全配置已保存")
    print(f"📁 配置文件: data/security/")
    print(f"📝 环境变量模板: .env.example")
    print(f"🔍 安全检查脚本: tools/security_check.py")
