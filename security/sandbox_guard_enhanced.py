#!/usr/bin/env python3
"""
Enhanced Sandbox Guard - 增强版沙盒守卫
功能：
1. Docker沙盒
2. Python venv沙盒
3. restricted shell
4. 资源限制
5. 超时控制
"""
import os
import sys
import subprocess
import time
import tempfile
import shutil
from typing import Dict, List, Optional, Tuple


class EnhancedSandboxGuard:
    """增强版沙盒守卫"""
    
    # ========== 沙盒类型 ==========
    SANDBOX_TYPES = {
        'docker': {
            'name': 'Docker',
            'description': 'Docker容器隔离',
            'enabled': False,  # 需要Docker
        },
        'venv': {
            'name': 'Python venv',
            'description': 'Python虚拟环境',
            'enabled': True,
        },
        'restricted': {
            'name': 'Restricted Shell',
            'description': '受限shell',
            'enabled': True,
        },
        'bwrap': {
            'name': 'Bubblewrap',
            'description': 'Linux沙盒',
            'enabled': False,  # 需要bwrap
        },
    }
    
    # ========== 资源限制 ==========
    RESOURCE_LIMITS = {
        'max_cpu_percent': 50,      # CPU限制 %
        'max_memory_mb': 512,       # 内存限制 MB
        'max_time_seconds': 300,    # 超时时间 5分钟
        'max_file_size_mb': 100,    # 文件大小限制
        'max_processes': 10,        # 最大进程数
    }
    
    def __init__(self, sandbox_type: str = 'venv'):
        """初始化"""
        self.sandbox_type = sandbox_type
        self.enabled = True
        
        # 检查沙盒可用性
        self._check_sandbox()
        
        # 统计
        self.stats = {
            'executions': 0,
            'success': 0,
            'failed': 0,
            'timeout': 0
        }
        
        # 日志
        self.log: List[dict] = []
    
    def _check_sandbox(self):
        """检查沙盒是否可用"""
        if self.sandbox_type == 'docker':
            try:
                result = subprocess.run(
                    ['docker', '--version'],
                    capture_output=True,
                    timeout=5
                )
                self.SANDBOX_TYPES['docker']['enabled'] = result.returncode == 0
            except:
                self.SANDBOX_TYPES['docker']['enabled'] = False
        
        elif self.sandbox_type == 'bwrap':
            try:
                result = subprocess.run(
                    ['bwrap', '--version'],
                    capture_output=True,
                    timeout=5
                )
                self.SANDBOX_TYPES['bwrap']['enabled'] = result.returncode == 0
            except:
                self.SANDBOX_TYPES['bwrap']['enabled'] = False
    
    def _log(self, action: str, **kwargs):
        """记录日志"""
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'sandbox_type': self.sandbox_type,
            **kwargs
        }
        self.log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/sandbox_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {action}: {kwargs}\n")
    
    # ========== Docker 沙盒 ==========
    
    def _execute_docker(self, command: str, timeout: int = 60) -> Dict:
        """Docker沙盒执行"""
        container_name = f"sandbox_{int(time.time())}"
        
        # 限制资源的Docker命令
        docker_cmd = [
            'docker', 'run',
            '--rm',
            '--name', container_name,
            '--memory', f"{self.RESOURCE_LIMITS['max_memory_mb']}m",
            '--cpus', str(self.RESOURCE_LIMITS['max_cpu_percent'] / 100),
            '--pids-limit', str(self.RESOURCE_LIMITS['max_processes']),
            '-v', f"{os.getcwd()}:/workspace",
            'python:3.11-slim',
            'sh', '-c', command
        ]
        
        try:
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd='/workspace'
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            # 停止容器
            subprocess.run(['docker', 'stop', container_name], 
                        capture_output=True)
            return {
                'success': False,
                'error': 'Timeout',
                'stderr': 'Execution timed out'
            }
    
    # ========== venv 沙盒 ==========
    
    def _execute_venv(self, command: str, timeout: int = 60) -> Dict:
        """Python venv沙盒执行"""
        # 创建临时venv
        venv_dir = tempfile.mkdtemp(prefix='sandbox_')
        venv_python = os.path.join(venv_dir, 'bin', 'python')
        
        try:
            # 创建venv
            subprocess.run(
                [sys.executable, '-m', 'venv', venv_dir],
                capture_output=True,
                timeout=60
            )
            
            # 安装基础包 (可选)
            # subprocess.run([venv_python, '-m', 'pip', 'install', 'requests'], ...)
            
            # 执行命令
            result = subprocess.run(
                [venv_python, '-c', command] if command.startswith('python -c') 
                else ['sh', '-c', command],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=venv_dir
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout',
                'stderr': 'Execution timed out'
            }
        finally:
            # 清理
            try:
                shutil.rmtree(venv_dir)
            except:
                pass
    
    # ========== Restricted Shell ==========
    
    def _execute_restricted(self, command: str, timeout: int = 60) -> Dict:
        """受限Shell执行"""
        # 构建受限命令
        restricted_cmd = [
            'bash',
            '-r',  # restricted mode
            '-c', command
        ]
        
        # 使用 rbash 或 restricted bash
        # 限制环境变量
        env = os.environ.copy()
        env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        env['HOME'] = tempfile.gettempdir()
        
        try:
            result = subprocess.run(
                restricted_cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                cwd=tempfile.gettempdir()
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout',
                'stderr': 'Execution timed out'
            }
    
    # ========== Bubblewrap ==========
    
    def _execute_bwrap(self, command: str, timeout: int = 60) -> Dict:
        """Bubblewrap沙盒执行"""
        bwrap_cmd = [
            'bwrap',
            '--unshare-ipc',
            '--unshare-net',
            '--unshare-pid',
            '--unshare-uts',
            '--ro-bind', '/', '/',
            '--tmpfs', '/tmp',
            '--dev', '/dev',
            '--proc', '/proc',
            'sh', '-c', command
        ]
        
        try:
            result = subprocess.run(
                bwrap_cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout',
                'stderr': 'Execution timed out'
            }
    
    # ========== 主执行方法 ==========
    
    def execute(self, command: str, timeout: int = None) -> Dict:
        """
        在沙盒中执行命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间(秒)
            
        Returns:
            dict: {
                'success': bool,
                'stdout': str,
                'stderr': str,
                'returncode': int
            }
        """
        self.stats['executions'] += 1
        
        if timeout is None:
            timeout = self.RESOURCE_LIMITS['max_time_seconds']
        
        # 选择执行方式
        if self.sandbox_type == 'docker' and self.SANDBOX_TYPES['docker']['enabled']:
            result = self._execute_docker(command, timeout)
        elif self.sandbox_type == 'venv':
            result = self._execute_venv(command, timeout)
        elif self.sandbox_type == 'bwrap' and self.SANDBOX_TYPES['bwrap']['enabled']:
            result = self._execute_bwrap(command, timeout)
        else:
            result = self._execute_restricted(command, timeout)
        
        # 统计
        if result.get('success'):
            self.stats['success'] += 1
        elif result.get('error') == 'Timeout':
            self.stats['timeout'] += 1
        else:
            self.stats['failed'] += 1
        
        # 记录日志
        self._log('execute', 
                   command=command[:100],
                   success=result.get('success', False))
        
        return result
    
    def execute_python(self, code: str, timeout: int = 60) -> Dict:
        """在沙盒中执行Python代码"""
        return self.execute(f'python3 -c "{code}"', timeout)
    
    def execute_script(self, script_path: str, timeout: int = 60) -> Dict:
        """在沙盒中执行脚本"""
        return self.execute(f'bash {script_path}', timeout)
    
    # ========== 工具方法 ==========
    
    def set_sandbox_type(self, sandbox_type: str):
        """设置沙盒类型"""
        if sandbox_type in self.SANDBOX_TYPES:
            self.sandbox_type = sandbox_type
    
    def get_sandbox_types(self) -> Dict:
        """获取可用的沙盒类型"""
        return self.SANDBOX_TYPES.copy()
    
    def set_resource_limits(self, **limits):
        """设置资源限制"""
        for key, value in limits.items():
            if key in self.RESOURCE_LIMITS:
                self.RESOURCE_LIMITS[key] = value
    
    def get_resource_limits(self) -> Dict:
        """获取资源限制"""
        return self.RESOURCE_LIMITS.copy()
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def get_log(self, limit: int = 100) -> List[dict]:
        return self.log[-limit:]


# 全局实例
_guard = None

def get_guard(sandbox_type: str = 'venv') -> EnhancedSandboxGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedSandboxGuard(sandbox_type)
    return _guard

def execute_in_sandbox(command: str, timeout: int = 60) -> Dict:
    return get_guard().execute(command, timeout)

def execute_python_in_sandbox(code: str, timeout: int = 60) -> Dict:
    return get_guard().execute_python(code, timeout)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Sandbox Guard 测试 ===\n")
    
    # 显示沙盒类型
    print("可用沙盒类型:")
    for stype, info in guard.get_sandbox_types().items():
        status = "✅" if info['enabled'] else "❌"
        print(f"  {status} {stype:12} - {info['description']}")
    
    print(f"\n当前沙盒: {guard.sandbox_type}")
    print(f"资源限制: {guard.get_resource_limits()}")
    
    # 测试执行
    print("\n测试执行:")
    result = guard.execute('echo "Hello from sandbox"', timeout=10)
    print(f"  结果: {'✅' if result['success'] else '❌'}")
    print(f"  输出: {result.get('stdout', '')[:50]}")
    
    # 测试Python
    print("\n测试Python:")
    result = guard.execute_python('print("Python in sandbox")', timeout=10)
    print(f"  结果: {'✅' if result['success'] else '❌'}")
    print(f"  输出: {result.get('stdout', '')}")
    
    print(f"\n统计: {guard.get_stats()}")
