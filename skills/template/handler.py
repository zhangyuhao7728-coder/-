#!/usr/bin/env python3
"""
Skill Handler - 技能处理器
"""

import json
from pathlib import Path

class SkillHandler:
    def __init__(self):
        self.name = "skill-name"
        self.version = "1.0.0"
    
    def load_config(self):
        """加载配置"""
        config_file = Path(__file__).parent / "skill.json"
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        return {}
    
    def can_handle(self, input_text):
        """检查是否能处理这个输入"""
        config = self.load_config()
        triggers = config.get("triggers", [])
        
        for trigger in triggers:
            if trigger in input_text:
                return True
        return False
    
    def handle(self, input_text, context=None):
        """处理输入"""
        # 实现你的技能逻辑
        return {
            "status": "success",
            "result": "处理结果",
            "message": "回复消息"
        }
    
    def get_prompt(self):
        """获取系统提示词"""
        prompt_file = Path(__file__).parent / "prompt.md"
        if prompt_file.exists():
            with open(prompt_file) as f:
                return f.read()
        return ""

def main():
    handler = SkillHandler()
    
    # 测试
    test_input = "测试关键词"
    if handler.can_handle(test_input):
        result = handler.handle(test_input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("无法处理")

if __name__ == "__main__":
    main()
