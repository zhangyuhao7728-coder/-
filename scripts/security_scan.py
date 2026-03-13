#!/usr/bin/env python3
"""
Security Scanner - 自动安全检测脚本
功能：
1. Token泄漏检测
2. 危险代码检测
3. 权限错误检测
4. 自动生成报告
"""
import os
import re
import subprocess
from datetime import datetime
from typing import Dict, List


class SecurityScanner:
    """安全扫描器"""
    
    PROJECT_DIR = os.path.expanduser("~/项目/Ai学习系统")
    
    def __init__(self):
        """初始化"""
        self.results = {
            'token_leaks': [],
            'dangerous_code': [],
            'permission_errors': [],
            'warnings': []
        }
    
    # ========== Token 泄漏检测 ==========
    
    TOKEN_PATTERNS = {
        'telegram': r'\d{8,10}:[a-zA-Z0-9_-]{35,}',
        'openai': r'sk-[a-zA-Z0-9]{20,}',
        'minimax': r'sk-cp-[a-zA-Z0-9_-]{20,}',
        'github': r'ghp_[a-zA-Z0-9]{36,}',
    }
    
    def scan_tokens(self) -> List[dict]:
        """扫描Token泄漏"""
        leaks = []
        
        for root, dirs, files in os.walk(self.PROJECT_DIR):
            # 跳过目录
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if not file.endswith(('.py', '.js', '.json', '.yaml', '.sh')):
                    continue
                
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            for token_type, pattern in self.TOKEN_PATTERNS.items():
                                if re.search(pattern, line):
                                    leaks.append({
                                        'file': filepath,
                                        'line': line_num,
                                        'type': token_type,
                                        'preview': line.strip()[:50]
                                    })
                except:
                    pass
        
        self.results['token_leaks'] = leaks
        return leaks
    
    # ========== 危险代码检测 ==========
    
    DANGEROUS_PATTERNS = {
        'shell_injection': [
            (r'os\.system\s*\(', 'os.system() 调用'),
            (r'subprocess\.\w+\s*\(\s*shell\s*=\s*True', 'shell=True 危险'),
            (r'eval\s*\(', 'eval() 危险'),
            (r'exec\s*\(', 'exec() 危险'),
        ],
        'hardcoded_secret': [
            (r'password\s*=\s*["\'][^"\']{6,}', '硬编码密码'),
            (r'api[_-]?key\s*=\s*["\'][^"\']{10,}', '硬编码API Key'),
            (r'secret\s*=\s*["\'][^"\']{10,}', '硬编码Secret'),
        ],
        'insecure_code': [
            (r'urllib\.request\.urlopen\s*\(', '不安全的URL请求'),
            (r'requests\.get\s*\(\s*[^"\']*http://', 'HTTP而非HTTPS'),
        ]
    }
    
    def scan_dangerous_code(self) -> List[dict]:
        """扫描危险代码"""
        dangerous = []
        
        for root, dirs, files in os.walk(self.PROJECT_DIR):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            
            for file in files:
                if not file.endswith(('.py', '.js', '.sh')):
                    continue
                
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            for category, patterns in self.DANGEROUS_PATTERNS.items():
                                for pattern, desc in patterns:
                                    if re.search(pattern, line, re.IGNORECASE):
                                        dangerous.append({
                                            'file': filepath,
                                            'line': line_num,
                                            'category': category,
                                            'description': desc,
                                            'preview': line.strip()[:50]
                                        })
                except:
                    pass
        
        self.results['dangerous_code'] = dangerous
        return dangerous
    
    # ========== 权限错误检测 ==========
    
    def scan_permissions(self) -> List[dict]:
        """扫描权限错误"""
        errors = []
        
        # 检查敏感文件权限
        sensitive_files = [
            '.env',
            '.env.local',
            '*.key',
            '*.pem',
            'id_rsa',
            'id_ed25519',
        ]
        
        for root, dirs, files in os.walk(self.PROJECT_DIR):
            for file in files:
                # 检查.env权限
                if file == '.env':
                    filepath = os.path.join(root, file)
                    try:
                        stat = os.stat(filepath)
                        mode = oct(stat.st_mode)[-3:]
                        
                        # 其他人可读
                        if stat.st_mode & 0o004:
                            errors.append({
                                'file': filepath,
                                'issue': '过于开放的权限',
                                'current': mode,
                                'recommended': '600'
                            })
                    except:
                        pass
                
                # 检查密码文件
                for pattern in ['passwords.txt', 'secrets.json', 'credentials.json']:
                    if file == pattern:
                        filepath = os.path.join(root, file)
                        errors.append({
                            'file': filepath,
                            'issue': '可能包含密码的文件名',
                            'recommendation': '重命名文件'
                        })
        
        self.results['permission_errors'] = errors
        return errors
    
    # ========== 综合扫描 ==========
    
    def scan_all(self) -> Dict:
        """运行完整扫描"""
        print("🔍 开始安全扫描...")
        print("=" * 50)
        
        # Token泄漏
        print("\n1. 扫描Token泄漏...")
        tokens = self.scan_tokens()
        print(f"   发现: {len(tokens)} 个")
        
        # 危险代码
        print("\n2. 扫描危险代码...")
        dangerous = self.scan_dangerous_code()
        print(f"   发现: {len(dangerous)} 个")
        
        # 权限
        print("\n3. 扫描权限错误...")
        perms = self.scan_permissions()
        print(f"   发现: {len(perms)} 个")
        
        # 汇总
        total = len(tokens) + len(dangerous) + len(perms)
        
        print("\n" + "=" * 50)
        print(f"📊 扫描完成: {total} 个问题")
        
        return self.results
    
    def generate_report(self) -> str:
        """生成报告"""
        self.scan_all()
        
        report = f"""
================================================================
                    安全扫描报告
================================================================
扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
项目目录: {self.PROJECT_DIR}

----------------------------------------------------------------
1. Token 泄漏 ({len(self.results['token_leaks'])} 个)
----------------------------------------------------------------
"""
        for leak in self.results['token_leaks'][:10]:
            report += f"  {leak['file']}:{leak['line']} - {leak['type']}\n"
        
        report += f"""
----------------------------------------------------------------
2. 危险代码 ({len(self.results['dangerous_code'])} 个)
----------------------------------------------------------------
"""
        for code in self.results['dangerous_code'][:10]:
            report += f"  {code['file']}:{code['line']} - {code['description']}\n"
        
        report += f"""
----------------------------------------------------------------
3. 权限错误 ({len(self.results['permission_errors'])} 个)
----------------------------------------------------------------
"""
        for perm in self.results['permission_errors']:
            report += f"  {perm['file']} - {perm['issue']}\n"
        
        report += f"""
================================================================
                        建议
================================================================
1. 将Token移至环境变量
2. 避免使用eval/exec
3. 使用600权限保护敏感文件
4. 定期运行安全扫描
================================================================
"""
        return report
    
    def save_report(self, filepath: str = None):
        """保存报告"""
        if filepath is None:
            filepath = os.path.expanduser(f'~/.openclaw/logs/security_scan_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        report = self.generate_report()
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(report)
        
        print(f"\n📄 报告已保存: {filepath}")
        
        return filepath


# 主函数
def main():
    scanner = SecurityScanner()
    scanner.save_report()


if __name__ == "__main__":
    main()
