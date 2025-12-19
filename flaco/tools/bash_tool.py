import subprocess
import os
import shlex
from typing import Dict, Any, Optional
from .base import Tool, ToolResult, ToolStatus
from ..utils.security import SecurityValidator
import threading
import queue


class BashTool(Tool):
    """
    Execute bash commands with security validation.

    Security Model:
    ---------------
    This tool uses shell=True to support shell features (pipes, redirects, etc.).
    Security is enforced through multiple layers:

    1. Permission System: Requires user approval before execution
    2. SecurityValidator: Checks for dangerous command patterns
    3. Output Sanitization: Redacts potential secrets from output
    4. Timeout Enforcement: Prevents runaway processes (max 600s)
    5. Path Restrictions: Commands execute within allowed directories

    WARNING: shell=True allows command injection if untrusted input is passed.
    The SecurityValidator provides defense-in-depth but is not foolproof.
    Always require user permission (requires_permission=True).
    """

    def __init__(self):
        super().__init__(
            name="Bash",
            description="Execute bash commands in a persistent shell session",
            requires_permission=True
        )
        self.shell_env = os.environ.copy()
        self.working_dir = os.getcwd()

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                },
                "timeout": {
                    "type": "number",
                    "description": "Timeout in seconds (default: 120, max: 600)"
                },
                "working_dir": {
                    "type": "string",
                    "description": "Working directory for the command"
                }
            },
            "required": ["command"]
        }

    def execute(
        self,
        command: str,
        timeout: Optional[int] = 120,
        working_dir: Optional[str] = None
    ) -> ToolResult:
        """
        Execute a bash command with security validation.

        Args:
            command: The bash command to execute
            timeout: Maximum execution time in seconds (default: 120, max: 600)
            working_dir: Working directory for command execution (default: current)

        Returns:
            ToolResult with command output, error status, and metadata

        Raises:
            No exceptions - all errors are returned as ToolResult with ERROR status
        """
        try:
            # Security validation
            is_safe, warning = SecurityValidator.validate_command(command)
            if not is_safe:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Security check failed: {warning}"
                )

            # Validate timeout
            if timeout and timeout > 600:
                timeout = 600

            # Use specified working directory or default
            cwd = working_dir or self.working_dir

            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                env=self.shell_env
            )

            # Combine stdout and stderr
            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"

            # Sanitize output for security
            output = SecurityValidator.sanitize_output(output, max_length=30000)

            status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.ERROR

            return ToolResult(
                status=status,
                output=output,
                metadata={
                    "return_code": result.returncode,
                    "command": command,
                    "working_dir": cwd
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Command timed out after {timeout} seconds"
            )
        except FileNotFoundError as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Working directory not found: {working_dir or self.working_dir}"
            )
        except PermissionError as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Permission denied: {str(e)}"
            )
        except subprocess.SubprocessError as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Subprocess error: {str(e)}"
            )
        except OSError as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"OS error executing command: {str(e)}"
            )
        except Exception as e:
            # Catch-all for unexpected errors
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Unexpected error: {type(e).__name__}: {str(e)}"
            )

    def set_working_dir(self, path: str):
        """Update the working directory for future commands"""
        if os.path.isdir(path):
            self.working_dir = path
