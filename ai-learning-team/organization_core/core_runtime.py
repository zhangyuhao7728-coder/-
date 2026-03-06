"""
Organization Core Runtime
统一运行时 - 支持异步任务队列 + 崩溃恢复 + LLM + Risk Manager
"""

from organization_core.event_bus import EventBus
from organization_core.scheduler import Scheduler
from organization_core.agent_registry import AgentRegistry
from organization_core.task_queue import TaskQueue
from organization_core.state_manager import StateManager
from organization_core.recovery_manager import RecoveryManager
from organization_core.worker_pool import LLMWorker, get_llm_worker
from organization_core.model_router import ModelRouter, get_model_router


class OrganizationCore:
    """Organization Core 运行时"""
    
    def __init__(self, max_workers: int = 4, enable_recovery: bool = True, risk_manager=None):
        self.bus = EventBus()
        self.scheduler = Scheduler()
        self.registry = AgentRegistry()
        self.state = StateManager()
        self.task_queue = TaskQueue(self.registry, max_workers=max_workers)
        self.risk_manager = risk_manager
        
        # 初始化 LLM Worker
        self.llm_worker = get_llm_worker()
        
        # 初始化 Model Router
        self.model_router = get_model_router()
        
        # 初始化恢复管理器
        self.recovery_manager = RecoveryManager(
            self.task_queue,
            self.task_queue.repo
        )
        
        self._setup()
        
        # 启动时恢复未完成任务
        if enable_recovery:
            self._recover_on_start()
        
        print("🚀 Organization Core initialized")
        print(f"   - EventBus: ✅")
        print(f"   - Scheduler: ✅")
        print(f"   - AgentRegistry: ✅")
        print(f"   - TaskQueue: ✅ (max_workers={max_workers})")
        print(f"   - LLMWorker: ✅")
        print(f"   - ModelRouter: ✅")
        print(f"   - RecoveryManager: ✅ (enabled={enable_recovery})")
        print(f"   - RiskManager: ✅" if risk_manager else "   - RiskManager: (not connected)")
    
    def _setup(self) -> None:
        """设置事件订阅"""
        self.bus.subscribe("message_received", self._handle_message)
    
    def _recover_on_start(self) -> None:
        """启动时恢复未完成任务"""
        print("\n" + "=" * 50)
        print("🔄 Running crash recovery...")
        print("=" * 50)
        result = self.recovery_manager.recover()
        print("=" * 50 + "\n")
    
    def _handle_message(self, message: dict) -> None:
        """处理消息 - 异步执行"""
        # 1. 决策：哪个 Agent 处理
        agent_name = self.scheduler.decide(message)
        
        # 2. 检查风险锁定
        if self.risk_manager and self.risk_manager.is_locked(agent_name):
            print(f"⛔ Task blocked: {agent_name} is locked due to CRITICAL risk")
            return
        
        # 3. 选择 LLM 模型 (使用 Model Router)
        content = message.get("content", "")
        selected_model = self.model_router.select_model(agent_name, content)
        
        # 4. 选择 LLM 提供商
        llm_provider = self.scheduler.select_llm_provider(message)
        
        # 5. 入队任务（非阻塞）
        task_id = self.task_queue.enqueue(
            content, 
            agent_name,
            metadata={
                "llm_provider": llm_provider,
                "model": selected_model
            }
        )
        
        print(f"📨 Message routed to {agent_name}, task_id={task_id}, model={selected_model}")
    
    def receive_message(self, message: dict) -> None:
        """接收消息入口"""
        self.bus.publish("message_received", message)
    
    def receive_message_sync(self, message: dict) -> None:
        """同步处理消息（直接执行，不过队列）"""
        agent_name = self.scheduler.decide(message)
        
        # 检查风险锁定
        if self.risk_manager and self.risk_manager.is_locked(agent_name):
            print(f"⛔ Task blocked: {agent_name} is locked due to CRITICAL risk")
            return {"error": f"{agent_name} is locked due to CRITICAL risk"}
        
        try:
            agent = self.registry.get(agent_name)
            result = agent(message)
            print(f"✅ Sync execution completed by {agent_name}")
            return result
        except Exception as e:
            print(f"❌ Sync execution failed: {e}")
            return {"error": str(e)}
    
    def chat_with_llm(self, message: str, provider: str = None) -> str:
        """
        使用 LLM 对话
        
        Args:
            message: 用户消息
            provider: 指定提供商 (可选)
            
        Returns:
            LLM 回复
        """
        return self.llm_worker.chat(message, provider_name=provider)
    
    def register_agent(self, name: str, handler) -> None:
        """注册 Agent"""
        self.registry.register(name, handler)
    
    def list_agents(self) -> list:
        """列出所有 Agent"""
        return self.registry.list_agents()
    
    def get_task_status(self, task_id: int) -> dict:
        """获取任务状态"""
        return self.task_queue.get_task(task_id)
    
    def list_tasks(self, status: str = None, limit: int = 100) -> list:
        """列出任务"""
        return self.task_queue.list_tasks(status, limit)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return self.task_queue.get_stats()
    
    def shutdown(self) -> None:
        """关闭核心"""
        self.task_queue.shutdown()
        print("🔴 Organization Core shutdown")
