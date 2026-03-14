#!/usr/bin/env python3
"""AI概念学习库"""
import json

class AIConceptLibrary:
    def __init__(self):
        self.concepts = {
            'LLM': {
                'name': '大语言模型',
                'description': 'Large Language Model，基于Transformer的大规模语言模型',
                'examples': ['GPT', 'Claude', 'MiniMax'],
                'level': '入门'
            },
            'Prompt': {
                'name': '提示词',
                'description': '与AI模型交互时输入的文本指令',
                'examples': ['角色扮演', 'few-shot', 'chain-of-thought'],
                'level': '入门'
            },
            'Agent': {
                'name': '智能体',
                'description': '能够自主执行任务的AI系统',
                'examples': ['OpenClaw', 'AutoGPT'],
                'level': '进阶'
            },
            'RAG': {
                'name': '检索增强生成',
                'description': '结合外部知识库来增强AI生成能力',
                'examples': ['向量数据库', '知识库'],
                'level': '进阶'
            },
            'Token': {
                'name': 'Token',
                'description': 'AI处理的最小文本单位',
                'examples': ['1个中文≈2个token'],
                'level': '入门'
            }
        }
    
    def learn(self, concept):
        if concept in self.concepts:
            c = self.concepts[concept]
            print(f"\n📖 {concept} - {c['name']}")
            print(f"   {c['description']}")
            print(f"   难度: {c['level']}")
            print(f"   示例: {', '.join(c['examples'])}")
        else:
            print(f"❌ 未找到概念: {concept}")
    
    def list_all(self):
        print("="*50)
        print("📚 AI概念库")
        print("="*50)
        for k, v in self.concepts.items():
            print(f"\n{k:10} {v['name']} ({v['level']})")
            print(f"         {v['description'][:40]}...")

if __name__ == '__main__':
    lib = AIConceptLibrary()
    lib.list_all()
