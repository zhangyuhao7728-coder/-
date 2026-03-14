#!/usr/bin/env python3
"""
Security Center - 安全防护中心
功能：
1. 统一安全管理
2. 自动安全扫描
3. 威胁检测
4. 自动防护
5. 安全报告
"""
import os
import sys
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

# 安全模块路径
PROJECT_ROOT = Path(__file__).parent.parent
SECURITY_DIR = PROJECT_ROOT / 'security'
sys.path.insert(0, str(SECURITY_DIR))

# 导入安全模块
try:
    from scraper_guard import ScraperGuard, check_code, check_url, check_command, check_file_type
    from network_guard_enhanced import EnhancedNetworkGuard
    GUARDS_AVAILABLE = True
except ImportError:
    GUARDS_AVAILABLE = False


# ========== 安全配置 ==========
class SecurityConfig:
    """安全配置"""
    
    # 监控的项目目录
    PROJECT_DIRS = [
        PROJECT_ROOT / 'openclaw_modules',
        PROJECT_ROOT / 'ai-control-plane',
        PROJECT_ROOT / 'scripts',
    ]
    
    # 自动化脚本目录（高风险）
    AUTO_SCRIPT_DIRS = [
        Path('~/.openclaw/scripts').expanduser(),
        PROJECT_ROOT / 'scripts',
    ]
    
    # 爬虫目录
    CRAWLER_DIRS = [
        PROJECT_ROOT / 'openclaw_modules' / 'tools' / 'crawler',
    ]
    
    # 安全日志目录
    LOG_DIR = Path('~/.openclaw/logs/security').expanduser()
    
    # 白名单域名
    ALLOWED_DOMAINS: Set[str] = {
        'quotes.toscrape.com',
        'news.163.com',
        'news.sina.com.cn',
        'reddit.com',
        'www.reddit.com',
        'github.com',
        'api.github.com',
        'wikipedia.org',
        'stackoverflow.com',
        'api.minimax.io',
        'api.openai.com',
        'api.anthropic.com',
    }
    
    # 危险文件模式
    DANGEROUS_PATTERNS = [
        'eval(', 'exec(', '__import__(',
        'os.system(', 'subprocess.',
        'socket.', 'pty.',
    ]
    
    # 自动修复
    AUTO_FIX = True
    
    # 威胁级别
    THREAT_LEVELS = {
        'critical': 0,  # 立即处理
        'high': 1,     # 24小时内处理
        'medium': 7,   # 7天内处理
        'low': 30,     # 30天内处理
    }


class SecurityReport:
    """安全报告"""
    
    def __init__(self):
        self.timestamp = datetime.now()
        self.findings: List[Dict] = []
        self.stats = {
            'files_scanned': 0,
            'threats_found': 0,
            'fixed': 0,
            'warnings': 0,
        }
    
    def add_finding(self, severity: str, category: str, description: str, 
                    file_path: str = '', line: int = 0, suggestion: str = ''):
        """添加发现"""
        self.findings.append({
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'category': category,
            'description': description,
            'file': file_path,
            'line': line,
            'suggestion': suggestion,
        })
        self.stats['threats_found'] += 1
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'findings': self.findings,
            'stats': self.stats,
        }


class SecurityCenter:
    """安全中心"""
    
    def __init__(self):
        self.config = SecurityConfig()
        self.logger = self._setup_logger()
        
        # 安全守卫
        self.scraper_guard = None
        self.network_guard = None
        
        if GUARDS_AVAILABLE:
            self.scraper_guard = ScraperGuard()
            self.network_guard = EnhancedNetworkGuard()
        
        # 扫描缓存（避免重复扫描）
        self._scan_cache: Dict[str, float] = {}
        self._cache_ttl = 3600  # 1小时
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        os.makedirs(self.config.LOG_DIR, exist_ok=True)
        
        logger = logging.getLogger('SecurityCenter')
        logger.setLevel(logging.INFO)
        
        # 文件处理器
        fh = logging.FileHandler(self.config.LOG_DIR / 'security_center.log')
        fh.setLevel(logging.INFO)
        
        # 控制台处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        
        # 格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    # ========== 文件扫描 ==========
    
    def scan_file(self, file_path: Path) -> Optional[Dict]:
        """扫描单个文件"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except:
            return None
        
        findings = []
        
        # 检查危险模式
        for i, line in enumerate(content.split('\n'), 1):
            for pattern in self.config.DANGEROUS_PATTERNS:
                if pattern in line:
                    # 排除注释
                    stripped = line.strip()
                    if stripped.startswith('#') or stripped.startswith('//'):
                        continue
                    
                    # 排除安全扫描/检测代码（只是在检查模式，不是真正执行）
                    if 'DANGEROUS_PATTERNS' in content or 'pattern' in line.lower():
                        # 检查是否真的是在定义模式，而不是执行
                        if "r'" in line or 're.compile' in content:
                            continue
                    
                    findings.append({
                        'line': i,
                        'pattern': pattern,
                        'content': line.strip()[:100],
                    })
        
        if findings:
            return {
                'file': str(file_path),
                'findings': findings,
                'hash': hashlib.md5(content.encode()).hexdigest(),
            }
        
        return None
    
    def scan_directory(self, directory: Path, patterns: List[str] = ['*.py']) -> List[Dict]:
        """扫描目录"""
        results = []
        
        if not directory.exists():
            self.logger.warning(f"目录不存在: {directory}")
            return results
        
        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                # 跳过 __pycache__
                if '__pycache__' in str(file_path):
                    continue
                
                # 检查缓存
                cache_key = str(file_path)
                if cache_key in self._scan_cache:
                    if time.time() - self._scan_cache[cache_key] < self._cache_ttl:
                        continue
                
                self._scan_cache[cache_key] = time.time()
                result = self.scan_file(file_path)
                
                if result:
                    results.append(result)
        
        return results
    
    # ========== 自动化脚本安全检查 ==========
    
    def check_auto_scripts(self) -> SecurityReport:
        """检查自动化脚本安全"""
        report = SecurityReport()
        
        self.logger.info("开始扫描自动化脚本...")
        
        for script_dir in self.config.AUTO_SCRIPT_DIRS:
            if not script_dir.exists():
                continue
            
            for py_file in script_dir.glob('*.py'):
                report.stats['files_scanned'] += 1
                
                result = self.scan_file(py_file)
                
                if result:
                    for finding in result['findings']:
                        # 评估严重程度
                        if 'eval(' in finding['pattern'] or 'exec(' in finding['pattern']:
                            severity = 'critical'
                        elif 'os.system' in finding['pattern']:
                            severity = 'high'
                        else:
                            severity = 'medium'
                        
                        report.add_finding(
                            severity=severity,
                            category='dangerous_code',
                            description=f"危险模式: {finding['pattern']}",
                            file_path=str(py_file),
                            line=finding['line'],
                            suggestion="检查是否为内部可控代码，必要时使用安全守卫"
                        )
        
        # 检查爬虫
        for crawler_dir in self.config.CRAWLER_DIRS:
            if not crawler_dir.exists():
                continue
            
            for py_file in crawler_dir.rglob('*.py'):
                report.stats['files_scanned'] += 1
                
                result = self.scan_file(py_file)
                
                if result:
                    for finding in result['findings']:
                        # 爬虫中的危险代码更危险
                        if finding['pattern'] in ['eval(', 'exec(']:
                            severity = 'critical'
                        else:
                            severity = 'high'
                        
                        report.add_finding(
                            severity=severity,
                            category='crawler_risk',
                            description=f"爬虫危险模式: {finding['pattern']}",
                            file_path=str(py_file),
                            line=finding['line'],
                            suggestion="确保使用 ScraperGuard 进行安全检查"
                        )
        
        self.logger.info(f"扫描完成: {report.stats}")
        return report
    
    # ========== URL/域名检查 ==========
    
    def check_domain(self, domain: str) -> Tuple[bool, str]:
        """检查域名是否安全"""
        if not GUARDS_AVAILABLE:
            # 简单检查
            return domain in self.config.ALLOWED_DOMAINS, ''
        
        return self.scraper_guard.check_domain(domain)
    
    def check_url(self, url: str) -> Tuple[bool, str]:
        """检查URL是否安全"""
        if not GUARDS_AVAILABLE:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            allowed = any(domain.endswith(d) or domain == d for d in self.config.ALLOWED_DOMAINS)
            return allowed, '' if allowed else '域名不在白名单'
        
        return self.scraper_guard.check_url(url)
    
    def check_code(self, code: str, source: str = 'unknown') -> Tuple[bool, str]:
        """检查代码是否安全"""
        if not GUARDS_AVAILABLE:
            for pattern in self.config.DANGEROUS_PATTERNS:
                if pattern in code:
                    return False, f"危险模式: {pattern}"
            return True, ''
        
        return self.scraper_guard.check_code_execution(code, source)
    
    # ========== 安全防护 ==========
    
    def protect_crawler(self, url: str) -> Tuple[bool, str]:
        """保护爬虫调用"""
        return self.check_url(url)
    
    def protect_code_execution(self, code: str, source: str = 'unknown') -> Tuple[bool, str]:
        """保护代码执行"""
        return self.check_code(code, source)
    
    def validate_download(self, url: str, content_type: str, filename: str = '') -> Tuple[bool, str]:
        """验证下载安全性"""
        # 检查URL
        url_safe, url_reason = self.check_url(url)
        if not url_safe:
            return False, f"URL: {url_reason}"
        
        # 检查文件类型
        if GUARDS_AVAILABLE:
            file_safe, file_reason = self.scraper_guard.check_file_type(content_type, filename)
            if not file_safe:
                return False, f"文件: {file_reason}"
        
        return True, '安全'
    
    # ========== 自动防护 ==========
    
    def auto_protect(self) -> Dict:
        """自动运行防护"""
        result = {
            'timestamp': datetime.now().isoformat(),
            'actions_taken': [],
        }
        
        # 1. 检查自动化脚本
        report = self.check_auto_scripts()
        
        # 2. 如果有严重问题，记录并尝试修复
        critical_count = sum(1 for f in report.findings if f['severity'] == 'critical')
        
        if critical_count > 0:
            self.logger.critical(f"发现 {critical_count} 个严重安全问题！")
            result['actions_taken'].append({
                'type': 'alert',
                'message': f'发现 {critical_count} 个严重安全问题，需要人工处理'
            })
        
        # 3. 检查运行中的进程是否有异常
        # （这里可以添加更多自动防护逻辑）
        
        return result
    
    # ========== 安全报告 ==========
    
    def generate_report(self, format: str = 'text') -> str:
        """生成安全报告"""
        report = self.check_auto_scripts()
        
        if format == 'json':
            return json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
        
        # 文本格式
        lines = [
            "=" * 60,
            "🛡️  安全扫描报告",
            "=" * 60,
            f"扫描时间: {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"扫描文件: {report.stats['files_scanned']}",
            f"发现问题: {report.stats['threats_found']}",
            "",
        ]
        
        # 按严重程度分组
        for severity in ['critical', 'high', 'medium', 'low']:
            findings = [f for f in report.findings if f['severity'] == severity]
            if findings:
                emoji = {'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢'}[severity]
                lines.append(f"\n{emoji} {severity.upper()} ({len(findings)}个)")
                lines.append("-" * 40)
                
                for f in findings[:5]:  # 最多显示5个
                    lines.append(f"  • {f['description']}")
                    lines.append(f"    文件: {f['file']}:{f['line']}")
                    if f['suggestion']:
                        lines.append(f"    建议: {f['suggestion']}")
                
                if len(findings) > 5:
                    lines.append(f"  ... 还有 {len(findings) - 5} 个")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict:
        """获取安全统计"""
        return {
            'guards_available': GUARDS_AVAILABLE,
            'cache_size': len(self._scan_cache),
            'log_dir': str(self.config.LOG_DIR),
        }


# ========== 单例 ==========
_center = None

def get_security_center() -> SecurityCenter:
    global _center
    if _center is None:
        _center = SecurityCenter()
    return _center


# ========== CLI ==========
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='安全中心')
    parser.add_argument('action', choices=['scan', 'report', 'protect', 'stats'],
                       help='操作')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='报告格式')
    
    args = parser.parse_args()
    
    center = get_security_center()
    
    if args.action == 'scan':
        report = center.check_auto_scripts()
        print(f"扫描完成: {report.stats}")
        
    elif args.action == 'report':
        print(center.generate_report(args.format))
        
    elif args.action == 'protect':
        result = center.auto_protect()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    elif args.action == 'stats':
        print(json.dumps(center.get_stats(), indent=2))
