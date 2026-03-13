#!/usr/bin/env python3
"""
Explanation Engine - 解释引擎
"""


class ExplanationEngine:
    """概念解释引擎"""
    
    # 预定义解释
    SIMPLE_EXPLANATIONS = {
        "变量": "变量就像盒子，用来存放数据。例如 x = 5，就是把5放进x这个盒子",
        "函数": "函数就像做菜的食谱，输入材料，输出美味的菜。可以重复使用",
        "循环": "循环就像跑步，跑完一圈再跑一圈，直到跑完为止",
        "列表": "列表就像一排抽屉，每个抽屉可以放东西",
        "字典": "字典就像真实的字典，通过拼音(键)找到对应的字(值)",
        "类": "类就像模具，用模具可以做出很多一样的对象",
        "对象": "对象就像用模具做出来的具体产品",
    }
    
    def explain(self, concept: str) -> str:
        # 先查预定义
        for key, value in self.SIMPLE_EXPLANATIONS.items():
            if key in concept:
                return value
        
        return f"'{concept}'是一个重要的Python概念，需要进一步学习"


_engine = None

def get_explanation_engine():
    global _engine
    if _engine is None:
        _engine = ExplanationEngine()
    return _engine
