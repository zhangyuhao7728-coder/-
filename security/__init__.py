"""
Security 模块 - 安全工具集
提供密钥管理、权限守卫、审计日志、沙盒环境、命令守卫等功能
"""
from .secrets_manager import (
    SecretsManager,
    get_secrets_manager,
    get_secret,
    get_required_secret,
)

from .permission_guard import (
    PermissionGuard,
    get_guard,
    check_file,
    check_command,
    scan_dir,
    fix_perm,
)

from .audit_logger import (
    AuditLogger,
    get_logger,
    log,
    audit_log,
)

from .sandbox import (
    Sandbox,
    get_sandbox,
    safe_read,
    safe_write,
    safe_list,
    safe_exec,
)

from .command_guard import (
    CommandGuard,
    get_command_guard,
    validate_command,
    check_command as cmd_check,
    add_allowed_command,
    add_allowed_dir,
)

from .filesystem_guard import (
    FileSystemGuard,
    get_fs_guard,
    validate_path,
    validate_file,
    check_path,
    check_file,
)

from .prompt_guard import (
    PromptGuard,
    get_prompt_guard,
    detect_prompt_attack,
    validate_prompt,
    check_prompt,
)

__all__ = [
    # Secrets Manager
    'SecretsManager',
    'get_secrets_manager',
    'get_secret',
    'get_required_secret',
    
    # Permission Guard
    'PermissionGuard',
    'get_guard',
    'check_file',
    'check_command',
    'scan_dir',
    'fix_perm',
    
    # Audit Logger
    'AuditLogger',
    'get_logger',
    'log',
    'audit_log',
    
    # Sandbox
    'Sandbox',
    'get_sandbox',
    'safe_read',
    'safe_write',
    'safe_list',
    'safe_exec',
    
    # Command Guard
    'CommandGuard',
    'get_command_guard',
    'validate_command',
    'add_allowed_command',
    'add_allowed_dir',
    
    # File System Guard
    'FileSystemGuard',
    'get_fs_guard',
    'validate_path',
    'validate_file',
    'check_path',
    'check_file',
    
    # Prompt Guard
    'PromptGuard',
    'get_prompt_guard',
    'detect_prompt_attack',
    'validate_prompt',
    'check_prompt',
    
    # Audit (集成)
    'SecurityAuditor',
    'get_auditor',
    'SecurityMiddleware',
]

__version__ = '1.0.0'
