#!/usr/bin/env python3
"""
Log Auto Cleanup - 日志自动清理
功能：
1. 自动清理旧日志
2. 保留最近N天
3. 压缩归档
"""
import os
import time
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path


class LogCleaner:
    """日志清理器"""
    
    # 配置
    LOGS_DIR = os.path.expanduser('~/.openclaw/logs')
    
    # 保留天数
    RETAIN_DAYS = {
        '*.log': 7,        # 普通日志保留7天
        '*.txt': 7,
        'audit.db': 30,    # 数据库保留30天
    }
    
    # 最大文件大小 (MB)
    MAX_SIZE = {
        'security.log': 10,
        'access.log': 10,
        'commands.log': 10,
    }
    
    def __init__(self):
        """初始化"""
        self.cleaned = 0
        self.deleted = 0
        self.compressed = 0
    
    def get_age_days(self, filepath: str) -> int:
        """获取文件年龄(天)"""
        mtime = os.path.getmtime(filepath)
        age = time.time() - mtime
        return int(age / 86400)
    
    def should_delete(self, filepath: str) -> bool:
        """判断是否应该删除"""
        basename = os.path.basename(filepath)
        
        for pattern, days in self.RETAIN_DAYS.items():
            if pattern.startswith('*.'):
                ext = pattern[1:]
                if basename.endswith(ext):
                    return self.get_age_days(filepath) > days
            elif pattern in basename:
                return self.get_age_days(filepath) > days
        
        return False
    
    def should_compress(self, filepath: str) -> bool:
        """判断是否应该压缩"""
        # 只压缩大文件
        size_mb = os.path.getsize(filepath) / 1024 / 1024
        return size_mb > 5
    
    def compress_file(self, filepath: str) -> bool:
        """压缩文件"""
        if filepath.endswith('.gz'):
            return False
        
        gz_path = filepath + '.gz'
        
        try:
            with open(filepath, 'rb') as f_in:
                with gzip.open(gz_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # 删除原文件
            os.remove(filepath)
            self.compressed += 1
            return True
        except Exception as e:
            print(f"压缩失败: {e}")
            return False
    
    def delete_file(self, filepath: str) -> bool:
        """删除文件"""
        try:
            os.remove(filepath)
            self.deleted += 1
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    def clean_logs(self, dry_run: bool = False) -> dict:
        """清理日志"""
        if not os.path.exists(self.LOGS_DIR):
            return {'error': '日志目录不存在'}
        
        self.cleaned = 0
        self.deleted = 0
        self.compressed = 0
        
        for root, dirs, files in os.walk(self.LOGS_DIR):
            for file in files:
                filepath = os.path.join(root, file)
                
                # 跳过目录和数据库
                if os.path.isdir(filepath):
                    continue
                if file.endswith('.db'):
                    continue
                
                # 检查是否应该删除
                if self.should_delete(filepath):
                    if not dry_run:
                        self.delete_file(filepath)
                    self.cleaned += 1
                
                # 检查是否应该压缩
                elif self.should_compress(filepath):
                    if not dry_run:
                        self.compress_file(filepath)
        
        return {
            'cleaned': self.cleaned,
            'deleted': self.deleted,
            'compressed': self.compressed
        }
    
    def get_stats(self) -> dict:
        """获取日志统计"""
        if not os.path.exists(self.LOGS_DIR):
            return {}
        
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.LOGS_DIR):
            for file in files:
                filepath = os.path.join(root, file)
                if not os.path.isdir(filepath):
                    total_size += os.path.getsize(filepath)
                    file_count += 1
        
        return {
            'files': file_count,
            'size_mb': round(total_size / 1024 / 1024, 2),
            'dir': self.LOGS_DIR
        }


# 全局实例
_cleaner = None

def get_log_cleaner() -> LogCleaner:
    global _cleaner
    if _cleaner is None:
        _cleaner = LogCleaner()
    return _cleaner

def clean_logs(dry_run: bool = False) -> dict:
    return get_log_cleaner().clean_logs(dry_run)


# 测试
if __name__ == "__main__":
    cleaner = get_log_cleaner()
    
    print("=== Log Auto Cleanup ===\n")
    
    # 统计
    stats = cleaner.get_stats()
    print(f"当前日志: {stats.get('files', 0)} 个文件, {stats.get('size_mb', 0)} MB")
    
    # 预览清理
    print("\n预览清理结果:")
    result = clean_logs(dry_run=True)
    print(f"  将删除: {result['cleaned']} 个")
    print(f"  将压缩: {result.get('compressed', 0)} 个")
    
    # 确认
    print("\n执行清理? (y/n): ", end='')
    # answer = input()
    # if answer.lower() == 'y':
    #     clean_logs()
    #     print("✅ 清理完成")
