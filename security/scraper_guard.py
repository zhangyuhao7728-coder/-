#!/usr/bin/env python3
"""
Scraper Guard - 爬虫安全守卫 v2
功能：
1. 禁止执行从网上获取的代码（eval/exec/compile等）
2. 下载文件类型检查
3. 安全地解析HTML/JSON
4. 隔离爬虫运行环境
5. 命令执行防护
6. 网络请求防护
"""
import os
import re
import ast
import json
import sys
import shutil
import subprocess
import tempfile
import threading
import time
from typing import Dict, List, Optional, Set, Tuple, Any
from pathlib import Path
from contextlib import contextmanager


# ========== 危险操作列表 ==========
DANGEROUS_BUILTINS = {
    'eval',       # 执行Python表达式
    'exec',       # 执行Python代码
    'compile',    # 编译代码
    '__import__', # 动态导入
    'open',       # 文件操作（可限制）
    'input',      # 用户输入
    'reload',     # 模块重载
    'breakpoint', # Python 3.7+ 调试
    'memoryview', # 内存视图（可用于漏洞利用）
}

# ========== 允许的文件类型 ==========
ALLOWED_FILE_TYPES = {
    # 文本
    'text/html',
    'text/plain',
    'text/css',
    'text/javascript',
    'application/json',
    'application/xml',
    'text/xml',
    'application/xml',
    'application/xhtml+xml',
    'application/rss+xml',
    # 图片（只读）
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml',
    'image/bmp',
    'image/x-icon',
    # 文档
    'application/pdf',
    'application/zip',
    'application/octet-stream',
    'application/gzip',
    'application/x-tar',
}

# ========== 危险扩展名 ==========
DANGEROUS_EXTENSIONS = {
    # 可执行文件
    '.exe', '.bat', '.sh', '.bash', '.zsh', '.ps1', '.cmd', '.com',
    '.dmg', '.pkg', '.deb', '.rpm', '.app', '.msi',
    # 动态库
    '.so', '.dll', '.dylib', '.a', '.lib',
    # Java/字节码
    '.jar', '.class', '.war',
    # Python
    '.pyc', '.pyo', '.pyd', '.pyw',
    # 脚本
    '.vbs', '.js', '.jse', '.wsf', '.wsh', '.php', '.pl', '.rb', '.lua',
    # 归档（可能有恶意payload）
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
    # 其他
    '.scr', '.pif', '.application', '.gadget', '.msh', '.msh1', '.msh2',
}

# ========== 危险命令关键词 ==========
DANGEROUS_COMMANDS = {
    # 文件操作
    'rm -rf', 'del /', 'rmdir', 'unlink', 'shutil.rmtree',
    'mkfs', 'dd if=', 'format',
    # 系统操作
    'shutdown', 'reboot', 'halt', 'poweroff',
    'kill -9', 'killall', 'pkill',
    'chmod 777', 'chown', 'chgrp',
    # 网络
    'wget ', 'curl ', 'nc ', 'netcat',
    'ssh ', 'scp ', 'sftp',
    'iptables', 'ufw', 'firewall-cmd',
    # 用户
    'useradd', 'userdel', 'passwd', 'sudo',
    # 进程
    'ps aux', 'top', 'htop',
    # Docker
    'docker run', 'docker exec', 'docker rm',
    # Python 危险操作
    'subprocess.call', 'subprocess.run', 'subprocess.Popen',
    'os.system', 'os.popen', 'os.spawn',
    'pty.spawn', 'pty.fork',
    'socket.connect', 'socket.socket',
}

# ========== 网络白名单域名 ==========
ALLOWED_DOMAINS = {
    # 常用网站
    'quotes.toscrape.com',
    'news.163.com',
    'news.sina.com.cn',
    'reddit.com',
    'www.reddit.com',
    'github.com',
    'api.github.com',
    'wikipedia.org',
    'en.wikipedia.org',
    'zh.wikipedia.org',
    'stackoverflow.com',
    'www.stackoverflow.com',
    # AI
    'api.minimax.io',
    'api.openai.com',
    'api.anthropic.com',
    # 本地
    'localhost',
    '127.0.0.1',
}


class SecurityError(Exception):
    """安全异常"""
    pass


class ScraperGuard:
    """爬虫安全守卫 v2"""
    
    # 类级别的安全开关
    _instance = None
    _enabled = True
    
    def __init__(self, allow_file_write: bool = False, allow_network: bool = True):
        """
        初始化
        
        Args:
            allow_file_write: 是否允许写文件（默认禁止）
            allow_network: 是否允许网络请求（默认允许）
        """
        self.allow_file_write = allow_file_write
        self.allow_network = allow_network
        
        # 统计
        self.stats = {
            'total_checks': 0,
            'code_blocked': 0,
            'file_blocked': 0,
            'command_blocked': 0,
            'network_blocked': 0,
            'allowed': 0
        }
        
        # 日志
        self.log: List[dict] = []
        
        # 沙盒目录
        self._sandbox_dir = None
    
    @classmethod
    def get_instance(cls) -> 'ScraperGuard':
        """单例模式"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def enable(cls):
        """启用安全检查"""
        cls._enabled = True
    
    @classmethod
    def disable(cls):
        """禁用安全检查（危险！）"""
        cls._enabled = False
    
    @classmethod
    def is_enabled(cls) -> bool:
        """是否启用"""
        return cls._enabled
    
    def _log(self, action: str, target: str, result: str, detail: str = ''):
        """记录日志"""
        if not self._enabled:
            return
            
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'target': target,
            'result': result,
            'detail': detail
        }
        self.log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/scraper_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} [{action}] {target}: {result} {detail}\n")
    
    # ========== URL/域名检查 ==========
    
    def check_domain(self, domain: str) -> Tuple[bool, str]:
        """检查域名是否允许"""
        if not self._enabled:
            return True, ''
            
        self.stats['total_checks'] += 1
        domain = domain.lower().strip()
        
        # 直接匹配
        if domain in ALLOWED_DOMAINS:
            self.stats['allowed'] += 1
            return True, ''
        
        # 子域名匹配
        for allowed in ALLOWED_DOMAINS:
            if domain == allowed or domain.endswith('.' + allowed):
                self.stats['allowed'] += 1
                return True, ''
        
        # 检查是否是IP
        if self._is_ip(domain):
            # 允许本地IP
            if domain in ('127.0.0.1', 'localhost', '0.0.0.0', '::1'):
                self.stats['allowed'] += 1
                return True, ''
        
        self.stats['network_blocked'] += 1
        self._log('domain_check', domain, 'blocked', '不在白名单')
        return False, f'域名不在白名单: {domain}'
    
    def _is_ip(self, target: str) -> bool:
        """检查是否是IP"""
        import socket
        try:
            socket.inet_aton(target)
            return True
        except:
            return False
    
    def check_url(self, url: str) -> Tuple[bool, str]:
        """检查URL是否允许"""
        if not self._enabled:
            return True, ''
            
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        return self.check_domain(domain)
    
    # ========== 代码执行检查 ==========
    
    def check_code_execution(self, code: str, source: str = 'unknown') -> Tuple[bool, str]:
        """
        检查代码是否包含危险操作
        """
        if not self._enabled:
            return True, ''
            
        self.stats['total_checks'] += 1
        
        # 检查是否包含危险关键词
        dangerous_patterns = [
            (r'\beval\s*\(', 'eval() 调用'),
            (r'\bexec\s*\(', 'exec() 调用'),
            (r'\bcompile\s*\(', 'compile() 调用'),
            (r'__import__\s*\(', '__import__() 调用'),
            (r'\bopen\s*\(', 'open() 文件操作'),
            (r'\binput\s*\(', 'input() 用户输入'),
            (r'subprocess\.(run|call|Popen|check_output)', 'subprocess 调用'),
            (r'os\.system\s*\(', 'os.system 调用'),
            (r'os\.popen\s*\(', 'os.popen 调用'),
            (r'os\.spawn', 'os.spawn 调用'),
            (r'os\.remove\s*\(', 'os.remove 删除文件'),
            (r'os\.unlink\s*\(', 'os.unlink 删除文件'),
            (r'os\.rmdir\s*\(', 'os.rmdir 删除目录'),
            (r'shutil\.(rmtree|move|copy)', 'shutil 危险操作'),
            (r'pty\.(open|fork|spawn)', 'pty 调用'),
            (r'socket\.(socket|connect)', 'socket 网络操作'),
            (r'urllib\.request\.urlopen', 'urllib 请求'),
            (r'requests\.(get|post|put|delete)', 'requests 请求'),
            (r'http\.client\.HTTPConnection', 'HTTP连接'),
            (r'eval\s*\(', 'eval 注入'),
            (r'exec\s*\(', 'exec 注入'),
            (r'__builtins__', '__builtins__ 访问'),
            (r'__globals__', '__globals__ 访问'),
            (r'__code__', '__code__ 访问'),
            (r'func_globals', 'func_globals 访问'),
            (r'breakpoint\s*\(', 'breakpoint 调试'),
            (r'memoryview\s*\(', 'memoryview 内存操作'),
        ]
        
        for pattern, description in dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                self.stats['code_blocked'] += 1
                self._log('code_check', source, 'blocked', description)
                return False, f"危险操作: {description}"
        
        self.stats['allowed'] += 1
        self._log('code_check', source, 'allowed', '无危险操作')
        return True, '安全'
    
    def check_ast(self, code: str, source: str = 'unknown') -> Tuple[bool, List[str]]:
        """用 AST 分析代码（更精确）"""
        if not self._enabled:
            return True, []
            
        dangers = []
        
        class DangerVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                if isinstance(node.func, ast.Name):
                    if node.func.id in DANGEROUS_BUILTINS:
                        dangers.append(f"危险内置: {node.func.id}")
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        obj = node.func.value.id
                        attr = node.func.attr
                        if obj == 'os' and attr in ('system', 'popen', 'spawn', 'remove', 'unlink', 'rmdir'):
                            dangers.append(f"os.{attr}")
                        elif obj == 'subprocess':
                            dangers.append(f"subprocess.{attr}")
                        elif obj == 'shutil':
                            dangers.append(f"shutil.{attr}")
                        elif obj == 'socket':
                            dangers.append(f"socket.{attr}")
                
                self.generic_visit(node)
            
            def visit_Import(self, node):
                dangers.append(f"导入模块: {', '.join(n.name for n in node.names)}")
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node):
                module = node.module or '?'
                dangers.append(f"从 {module} 导入: {', '.join(n.name for n in node.names)}")
                self.generic_visit(node)
        
        try:
            tree = ast.parse(code)
            visitor = DangerVisitor()
            visitor.visit(tree)
            
            if dangers:
                self.stats['code_blocked'] += 1
                self._log('ast_check', source, 'blocked', str(dangers))
                return False, dangers
        except SyntaxError as e:
            dangers.append(f"语法错误: {e}")
        
        self.stats['allowed'] += 1
        self._log('ast_check', source, 'allowed', '无危险操作')
        return True, []
    
    # ========== 文件安全检查 ==========
    
    def check_file_type(self, content_type: str, filename: str = '') -> Tuple[bool, str]:
        """检查文件类型是否安全"""
        if not self._enabled:
            return True, ''
            
        self.stats['total_checks'] += 1
        
        # 检查扩展名
        if filename:
            ext = Path(filename).suffix.lower()
            if ext in DANGEROUS_EXTENSIONS:
                self.stats['file_blocked'] += 1
                self._log('file_check', filename, 'blocked', f'危险扩展名: {ext}')
                return False, f'危险文件类型: {ext}'
        
        # 检查 MIME 类型
        base_type = content_type.split(';')[0].strip().lower()
        
        if base_type in ALLOWED_FILE_TYPES:
            self.stats['allowed'] += 1
            self._log('file_check', filename or content_type, 'allowed', base_type)
            return True, '允许'
        
        # 允许未知的 text/* 类型
        if base_type.startswith('text/'):
            self.stats['allowed'] += 1
            return True, '允许 (text/*)'
        
        self.stats['file_blocked'] += 1
        self._log('file_check', filename or content_type, 'blocked', base_type)
        return False, f'不支持的文件类型: {base_type}'
    
    # ========== 命令执行防护 ==========
    
    def check_command(self, command: str) -> Tuple[bool, str]:
        """检查命令是否危险"""
        if not self._enabled:
            return True, ''
            
        self.stats['total_checks'] += 1
        
        command_lower = command.lower()
        
        for dangerous in DANGEROUS_COMMANDS:
            if dangerous in command_lower:
                self.stats['command_blocked'] += 1
                self._log('command_check', command, 'blocked', dangerous)
                return False, f"危险命令: {dangerous}"
        
        self.stats['allowed'] += 1
        return True, '安全'
    
    # ========== 安全解析 ==========
    
    def safe_json_loads(self, text: str, source: str = 'unknown') -> Optional[Any]:
        """安全地解析 JSON"""
        if not self._enabled:
            return json.loads(text)
            
        try:
            data = json.loads(text)
            self._log('json_parse', source, 'success', type(data).__name__)
            return data
        except json.JSONDecodeError as e:
            self._log('json_parse', source, 'error', str(e))
            return None
    
    def safe_html_parse(self, html: str) -> Optional[Any]:
        """安全地解析 HTML"""
        if not self._enabled:
            from bs4 import BeautifulSoup
            return BeautifulSoup(html, 'html.parser')
            
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            self._log('html_parse', 'string', 'success', 'BeautifulSoup/html.parser')
            return soup
        except ImportError:
            pass
        except Exception as e:
            self._log('html_parse', 'string', 'error', str(e))
        return None
    
    # ========== 沙盒运行 ==========
    
    @contextmanager
    def sandbox(self, directory: str = None):
        """
        沙盒上下文管理器
        在临时目录中运行代码，退出时自动清理
        """
        if directory is None:
            # 创建临时目录
            self._sandbox_dir = tempfile.mkdtemp(prefix='scraper_sandbox_')
        else:
            self._sandbox_dir = directory
            os.makedirs(self._sandbox_dir, exist_ok=True)
        
        original_dir = os.getcwd()
        
        try:
            # 切换到沙盒目录
            os.chdir(self._sandbox_dir)
            yield self._sandbox_dir
        finally:
            # 恢复目录
            os.chdir(original_dir)
            # 清理沙盒
            if self._sandbox_dir and os.path.exists(self._sandbox_dir):
                try:
                    shutil.rmtree(self._sandbox_dir)
                    self._log('sandbox', self._sandbox_dir, 'cleaned', '')
                except Exception as e:
                    self._log('sandbox', self._sandbox_dir, 'cleanup_failed', str(e))
    
    def safe_download(self, url: str, content: bytes, filename: str = '') -> Tuple[bool, str]:
        """安全下载检查"""
        if not self._enabled:
            return True, ''
            
        # 检查URL
        url_safe, url_reason = self.check_url(url)
        if not url_safe:
            return False, url_reason
        
        # 如果有文件名，检查扩展名
        if filename:
            ext = Path(filename).suffix.lower()
            if ext in DANGEROUS_EXTENSIONS:
                self.stats['file_blocked'] += 1
                return False, f'危险文件类型: {ext}'
        
        return True, '允许'
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def get_log(self, limit: int = 100) -> List[dict]:
        return self.log[-limit:]
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            'total_checks': 0,
            'code_blocked': 0,
            'file_blocked': 0,
            'command_blocked': 0,
            'network_blocked': 0,
            'allowed': 0
        }


# ========== 全局函数 ==========

def get_guard() -> ScraperGuard:
    return ScraperGuard.get_instance()

def check_code(code: str, source: str = 'unknown') -> Tuple[bool, str]:
    return get_guard().check_code_execution(code, source)

def check_file_type(content_type: str, filename: str = '') -> Tuple[bool, str]:
    return get_guard().check_file_type(content_type, filename)

def check_url(url: str) -> Tuple[bool, str]:
    return get_guard().check_url(url)

def check_command(command: str) -> Tuple[bool, str]:
    return get_guard().check_command(command)

def safe_json_loads(text: str) -> Optional[Any]:
    return get_guard().safe_json_loads(text)


# ========== 装饰器 ==========

def safe_execute(func):
    """安全执行装饰器"""
    def wrapper(*args, **kwargs):
        guard = get_guard()
        if not guard._enabled:
            return func(*args, **kwargs)
        
        # 检查返回值是否包含危险代码
        result = func(*args, **kwargs)
        
        if isinstance(result, str):
            safe, reason = guard.check_code_execution(result, func.__name__)
            if not safe:
                raise SecurityError(f"危险代码被阻止: {reason}")
        
        return result
    return wrapper


# ========== 测试 ==========
if __name__ == "__main__":
    guard = ScraperGuard()
    
    print("=== Scraper Guard v2 测试 ===\n")
    
    # 测试域名检查
    print("【域名检查】")
    test_domains = [
        ('quotes.toscrape.com', '白名单'),
        ('evil.com', '恶意'),
        ('127.0.0.1', '本地IP'),
        ('google.com', '未授权'),
    ]
    for domain, desc in test_domains:
        safe, reason = guard.check_domain(domain)
        status = "✅" if safe else "❌"
        print(f"  {status} {domain} ({desc}): {reason or '允许'}")
    
    # 测试代码检查
    print("\n【代码检查】")
    test_codes = [
        ('print("hello")', '安全'),
        ('eval("1+1")', 'eval'),
        ('os.system("ls")', 'os.system'),
        ('subprocess.run(["ls"])', 'subprocess'),
    ]
    for code, desc in test_codes:
        safe, reason = guard.check_code_execution(code, desc)
        status = "✅" if safe else "❌"
        print(f"  {status} {desc}: {reason}")
    
    # 测试文件类型
    print("\n【文件类型检查】")
    test_files = [
        ('text/html', 'page.html', 'HTML'),
        ('image/png', 'image.png', 'PNG'),
        ('application/octet-stream', 'malware.exe', 'EXE'),
        ('application/octet-stream', 'script.sh', 'SH'),
    ]
    for ctype, fname, desc in test_files:
        safe, reason = guard.check_file_type(ctype, fname)
        status = "✅" if safe else "❌"
        print(f"  {status} {desc}: {reason}")
    
    # 测试命令
    print("\n【命令检查】")
    test_cmds = [
        ('ls -la', '安全'),
        ('rm -rf /', '危险'),
        ('curl http://evil.com', '危险'),
    ]
    for cmd, desc in test_cmds:
        safe, reason = guard.check_command(cmd)
        status = "✅" if safe else "❌"
        print(f"  {status} {desc}: {reason}")
    
    print(f"\n统计: {guard.get_stats()}")
