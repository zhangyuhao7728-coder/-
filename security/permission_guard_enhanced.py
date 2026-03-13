#!/usr/bin/env python3
"""
Enhanced Permission Guard - 增强版权限守卫
功能：
1. Agent权限控制
2. 角色权限
3. 操作审计
4. 权限继承
"""
import os
import json
from typing import Dict, List, Set, Optional


class EnhancedPermissionGuard:
    """增强版权限守卫"""
    
    # ========== 基础权限定义 ==========
    PERMISSIONS = {
        # 文件操作
        'read_project': '读取项目文件',
        'write_project': '写入项目文件',
        'delete_project': '删除项目文件',
        'read_external': '读取外部文件',
        
        # 执行权限
        'execute_script': '执行脚本',
        'execute_command': '执行系统命令',
        'install_package': '安装软件包',
        
        # 网络权限
        'network_access': '访问网络',
        'api_call': '调用外部API',
        
        # 敏感权限
        'read_config': '读取配置',
        'write_config': '写入配置',
        'read_logs': '读取日志',
        
        # 管理权限
        'manage_agent': '管理Agent',
        'view_audit': '查看审计日志',
    }
    
    # ========== Agent权限配置 ==========
    AGENT_PERMISSIONS = {
        # 爬虫Agent - 只读项目，写入输出
        'crawler': {
            'permissions': [
                'read_project',
                'write_project',
                'network_access',
                'execute_script',
            ],
            'description': '爬虫Agent - 数据采集'
        },
        
        # 研究Agent - 读取项目，网络
        'researcher': {
            'permissions': [
                'read_project',
                'network_access',
                'api_call',
            ],
            'description': '研究Agent - 信息收集'
        },
        
        # 工程师Agent - 读写执行
        'engineer': {
            'permissions': [
                'read_project',
                'write_project',
                'execute_script',
                'execute_command',
                'install_package',
            ],
            'description': '工程师Agent - 开发调试'
        },
        
        # 管理员 - 全部权限
        'admin': {
            'permissions': list(PERMISSIONS.keys()),
            'description': '管理员 - 全部权限'
        },
        
        # 默认Agent
        'default': {
            'permissions': [
                'read_project',
                'network_access',
            ],
            'description': '默认权限'
        },
        
        # 主Agent - 全部权限
        'main': {
            'permissions': list(PERMISSIONS.keys()),
            'description': '主Agent - 全部权限'
        },
    }
    
    # ========== 角色权限 ==========
    ROLE_PERMISSIONS = {
        'developer': [
            'read_project',
            'write_project',
            'execute_script',
            'network_access',
        ],
        'analyst': [
            'read_project',
            'read_logs',
            'api_call',
        ],
        'operator': [
            'read_project',
            'execute_script',
            'network_access',
        ],
    }
    
    def __init__(self):
        """初始化"""
        self.custom_permissions: Dict[str, dict] = {}
        self.user_permissions: Dict[str, Set[str]] = {}
        self.session_permissions: Dict[str, Set[str]] = {}
        
        # 加载配置
        self._load_config()
        
        # 统计
        self.stats = {
            'total_checks': 0,
            'allowed': 0,
            'denied': 0
        }
        
        # 日志
        self.log: List[dict] = []
    
    def _load_config(self):
        """加载配置"""
        # 从环境变量加载
        agents_config = os.environ.get('AGENT_PERMISSIONS', '')
        if agents_config:
            try:
                config = json.loads(agents_config)
                self.AGENT_PERMISSIONS.update(config)
            except:
                pass
    
    def _log(self, action: str, agent: str, permission: str, result: bool):
        """记录日志"""
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'agent': agent,
            'permission': permission,
            'result': 'allowed' if result else 'denied'
        }
        self.log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/permission_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {action}: agent={agent} permission={permission} result={entry['result']}\n")
    
    # ========== 权限管理 ==========
    
    def get_agent_permissions(self, agent: str) -> List[str]:
        """获取Agent的权限列表"""
        if agent in self.custom_permissions:
            return self.custom_permissions[agent].get('permissions', [])
        
        if agent in self.AGENT_PERMISSIONS:
            return self.AGENT_PERMISSIONS[agent].get('permissions', [])
        
        # 返回默认权限
        return self.AGENT_PERMISSIONS.get('default', {}).get('permissions', [])
    
    def set_agent_permissions(self, agent: str, permissions: List[str], description: str = ''):
        """设置Agent权限"""
        self.custom_permissions[agent] = {
            'permissions': permissions,
            'description': description
        }
    
    def add_permission(self, agent: str, permission: str):
        """添加权限"""
        if agent not in self.custom_permissions:
            self.custom_permissions[agent] = {
                'permissions': [],
                'description': ''
            }
        
        perms = self.custom_permissions[agent]['permissions']
        if permission not in perms:
            perms.append(permission)
    
    def remove_permission(self, agent: str, permission: str):
        """移除权限"""
        if agent in self.custom_permissions:
            perms = self.custom_permissions[agent]['permissions']
            if permission in perms:
                perms.remove(permission)
    
    def has_permission(self, agent: str, permission: str) -> bool:
        """检查是否有权限"""
        perms = self.get_agent_permissions(agent)
        return permission in perms
    
    # ========== 权限验证 ==========
    
    def validate(self, agent: str, permission: str) -> dict:
        """
        验证权限
        
        Returns:
            dict: {
                'allowed': bool,
                'reason': str,
                'permissions': List[str]
            }
        """
        self.stats['total_checks'] += 1
        
        # 获取权限
        perms = self.get_agent_permissions(agent)
        
        # 检查权限
        if permission in perms:
            self.stats['allowed'] += 1
            self._log('check', agent, permission, True)
            
            return {
                'allowed': True,
                'reason': '权限验证通过',
                'permissions': perms
            }
        
        self.stats['denied'] += 1
        self._log('check', agent, permission, False)
        
        return {
            'allowed': False,
            'reason': f'权限不足: 需要 {permission}',
            'permissions': perms
        }
    
    def check(self, agent: str, permission: str) -> bool:
        """检查并抛出异常"""
        result = self.validate(agent, permission)
        
        if not result['allowed']:
            raise PermissionError(
                f"🚫 权限不足\n"
                f"Agent: {agent}\n"
                f"需要权限: {permission}\n"
                f"已有权限: {result['permissions']}"
            )
        
        return True
    
    # ========== 批量权限 ==========
    
    def validate_all(self, agent: str, permissions: List[str]) -> dict:
        """验证多个权限"""
        allowed_permissions = self.get_agent_permissions(agent)
        
        missing = [p for p in permissions if p not in allowed_permissions]
        
        if missing:
            return {
                'allowed': False,
                'missing': missing,
                'reason': f'缺少权限: {missing}'
            }
        
        return {
            'allowed': True,
            'reason': '所有权限验证通过'
        }
    
    def validate_any(self, agent: str, permissions: List[str]) -> dict:
        """验证任一权限"""
        allowed_permissions = self.get_agent_permissions(agent)
        
        granted = [p for p in permissions if p in allowed_permissions]
        
        if granted:
            return {
                'allowed': True,
                'granted': granted,
                'reason': f'已获得权限: {granted}'
            }
        
        return {
            'allowed': False,
            'reason': f'没有任何所需权限: {permissions}'
        }
    
    # ========== 会话权限 ==========
    
    def create_session(self, agent: str, session_id: str) -> Set[str]:
        """创建会话并分配权限"""
        perms = set(self.get_agent_permissions(agent))
        self.session_permissions[session_id] = perms
        return perms
    
    def check_session(self, session_id: str, permission: str) -> bool:
        """检查会话权限"""
        if session_id not in self.session_permissions:
            return False
        return permission in self.session_permissions[session_id]
    
    def revoke_session(self, session_id: str):
        """撤销会话"""
        if session_id in self.session_permissions:
            del self.session_permissions[session_id]
    
    # ========== 查询 ==========
    
    def list_agents(self) -> Dict[str, dict]:
        """列出所有Agent及其权限"""
        result = {}
        
        for agent, config in self.AGENT_PERMISSIONS.items():
            result[agent] = {
                'permissions': config.get('permissions', []),
                'description': config.get('description', '')
            }
        
        return result
    
    def list_permissions(self) -> Dict[str, str]:
        """列出所有权限"""
        return self.PERMISSIONS.copy()
    
    def get_stats(self) -> dict:
        return self.stats.copy()


# 全局实例
_guard = None

def get_guard() -> EnhancedPermissionGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedPermissionGuard()
    return _guard

def check_permission(agent: str, permission: str) -> bool:
    return get_guard().check(agent, permission)

def validate_permission(agent: str, permission: str) -> dict:
    return get_guard().validate(agent, permission)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Permission Guard 测试 ===\n")
    
    # 列出Agent
    print("Agent权限配置:")
    for agent, config in guard.list_agents().items():
        print(f"\n{agent}:")
        print(f"  描述: {config['description']}")
        print(f"  权限: {config['permissions']}")
    
    print("\n" + "=" * 50)
    
    # 测试权限
    tests = [
        ('crawler', 'read_project'),
        ('crawler', 'execute_command'),
        ('engineer', 'execute_command'),
        ('main', 'delete_project'),
        ('researcher', 'api_call'),
    ]
    
    print("\n权限验证:")
    for agent, permission in tests:
        result = guard.validate(agent, permission)
        status = "✅" if result['allowed'] else "❌"
        print(f"  {agent:12} -> {permission:20} {status}")
    
    print(f"\n统计: {guard.get_stats()}")
