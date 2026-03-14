#!/usr/bin/env python3
"""
Security Auto-Protect - 自动安全防护
定时运行安全检查，发现问题自动处理
"""
import os
import sys
import time
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from threading import Thread

# 添加 security 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'security'))

from security_center import get_security_center


class AutoProtector:
    """自动防护器"""
    
    def __init__(self, interval: int = 3600):
        """
        初始化
        
        Args:
            interval: 检查间隔（秒），默认1小时
        """
        self.interval = interval
        self.running = False
        self.center = get_security_center()
        self.logger = self._setup_logger()
        self.last_report = None
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        log_dir = Path('~/.openclaw/logs/security').expanduser()
        os.makedirs(log_dir, exist_ok=True)
        
        logger = logging.getLogger('AutoProtect')
        logger.setLevel(logging.INFO)
        
        fh = logging.FileHandler(log_dir / 'auto_protect.log')
        fh.setLevel(logging.INFO)
        
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def run_check(self) -> dict:
        """运行安全检查"""
        self.logger.info("开始安全检查...")
        
        try:
            # 1. 运行扫描
            report = self.center.check_auto_scripts()
            
            # 2. 生成报告
            result = {
                'timestamp': datetime.now().isoformat(),
                'stats': report.stats,
                'findings': [],
            }
            
            # 3. 分析结果
            critical = [f for f in report.findings if f['severity'] == 'critical']
            high = [f for f in report.findings if f['severity'] == 'high']
            
            if critical:
                self.logger.critical(f"🚨 发现 {len(critical)} 个严重问题！")
                result['alert'] = 'critical'
                result['findings'].extend(critical)
            elif high:
                self.logger.warning(f"⚠️ 发现 {len(high)} 个高危问题")
                result['alert'] = 'high'
                result['findings'].extend(high)
            else:
                self.logger.info("✅ 安全检查通过")
                result['alert'] = 'none'
            
            self.last_report = result
            return result
            
        except Exception as e:
            self.logger.error(f"安全检查失败: {e}")
            return {'error': str(e)}
    
    def protect_crawler(self, url: str) -> Tuple[bool, str]:
        """保护爬虫调用"""
        return self.center.protect_crawler(url)
    
    def protect_code(self, code: str, source: str = 'unknown') -> Tuple[bool, str]:
        """保护代码执行"""
        return self.center.protect_code_execution(code, source)
    
    def start(self):
        """启动自动防护"""
        self.running = True
        self.logger.info(f"🚀 自动防护启动，检查间隔: {self.interval}秒")
        
        # 立即运行一次检查
        self.run_check()
        
        # 后台循环
        while self.running:
            time.sleep(self.interval)
            if self.running:
                self.run_check()
    
    def stop(self):
        """停止自动防护"""
        self.running = False
        self.logger.info("⏹️ 自动防护已停止")
    
    def get_status(self) -> dict:
        """获取状态"""
        return {
            'running': self.running,
            'interval': self.interval,
            'last_check': self.last_report.get('timestamp') if self.last_report else None,
            'last_alert': self.last_report.get('alert') if self.last_report else None,
        }


# ========== 全局实例 ==========
_protector = None

def get_protector(interval: int = 3600) -> AutoProtector:
    global _protector
    if _protector is None:
        _protector = AutoProtector(interval)
    return _protector


# ========== CLI ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='自动安全防护')
    parser.add_argument('--interval', type=int, default=3600,
                       help='检查间隔（秒），默认1小时')
    parser.add_argument('--once', action='store_true',
                       help='只运行一次检查')
    parser.add_argument('--daemon', action='store_true',
                       help='后台守护运行')
    
    args = parser.parse_args()
    
    protector = get_protector(args.interval)
    
    if args.once:
        result = protector.run_check()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.daemon:
        try:
            protector.start()
        except KeyboardInterrupt:
            protector.stop()
    else:
        # 默认运行一次
        result = protector.run_check()
        
        if result.get('alert') == 'none':
            print("✅ 安全检查通过")
        else:
            print(f"⚠️ 发现 {len(result.get('findings', []))} 个问题")
            print(json.dumps(result, indent=2, ensure_ascii=False))
