#!/usr/bin/env python3
"""
AI Team Workflow - AI团队协作流程
完整协作: CEO→Planner→Researcher→Coder→Reviewer→Analyst
"""
import requests
from typing import Dict, List


class AIWorkflow:
    """AI团队协作流程"""
    
    # Agent模型映射
    AGENT_MODELS = {
        "CEO": "qwen3.5:9b",
        "Planner": "qwen3.5:9b",
        "Researcher": "qwen2.5:14b",
        "Coder": "deepseek-coder:6.7b",
        "Reviewer": "qwen3.5:9b",
        "Analyst": "qwen2.5:14b",
    }
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.results = {}
    
    def call_model(self, model: str, prompt: str) -> str:
        """调用模型"""
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=60
            )
            
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        
        return f"[{model}] 处理: {prompt}"
    
    # ===== 步骤1: CEO决策 =====
    
    def step_ceo(self, task: str) -> str:
        """CEO决策"""
        print(f"\n👔 CEO 决策中...")
        
        prompt = f"""你是一个CEO，需要决策如何完成这个任务: {task}
给出决策建议:"""
        
        result = self.call_model(self.AGENT_MODELS["CEO"], prompt)
        
        print(f"   决策: {result[:100]}...")
        self.results["CEO"] = result
        
        return result
    
    # ===== 步骤2: Planner规划 =====
    
    def step_planner(self, task: str) -> List[str]:
        """Planner规划"""
        print(f"\n📋 Planner 规划中...")
        
        prompt = f"""将这个任务拆解为具体步骤:
{task}

返回步骤列表，每行一个步骤:"""
        
        result = self.call_model(self.AGENT_MODELS["Planner"], prompt)
        
        # 解析步骤
        steps = [s.strip() for s in result.split("\n") if s.strip()]
        
        print(f"   拆解为 {len(steps)} 个步骤")
        self.results["Planner"] = steps
        
        return steps
    
    # ===== 步骤3: Researcher调研 =====
    
    def step_researcher(self, topic: str) -> str:
        """Researcher调研"""
        print(f"\n🔍 Researcher 调研中...")
        
        prompt = f"""调研这个主题:
{topic}

给出关键信息:"""
        
        result = self.call_model(self.AGENT_MODELS["Researcher"], prompt)
        
        print(f"   调研完成")
        self.results["Researcher"] = result
        
        return result
    
    # ===== 步骤4: Coder编码 =====
    
    def step_coder(self, task: str) -> str:
        """Coder编码"""
        print(f"\n💻 Coder 编写代码...")
        
        prompt = f"""编写代码完成这个任务:
{task}

只返回代码，不要解释:"""
        
        result = self.call_model(self.AGENT_MODELS["Coder"], prompt)
        
        print(f"   代码编写完成")
        self.results["Coder"] = result
        
        return result
    
    # ===== 步骤5: Reviewer审核 =====
    
    def step_reviewer(self, code: str) -> str:
        """Reviewer审核"""
        print(f"\n🔎 Reviewer 审核代码...")
        
        prompt = f"""审核这段代码，给出改进建议:
{code[:500]}"""
        
        result = self.call_model(self.AGENT_MODELS["Reviewer"], prompt)
        
        print(f"   审核完成")
        self.results["Reviewer"] = result
        
        return result
    
    # ===== 步骤6: Analyst评估 =====
    
    def step_analyst(self, results: Dict) -> str:
        """Analyst评估"""
        print(f"\n📊 Analyst 评估结果...")
        
        prompt = f"""评估这些结果，给出总结:
{results}"""
        
        result = self.call_model(self.AGENT_MODELS["Analyst"], prompt)
        
        print(f"   评估完成")
        self.results["Analyst"] = result
        
        return result
    
    # ===== 完整工作流 =====
    
    def execute(self, task: str) -> Dict:
        """执行完整工作流"""
        print("="*50)
        print(f"🎯 任务: {task}")
        print("="*50)
        
        # 1. CEO决策
        ceo_result = self.step_ceo(task)
        
        # 2. Planner规划
        steps = self.step_planner(task)
        
        # 3. 步骤执行
        step_results = []
        
        for i, step in enumerate(steps[:3], 1):  # 最多3个步骤
            print(f"\n--- 步骤 {i}/{len(steps)}: {step[:30]} ---")
            
            # 根据步骤类型选择Agent
            if any(kw in step.lower() for kw in ["查", "研究", "调研"]):
                step_result = self.step_researcher(step)
            elif any(kw in step.lower() for kw in ["写", "代码", "实现"]):
                step_result = self.step_coder(step)
            else:
                step_result = self.call_model("qwen2.5:latest", step)
            
            step_results.append(step_result)
        
        # 4. Reviewer审核
        if step_results:
            code = step_results[0]
            review = self.step_reviewer(code)
        
        # 5. Analyst评估
        final = self.step_analyst({
            "CEO": ceo_result[:100],
            "steps": steps,
            "results": step_results,
        })
        
        print("\n" + "="*50)
        print("✅ 工作流完成!")
        print("="*50)
        
        return {
            "task": task,
            "ceo_decision": ceo_result,
            "steps": steps,
            "step_results": step_results,
            "final": final,
        }


# 测试
if __name__ == "__main__":
    workflow = AIWorkflow()
    
    print("=== AI Team Workflow 测试 ===\n")
    
    # 执行完整工作流
    result = workflow.execute("写一个爬虫抓取新闻")
