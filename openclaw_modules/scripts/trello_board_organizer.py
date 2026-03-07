#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例49：Trello看板夜间整理
自动整理Trello看板
"""

import os
import requests
from datetime import datetime, timedelta

# Trello API配置 (需要设置环境变量)
TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY", "")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN", "")
BOARD_ID = os.environ.get("TRELLO_BOARD_ID", "")

CONFIG_FILE = os.path.expanduser("~/.openclaw/trello_config.json")

def load_config():
    """从文件加载配置"""
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(api_key, token, board_id):
    """保存配置"""
    import json
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"api_key": api_key, "token": token, "board_id": board_id}, f)

def get_cards(board_id, api_key, token):
    """获取看板卡片"""
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = {"key": api_key, "token": token}
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.json() if resp.status_code == 200 else []
    except:
        return []

def close_card(card_id, api_key, token):
    """关闭卡片"""
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {"key": api_key, "token": token, "closed": "true"}
    
    try:
        resp = requests.put(url, params=params)
        return resp.status_code == 200
    except:
        return False

def generate_report(api_key=None, token=None, board_id=None):
    """生成报告"""
    print("="*50)
    print("📋 Trello看板夜间整理")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 优先使用环境变量，其次使用配置文件
    api_key = api_key or TRELLO_API_KEY or load_config().get("api_key", "")
    token = token or TRELLO_TOKEN or load_config().get("token", "")
    board_id = board_id or BOARD_ID or load_config().get("board_id", "")
    
    if not api_key or not token:
        print("\n⚠️ 未配置Trello API")
        print("请配置:")
        print("1. 访问 https://trello.com/app-key 获取API Key")
        print("2. 生成Token: https://trello.com/1/authorize?expiration=1day&scope=read,write&name=OpenClaw")
        print("3. 告诉我配置信息")
        return False
    
    # 获取卡片
    cards = get_cards(board_id, api_key, token)
    
    if not cards:
        print("\n⚠️ 无法获取卡片，请检查Board ID")
        return False
    
    print(f"\n📊 看板共有 {len(cards)} 张卡片")
    
    # 分析
    old_cards = []
    for card in cards:
        if card.get("due") and card.get("dueComplete"):
            try:
                due_date = datetime.fromisoformat(card["due"].replace("Z", "+00:00"))
                if (datetime.now() - due_date.replace(tzinfo=None)).days > 30:
                    old_cards.append(card)
            except:
                pass
    
    # 显示结果
    print(f"\n📋 过期已完成卡片 (30天+): {len(old_cards)}")
    for card in old_cards[:5]:
        print(f"   - {card['name']}")
    
    if old_cards:
        print(f"\n💡 可用 '整理Trello' 命令自动归档")
    
    return True

def configure(api_key, token, board_id):
    """配置Trello"""
    save_config(api_key, token, board_id)
    print("✅ Trello配置已保存！")

def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "configure" and len(sys.argv) >= 5:
            configure(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("用法:")
            print("  python trello_board_organizer.py                    # 报告")
            print("  python trello_board_organizer.py configure <key> <token> <board_id>  # 配置")
    else:
        generate_report()

if __name__ == "__main__":
    main()
