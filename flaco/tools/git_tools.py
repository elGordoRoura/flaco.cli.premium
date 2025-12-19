import subprocess
import os
from typing import Dict, Any, Optional
from .base import Tool, ToolResult, ToolStatus


class GitTool(Tool):
    """Git operations helper"""

    def __init__(self):
        super().__init__(
            name="Git",
            description="Perform git operations (status, diff, log, commit, etc.)",
            requires_permission=True
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["status", "diff", "log", "add", "commit", "push", "pull", "branch", "checkout"],
                    "description": "The git operation to perform"
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Additional arguments for the git command"
                },
                "message": {
                    "type": "string",
                    "description": "Commit message (for commit operation)"
                }
            },
            "required": ["operation"]
        }

    def execute(
        self,
        operation: str,
        args: Optional[list] = None,
        message: Optional[str] = None
    ) -> ToolResult:
        try:
            cmd = ["git", operation]

            if args:
                cmd.extend(args)

            # Special handling for commit
            if operation == "commit" and message:
                cmd.extend(["-m", message])

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"

            status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.ERROR

            return ToolResult(
                status=status,
                output=output,
                metadata={"operation": operation, "return_code": result.returncode}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error executing git command: {str(e)}"
            )

    def get_repo_info(self) -> Dict[str, Any]:
        """Get information about the current git repository"""
        try:
            # Check if we're in a git repo
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return {"is_repo": False}

            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            )

            # Get remote URL
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True
            )

            return {
                "is_repo": True,
                "branch": branch_result.stdout.strip(),
                "remote": remote_result.stdout.strip() if remote_result.returncode == 0 else None
            }

        except Exception:
            return {"is_repo": False}
