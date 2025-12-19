from enum import Enum
from typing import Dict, Any, Callable, Optional
from rich.console import Console
from rich.prompt import Confirm
import sys


class PermissionMode(Enum):
    """Permission modes for tool execution"""
    INTERACTIVE = "interactive"  # Ask for permission
    AUTO_APPROVE = "auto_approve"  # Auto-approve all
    HEADLESS = "headless"  # No interaction, deny by default


class PermissionManager:
    """Manages permissions for tool execution"""

    def __init__(self, mode: PermissionMode = PermissionMode.INTERACTIVE):
        self.mode = mode
        self.console = Console()
        self.approved_tools: Dict[str, bool] = {}
        self.session_approvals: set = set()  # Tools approved for this session

    def request_permission(
        self,
        tool_name: str,
        action_description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Request permission to execute a tool"""

        # Check if user interrupted - deny permission if so
        try:
            from flaco.cli import interrupt_requested
            if interrupt_requested:
                return False
        except (ImportError, AttributeError):
            pass  # Flag not available, continue normally

        # Auto-approve mode
        if self.mode == PermissionMode.AUTO_APPROVE:
            return True

        # Headless mode - deny by default
        if self.mode == PermissionMode.HEADLESS:
            return False

        # Interactive mode
        # Check if already approved for this session
        if tool_name in self.session_approvals:
            return True

        # Format the permission request
        self.console.print(f"\n[yellow]🔐 Permission Request[/yellow]")
        self.console.print(f"[cyan]Tool:[/cyan] {tool_name}")
        self.console.print(f"[cyan]Action:[/cyan] {action_description}")

        if metadata:
            for key, value in metadata.items():
                self.console.print(f"[cyan]{key}:[/cyan] {value}")

        try:
            # Ask for permission with timeout/interrupt handling
            approved = Confirm.ask("\nAllow this action?", default=True)

            if approved:
                # Ask if they want to approve all uses of this tool this session
                approve_all = Confirm.ask(
                    f"Always approve '{tool_name}' for this session?",
                    default=False
                )
                if approve_all:
                    self.session_approvals.add(tool_name)

            return approved
        except (KeyboardInterrupt, EOFError):
            # User interrupted during permission prompt - deny
            self.console.print("\n[yellow]Permission denied (interrupted)[/yellow]")
            return False

    def set_mode(self, mode: PermissionMode):
        """Change permission mode"""
        self.mode = mode

    def clear_session_approvals(self):
        """Clear all session approvals"""
        self.session_approvals.clear()

    def is_auto_approved(self, tool_name: str) -> bool:
        """Check if a tool is auto-approved for this session"""
        return tool_name in self.session_approvals or self.mode == PermissionMode.AUTO_APPROVE
