#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生活记忆记录器 - 用例60 (加密版)
敏感数据加密存储
"""

import os
import json
import re
import base64
import hashlib
from datetime import datetime

# 文件路径
PEOPLE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/people.json.enc")
INTERACTIONS_FILE = os.path.expanduser("~/.openclaw/workspace/memory/interactions.json.enc")
KEY_FILE = os.path.expanduser("~/.openclaw/workspace/memory/.key")

# 简单加密 (Base64 + 混淆)
def generate_key():
    """生成加密密钥"""
    key = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:16]
    return key

def load_key():
    """加载密钥"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return f.read()
    else:
        key = generate_key()
        with open(KEY_FILE, 'w') as f:
            f.write(key)
        return key

def encrypt(text):
    """加密"""
    if not text:
        return ""
    key = load_key()
    # 简单XOR加密 + Base64
    encrypted = ""
    for i, c in enumerate(text):
        encrypted += chr(ord(c) ^ ord(key[i % len(key)]))
    return base64.b64encode(encrypted.encode()).decode()

def decrypt(text):
    """解密"""
    if not text:
        return ""
    try:
        key = load_key()
        decoded = base64.b64decode(text.encode()).decode()
        decrypted = ""
        for i, c in enumerate(decoded):
            decrypted += chr(ord(c) ^ ord(key[i % len(key)]))
        return decrypted
    except:
        return text

# 敏感字段
SENSITIVE_FIELDS = ["电话", "微信", "地址", "生日"]

def encrypt_people(people):
    """加密敏感字段"""
    encrypted = {}
    
    for name, data in people.items():
        encrypted[name] = data.copy()
        
        if "info" in data:
            encrypted[name]["info"] = {}
            for key, values in data["info"].items():
                if key in SENSITIVE_FIELDS:
                    encrypted[name]["info"][key] = [encrypt(v) for v in values]
                else:
                    encrypted[name]["info"][key] = values
    
    return encrypted

def decrypt_people(data):
    """解密敏感字段"""
    decrypted = {}
    
    for name, person in data.items():
        decrypted[name] = person.copy()
        
        if "info" in person:
            decrypted[name]["info"] = {}
            for key, values in person["info"].items():
                if key in SENSITIVE_FIELDS:
                    decrypted[name]["info"][key] = [decrypt(v) for v in values]
                else:
                    decrypted[name]["info"][key] = values
    
    return decrypted

def save_people_encrypted(people):
    """保存加密数据"""
    encrypted = encrypt_people(people)
    os.makedirs(os.path.dirname(PEOPLE_FILE), exist_ok=True)
    with open(PEOPLE_FILE, 'w') as f:
        json.dump(encrypted, f, ensure_ascii=False, indent=2)

def load_people_decrypted():
    """加载解密数据"""
    if os.path.exists(PEOPLE_FILE):
        with open(PEOPLE_FILE, 'r') as f:
            encrypted = json.load(f)
        return decrypt_people(encrypted)
    return {}

def migrate_plaintext():
    """迁移纯文本数据"""
    plain_file = PEOPLE_FILE.replace('.enc', '')
    
    if os.path.exists(plain_file):
        print("发现纯文本数据，正在加密迁移...")
        
        with open(plain_file, 'r') as f:
            people = json.load(f)
        
        save_people_encrypted(people)
        
        # 备份原文件
        os.rename(plain_file, plain_file + ".bak")
        print(f"✅ 已加密并备份原文件到 {plain_file}.bak")
        return True
    
    return False

# 兼容旧接口
def load_people():
    return load_people_decrypted()

def save_people(people):
    save_people_encrypted(people)

# ========== 以下是原版功能 ==========

EXTRACT_PATTERNS = {
    "过敏": r'(.+?)对(.+?)过敏|过敏',
    "喜好": r'喜欢(.+?)|爱吃',
    "厌恶": r'不喜欢|讨厌|不吃',
    "职业": r'是(.+?)(老师|医生|工程师|设计师|学生|老板|程序员|产品经理)',
    "孩子": r'有(.+?)孩子|孩子叫',
    "生日": r'生日.*?(\d+)月(\d+)日',
    "家乡": r'来自|老家的',
    "电话": r'电话.*?(\d{11})|号码.*?(\d{11})',
    "跟进": r'记得|要.*?提醒',
}

RELATION_TYPES = {
    "朋友": "friend",
    "同事": "colleague", 
    "家人": "family",
    "老师": "teacher",
    "同学": "classmate",
    "客户": "client",
}

def extract_info(text):
    info = {}
    for key, pattern in EXTRACT_PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            info[key] = [m if isinstance(m, str) else ' '.join(m) for m in matches]
    return info

def add_person(name, info=None, relation=None):
    people = load_people()
    
    if name not in people:
        people[name] = {
            "created": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "last_interaction": None,
            "relation": relation or "朋友",
            "info": {},
            "photo": None,
        }
    
    if info:
        for key, values in info.items():
            if key not in people[name]["info"]:
                people[name]["info"][key] = []
            for v in values:
                if v and v not in people[name]["info"][key]:
                    people[name]["info"][key].append(v)
    
    people[name]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    save_people(people)
    return True

def list_people():
    people = load_people()
    
    output = "👥 人物记忆库 (已加密)\n"
    output += f"📊 总人数: {len(people)}人\n\n"
    
    by_relation = {}
    for name, data in people.items():
        rel = data.get('relation', '朋友')
        if rel not in by_relation:
            by_relation[rel] = []
        by_relation[rel].append(name)
    
    for rel, names in by_relation.items():
        output += f"🏷️ {rel}:\n"
        for name in names:
            data = people[name]
            output += f"   • {name}\n"
            if data.get('info'):
                for k, v in data['info'].items():
                    display_val = v[0] if v else ""
                    if k in SENSITIVE_FIELDS:
                        display_val = "***"
                    output += f"     {k}: {display_val}\n"
        output += "\n"
    
    return output

def main():
    import sys
    
    # 迁移旧数据
    migrate_plaintext()
    
    if len(sys.argv) < 2:
        print(list_people())
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) > 2:
        name = sys.argv[2]
        args = ' '.join(sys.argv[3:])
        info = extract_info(args)
        
        relation = None
        for rel in RELATION_TYPES.keys():
            if f"关系:{rel}" in args:
                relation = rel
        
        add_person(name, info, relation)
        print(f"✅ 已添加 {name} (已加密)")
    
    elif cmd == "list":
        print(list_people())
    
    else:
        print(list_people())

if __name__ == "__main__":
    main()
