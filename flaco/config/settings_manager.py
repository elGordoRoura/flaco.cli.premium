"""
Hierarchical Settings Manager for Flaco CLI
Implements Claude Code-style settings with precedence:
1. Enterprise Managed (highest)
2. Command line arguments
3. Local project (.flaco/settings.local.json)
4. Shared project (.flaco/settings.json)
5. User (~/.flaco/settings.json) (lowest)
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class PermissionRules:
    """Permission rules for tools"""
    allow: List[str] = field(default_factory=list)
    deny: List[str] = field(default_factory=list)
    ask: List[str] = field(default_factory=list)
    additional_directories: List[str] = field(default_factory=list)
    default_mode: str = "interactive"  # interactive, acceptEdits, auto, headless
    disable_bypass_permissions_mode: Optional[str] = None


@dataclass
class SandboxConfig:
    """Sandbox configuration for bash commands"""
    enabled: bool = False
    auto_allow_bash_if_sandboxed: bool = True
    excluded_commands: List[str] = field(default_factory=list)
    allow_unsandboxed_commands: bool = True
    network_allow_unix_sockets: List[str] = field(default_factory=list)
    network_allow_local_binding: bool = False
    network_http_proxy_port: Optional[int] = None
    network_socks_proxy_port: Optional[int] = None
    enable_weaker_nested_sandbox: bool = False


@dataclass
class FlacoSettings:
    """Complete Flaco CLI settings"""
    # Core settings
    model: Optional[str] = None
    ollama_url: str = "http://192.168.20.3:11434"
    api_key_helper: Optional[str] = None
    cleanup_period_days: int = 30
    company_announcements: List[str] = field(default_factory=list)

    # Environment
    env: Dict[str, str] = field(default_factory=dict)

    # Permissions
    permissions: PermissionRules = field(default_factory=PermissionRules)

    # Sandbox
    sandbox: SandboxConfig = field(default_factory=SandboxConfig)

    # Attribution
    attribution: Dict[str, str] = field(default_factory=lambda: {
        "commit": "🤖 Generated with Flaco CLI\n\nCo-Authored-By: Flaco AI <noreply@flaco.ai>",
        "pr": "🤖 Generated with Flaco CLI"
    })
    include_co_authored_by: bool = True  # Deprecated, use attribution

    # Tool settings
    allowed_tools: List[str] = field(default_factory=list)
    disabled_tools: List[str] = field(default_factory=list)

    # Output
    output_style: str = "Explanatory"  # Explanatory, Concise, Technical
    status_line: Optional[Dict[str, Any]] = None

    # MCP
    enable_all_project_mcp_servers: bool = False
    enabled_mcp_json_servers: List[str] = field(default_factory=list)
    disabled_mcp_json_servers: List[str] = field(default_factory=list)
    allowed_mcp_servers: Optional[List[Dict[str, str]]] = None
    denied_mcp_servers: Optional[List[Dict[str, str]]] = None

    # Plugins
    enabled_plugins: Dict[str, bool] = field(default_factory=dict)
    extra_known_marketplaces: Dict[str, Any] = field(default_factory=dict)

    # Thinking
    always_thinking_enabled: bool = False
    max_thinking_tokens: Optional[int] = None

    # Misc
    force_login_method: Optional[str] = None
    force_login_org_uuid: Optional[str] = None
    disable_all_hooks: bool = False
    hooks: Dict[str, Any] = field(default_factory=dict)


class SettingsManager:
    """Manages hierarchical settings for Flaco CLI"""

    def __init__(self, working_dir: Optional[str] = None):
        self.working_dir = Path(working_dir or os.getcwd()).resolve()
        self.user_home = Path.home()

        # Settings file paths (in precedence order, highest first)
        self.managed_settings_path = self._get_managed_settings_path()
        self.user_settings_path = self.user_home / ".flaco" / "settings.json"
        self.project_settings_path = self.working_dir / ".flaco" / "settings.json"
        self.local_settings_path = self.working_dir / ".flaco" / "settings.local.json"

        # Ensure directories exist
        self.user_settings_path.parent.mkdir(parents=True, exist_ok=True)

        # Loaded settings (merged)
        self.settings: FlacoSettings = FlacoSettings()
        self._load_all_settings()

    def _get_managed_settings_path(self) -> Optional[Path]:
        """Get platform-specific managed settings path"""
        import platform
        system = platform.system()

        if system == "Darwin":  # macOS
            return Path("/Library/Application Support/FlacoCLI/managed-settings.json")
        elif system == "Linux" or system.startswith("CYGWIN"):
            return Path("/etc/flaco-cli/managed-settings.json")
        elif system == "Windows":
            return Path("C:/Program Files/FlacoCLI/managed-settings.json")

        return None

    def _load_json_file(self, path: Path) -> Dict[str, Any]:
        """Load JSON file if it exists"""
        if path.exists():
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to load {path}: {e}")
                return {}
        return {}

    def _load_all_settings(self):
        """Load and merge all settings files in precedence order"""
        # Load from lowest to highest precedence
        settings_list = [
            ("user", self.user_settings_path),
            ("project", self.project_settings_path),
            ("local", self.local_settings_path),
        ]

        merged = {}

        for name, path in settings_list:
            data = self._load_json_file(path)
            if data:
                logger.info(f"Loaded {name} settings from {path}")
                merged = self._merge_settings(merged, data)

        # Load managed settings last (highest precedence)
        if self.managed_settings_path:
            managed_data = self._load_json_file(self.managed_settings_path)
            if managed_data:
                logger.info(f"Loaded managed settings from {self.managed_settings_path}")
                merged = self._merge_settings(merged, managed_data)

        # Apply merged settings to dataclass
        self._apply_settings_dict(merged)

    def _merge_settings(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two settings dictionaries"""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_settings(result[key], value)
            elif key in result and isinstance(result[key], list) and isinstance(value, list):
                # For lists, append override to base
                result[key] = result[key] + value
            else:
                result[key] = value

        return result

    def _apply_settings_dict(self, data: Dict[str, Any]):
        """Apply settings dictionary to FlacoSettings dataclass"""
        # Core settings
        if "model" in data:
            self.settings.model = data["model"]
        if "ollama_url" in data:
            self.settings.ollama_url = data["ollama_url"]
        if "apiKeyHelper" in data:
            self.settings.api_key_helper = data["apiKeyHelper"]
        if "cleanupPeriodDays" in data:
            self.settings.cleanup_period_days = data["cleanupPeriodDays"]
        if "companyAnnouncements" in data:
            self.settings.company_announcements = data["companyAnnouncements"]

        # Environment
        if "env" in data:
            self.settings.env.update(data["env"])

        # Permissions
        if "permissions" in data:
            perm_data = data["permissions"]
            if "allow" in perm_data:
                self.settings.permissions.allow.extend(perm_data["allow"])
            if "deny" in perm_data:
                self.settings.permissions.deny.extend(perm_data["deny"])
            if "ask" in perm_data:
                self.settings.permissions.ask.extend(perm_data["ask"])
            if "additionalDirectories" in perm_data:
                self.settings.permissions.additional_directories.extend(perm_data["additionalDirectories"])
            if "defaultMode" in perm_data:
                self.settings.permissions.default_mode = perm_data["defaultMode"]
            if "disableBypassPermissionsMode" in perm_data:
                self.settings.permissions.disable_bypass_permissions_mode = perm_data["disableBypassPermissionsMode"]

        # Sandbox
        if "sandbox" in data:
            sand_data = data["sandbox"]
            if "enabled" in sand_data:
                self.settings.sandbox.enabled = sand_data["enabled"]
            if "autoAllowBashIfSandboxed" in sand_data:
                self.settings.sandbox.auto_allow_bash_if_sandboxed = sand_data["autoAllowBashIfSandboxed"]
            if "excludedCommands" in sand_data:
                self.settings.sandbox.excluded_commands.extend(sand_data["excludedCommands"])
            if "allowUnsandboxedCommands" in sand_data:
                self.settings.sandbox.allow_unsandboxed_commands = sand_data["allowUnsandboxedCommands"]
            if "network" in sand_data:
                net = sand_data["network"]
                if "allowUnixSockets" in net:
                    self.settings.sandbox.network_allow_unix_sockets.extend(net["allowUnixSockets"])
                if "allowLocalBinding" in net:
                    self.settings.sandbox.network_allow_local_binding = net["allowLocalBinding"]
                if "httpProxyPort" in net:
                    self.settings.sandbox.network_http_proxy_port = net["httpProxyPort"]
                if "socksProxyPort" in net:
                    self.settings.sandbox.network_socks_proxy_port = net["socksProxyPort"]
            if "enableWeakerNestedSandbox" in sand_data:
                self.settings.sandbox.enable_weaker_nested_sandbox = sand_data["enableWeakerNestedSandbox"]

        # Attribution
        if "attribution" in data:
            self.settings.attribution.update(data["attribution"])
        if "includeCoAuthoredBy" in data:
            self.settings.include_co_authored_by = data["includeCoAuthoredBy"]

        # Tool settings
        if "allowedTools" in data:
            self.settings.allowed_tools.extend(data["allowedTools"])
        if "disabledTools" in data:
            self.settings.disabled_tools.extend(data["disabledTools"])

        # Output
        if "outputStyle" in data:
            self.settings.output_style = data["outputStyle"]
        if "statusLine" in data:
            self.settings.status_line = data["statusLine"]

        # MCP
        if "enableAllProjectMcpServers" in data:
            self.settings.enable_all_project_mcp_servers = data["enableAllProjectMcpServers"]
        if "enabledMcpjsonServers" in data:
            self.settings.enabled_mcp_json_servers.extend(data["enabledMcpjsonServers"])
        if "disabledMcpjsonServers" in data:
            self.settings.disabled_mcp_json_servers.extend(data["disabledMcpjsonServers"])
        if "allowedMcpServers" in data:
            self.settings.allowed_mcp_servers = data["allowedMcpServers"]
        if "deniedMcpServers" in data:
            self.settings.denied_mcp_servers = data["deniedMcpServers"]

        # Plugins
        if "enabledPlugins" in data:
            self.settings.enabled_plugins.update(data["enabledPlugins"])
        if "extraKnownMarketplaces" in data:
            self.settings.extra_known_marketplaces.update(data["extraKnownMarketplaces"])

        # Thinking
        if "alwaysThinkingEnabled" in data:
            self.settings.always_thinking_enabled = data["alwaysThinkingEnabled"]
        if "maxThinkingTokens" in data:
            self.settings.max_thinking_tokens = data["maxThinkingTokens"]

        # Misc
        if "forceLoginMethod" in data:
            self.settings.force_login_method = data["forceLoginMethod"]
        if "forceLoginOrgUUID" in data:
            self.settings.force_login_org_uuid = data["forceLoginOrgUUID"]
        if "disableAllHooks" in data:
            self.settings.disable_all_hooks = data["disableAllHooks"]
        if "hooks" in data:
            self.settings.hooks.update(data["hooks"])

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return getattr(self.settings, key, default)

    def save_user_settings(self, settings: Dict[str, Any]):
        """Save settings to user settings file"""
        self.user_settings_path.parent.mkdir(parents=True, exist_ok=True)

        existing = self._load_json_file(self.user_settings_path)
        existing.update(settings)

        with open(self.user_settings_path, 'w') as f:
            json.dump(existing, f, indent=2)

        logger.info(f"Saved user settings to {self.user_settings_path}")

    def save_project_settings(self, settings: Dict[str, Any], local: bool = False):
        """Save settings to project settings file"""
        path = self.local_settings_path if local else self.project_settings_path
        path.parent.mkdir(parents=True, exist_ok=True)

        existing = self._load_json_file(path)
        existing.update(settings)

        with open(path, 'w') as f:
            json.dump(existing, f, indent=2)

        logger.info(f"Saved {'local' if local else 'project'} settings to {path}")
