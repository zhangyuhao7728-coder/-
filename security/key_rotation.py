#!/usr/bin/env python3
"""
Key Rotation Module - 密钥轮换模块
功能：
1. 自动轮换密钥
2. 记录轮换历史
3. 提醒更换
"""
import os
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class KeyRotationManager:
    """密钥轮换管理器"""
    
    # 轮换周期 (天)
    ROTATION_PERIOD = {
        'TELEGRAM_BOT_TOKEN': 90,
        'MINIMAX_API_KEY': 30,
        'OPENCLAW_SECRET': 90,
        'JWT_SECRET': 30,
    }
    
    def __init__(self):
        """初始化"""
        self.rotation_file = os.path.expanduser('~/.openclaw/logs/key_rotation.json')
        self._ensure_file()
        
        # 加载历史
        with open(self.rotation_file, 'r') as f:
            self.history = json.load(f)
    
    def _ensure_file(self):
        """确保文件存在"""
        os.makedirs(os.path.dirname(self.rotation_file), exist_ok=True)
        if not os.path.exists(self.rotation_file):
            with open(self.rotation_file, 'w') as f:
                json.dump({'keys': {}, 'history': []}, f)
    
    def _save(self):
        """保存"""
        with open(self.rotation_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def register_key(self, key_name: str):
        """注册密钥"""
        if key_name not in self.history['keys']:
            self.history['keys'][key_name] = {
                'created_at': datetime.now().isoformat(),
                'last_rotated': datetime.now().isoformat(),
                'rotation_period': self.ROTATION_PERIOD.get(key_name, 90)
            }
            self._save()
    
    def check_rotation(self, key_name: str) -> dict:
        """检查是否需要轮换"""
        if key_name not in self.history['keys']:
            return {'needs_rotation': True, 'reason': 'not_registered'}
        
        key_info = self.history['keys'][key_name]
        
        last_rotated = datetime.fromisoformat(key_info['last_rotated'])
        period = key_info.get('rotation_period', 90)
        
        days_since = (datetime.now() - last_rotated).days
        
        if days_since >= period:
            return {
                'needs_rotation': True,
                'days_overdue': days_since - period,
                'last_rotated': key_info['last_rotated']
            }
        
        return {
            'needs_rotation': False,
            'days_until_due': period - days_since,
            'last_rotated': key_info['last_rotated']
        }
    
    def rotate_key(self, key_name: str, new_value: str = None) -> bool:
        """记录密钥轮换"""
        if key_name not in self.history['keys']:
            self.register_key(key_name)
        
        # 记录历史
        self.history['history'].append({
            'key_name': key_name,
            'rotated_at': datetime.now().isoformat(),
            'new_value_provided': new_value is not None
        })
        
        # 只保留最近100条
        self.history['history'] = self.history['history'][-100:]
        
        # 更新
        self.history['keys'][key_name]['last_rotated'] = datetime.now().isoformat()
        
        self._save()
        
        return True
    
    def get_status(self) -> dict:
        """获取密钥状态"""
        status = {}
        
        for key_name in self.ROTATION_PERIOD.keys():
            status[key_name] = self.check_rotation(key_name)
        
        return status
    
    def get_due_keys(self) -> List[str]:
        """获取需要轮换的密钥"""
        due = []
        
        for key_name in self.ROTATION_PERIOD.keys():
            result = self.check_rotation(key_name)
            if result['needs_rotation']:
                due.append(key_name)
        
        return due
    
    def get_history(self, key_name: str = None, limit: int = 10) -> List[dict]:
        """获取轮换历史"""
        if key_name:
            return [
                h for h in self.history['history'][-limit:]
                if h['key_name'] == key_name
            ]
        return self.history['history'][-limit:]


# 全局实例
_manager = None

def get_rotation_manager() -> KeyRotationManager:
    global _manager
    if _manager is None:
        _manager = KeyRotationManager()
    return _manager


# 测试
if __name__ == "__main__":
    mgr = get_rotation_manager()
    
    print("=== Key Rotation 测试 ===\n")
    
    # 注册密钥
    for key in ['TELEGRAM_BOT_TOKEN', 'MINIMAX_API_KEY']:
        mgr.register_key(key)
    
    # 检查状态
    print("密钥状态:")
    for key, status in mgr.get_status().items():
        due = "⚠️ 需要轮换" if status['needs_rotation'] else "✅ 正常"
        print(f"  {key}: {due}")
    
    print(f"\n需要轮换: {mgr.get_due_keys()}")
