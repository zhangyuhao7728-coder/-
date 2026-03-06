#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI学习系统 - 精准权限配置 (最终版)
"""

import os
import json

PERMISSIONS_FILE = os.path.expanduser("~/.openclaw/workspace/memory/permissions.json")

PERMISSIONS = {
    "自动执行": {
        "description": "AI学习系统 - 无需确认可直接执行",
        "actions": [
            # 学习
            "获取新闻", "RSS获取", "天气查询",
            "查看日历", "查看计划", "生成计划",
            "记录学习", "整理笔记", "搜索资料",
            
            # 运维
            "心跳检查", "状态监控", "日志分析",
            "健康检查", "备份数据", "文件整理",
            
            # 记忆
            "读取记忆", "写入记忆", "记忆归档",
            "查看日报", "更新TODO",
            
            # 执行类
            "执行代码", "运行脚本", "安装依赖",
            "创建文件", "修改代码"
        ]
    },
    "需确认": {
        "description": "AI学习系统 - 执行前需确认",
        "actions": [
            # 删除代码
            "删除代码",
            
            # 外部类
            "发送邮件", "发送消息", "发布内容",
            "调用API", "执行部署",
            
            # 危险类 (用户要求确认)
            "文件删除", "数据库操作", "系统命令",
            "安装技能", "卸载技能",
            "格式化磁盘", "删除系统文件",
            "提权操作", "未知命令执行",
            "外发敏感数据", "删除备份"
        ]
    },
    "禁止": {
        "description": "AI学习系统 - 绝对禁止执行",
        "actions": []
    }
}

def save_permissions():
    os.makedirs(os.path.dirname(PERMISSIONS_FILE), exist_ok=True)
    with open(PERMISSIONS_FILE, 'w') as f:
        json.dump(PERMISSIONS, f, ensure_ascii=False, indent=2)

def main():
    save_permissions()
    print("✅ 权限已更新！\n")
    print("🛡️ 最终权限配置：\n")
    print(f"✅ 自动执行: {len(PERMISSIONS['自动执行']['actions'])}项")
    print(f"⚠️ 需确认: {len(PERMISSIONS['需确认']['actions'])}项 (全部确认)")
    print(f"🚫 禁止: {len(PERMISSIONS['禁止']['actions'])}项")

if __name__ == "__main__":
    main()
