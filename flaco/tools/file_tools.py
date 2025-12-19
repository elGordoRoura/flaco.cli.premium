import os
import glob as glob_module
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from .base import Tool, ToolResult, ToolStatus
from ..utils.security import SecurityValidator


class ReadTool(Tool):
    """Read file contents"""

    def __init__(self):
        super().__init__(
            name="Read",
            description="Read the contents of a file from the filesystem",
            requires_permission=False
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to read"
                },
                "offset": {
                    "type": "number",
                    "description": "Line number to start reading from (optional)"
                },
                "limit": {
                    "type": "number",
                    "description": "Number of lines to read (optional)"
                }
            },
            "required": ["file_path"]
        }

    def execute(self, file_path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> ToolResult:
        try:
            # Security validation
            is_safe, warning = SecurityValidator.validate_file_path(file_path, operation="read")
            if not is_safe:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Security check failed: {warning}"
                )

            if not os.path.exists(file_path):
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"File not found: {file_path}"
                )

            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Apply offset and limit
            start = (offset - 1) if offset else 0
            end = (start + limit) if limit else len(lines)
            lines = lines[start:end]

            # Format with line numbers
            output = ""
            for i, line in enumerate(lines, start=start + 1):
                # Truncate long lines
                if len(line) > 2000:
                    line = line[:2000] + "... [truncated]\n"
                output += f"{i:6d}\t{line}"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"file_path": file_path, "lines_read": len(lines)}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error reading file: {str(e)}"
            )


class WriteTool(Tool):
    """Write content to a file"""

    def __init__(self):
        super().__init__(
            name="Write",
            description="Write content to a file (creates new or overwrites existing)",
            requires_permission=True
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }

    def execute(self, file_path: str, content: str) -> ToolResult:
        try:
            # Security validation
            is_safe, warning = SecurityValidator.validate_file_path(file_path, operation="write")
            if not is_safe:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Security check failed: {warning}"
                )

            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"File written successfully: {file_path}",
                metadata={"file_path": file_path, "bytes_written": len(content)}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error writing file: {str(e)}"
            )


class EditTool(Tool):
    """Edit a file by replacing old string with new string"""

    def __init__(self):
        super().__init__(
            name="Edit",
            description="Perform exact string replacement in a file",
            requires_permission=True
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The absolute path to the file to edit"
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact string to replace"
                },
                "new_string": {
                    "type": "string",
                    "description": "The string to replace it with"
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default: false)"
                }
            },
            "required": ["file_path", "old_string", "new_string"]
        }

    def execute(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> ToolResult:
        try:
            # Security validation
            is_safe, warning = SecurityValidator.validate_file_path(file_path, operation="write")
            if not is_safe:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Security check failed: {warning}"
                )

            if not os.path.exists(file_path):
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"File not found: {file_path}"
                )

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if old_string exists
            if old_string not in content:
                # Try to find similar strings for better error message
                lines = content.split('\n')
                preview = '\n'.join(lines[:10]) if len(lines) > 10 else content
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=(
                        f"String not found in file '{file_path}'.\n"
                        f"Searched for: {old_string[:200]}...\n"
                        f"\nFile preview (first 10 lines):\n{preview[:500]}...\n"
                        f"\nTip: Make sure whitespace and indentation match exactly."
                    )
                )

            # Check if unique (unless replace_all is True)
            if not replace_all and content.count(old_string) > 1:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"String appears {content.count(old_string)} times. Use replace_all=true or provide more context"
                )

            # Perform replacement
            if replace_all:
                new_content = content.replace(old_string, new_string)
                count = content.count(old_string)
            else:
                new_content = content.replace(old_string, new_string, 1)
                count = 1

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"Successfully replaced {count} occurrence(s) in {file_path}",
                metadata={"file_path": file_path, "replacements": count}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error editing file: {str(e)}"
            )


class GlobTool(Tool):
    """Find files matching a pattern"""

    def __init__(self):
        super().__init__(
            name="Glob",
            description="Find files matching a glob pattern (e.g., '**/*.py')",
            requires_permission=False
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The glob pattern to match (e.g., '**/*.py', 'src/**/*.ts')"
                },
                "path": {
                    "type": "string",
                    "description": "The directory to search in (defaults to current directory)"
                }
            },
            "required": ["pattern"]
        }

    def execute(self, pattern: str, path: Optional[str] = None) -> ToolResult:
        try:
            search_path = path or os.getcwd()
            full_pattern = os.path.join(search_path, pattern)

            matches = glob_module.glob(full_pattern, recursive=True)
            matches = sorted(matches)

            # Get file modification times and sort by most recent
            files_with_times = []
            for match in matches:
                if os.path.isfile(match):
                    mtime = os.path.getmtime(match)
                    files_with_times.append((match, mtime))

            files_with_times.sort(key=lambda x: x[1], reverse=True)
            sorted_matches = [f[0] for f in files_with_times]

            output = "\n".join(sorted_matches) if sorted_matches else "No files found matching pattern"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"pattern": pattern, "matches": len(sorted_matches)}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error globbing files: {str(e)}"
            )


class GrepTool(Tool):
    """Search for patterns in files using ripgrep"""

    def __init__(self):
        super().__init__(
            name="Grep",
            description="Search for patterns in files (uses ripgrep if available, falls back to grep)",
            requires_permission=False
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "The regex pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "File or directory to search in"
                },
                "glob": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g., '*.py')"
                },
                "case_insensitive": {
                    "type": "boolean",
                    "description": "Case insensitive search"
                },
                "output_mode": {
                    "type": "string",
                    "enum": ["content", "files_with_matches", "count"],
                    "description": "Output mode: show content, just filenames, or counts"
                },
                "context_lines": {
                    "type": "number",
                    "description": "Number of context lines to show around matches"
                }
            },
            "required": ["pattern"]
        }

    def execute(
        self,
        pattern: str,
        path: Optional[str] = None,
        glob: Optional[str] = None,
        case_insensitive: bool = False,
        output_mode: str = "files_with_matches",
        context_lines: Optional[int] = None
    ) -> ToolResult:
        try:
            search_path = path or os.getcwd()

            # Try ripgrep first, fall back to grep
            cmd = self._build_rg_command(
                pattern, search_path, glob, case_insensitive, output_mode, context_lines
            )

            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = result.stdout if result.returncode in [0, 1] else result.stderr

                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=output or "No matches found",
                    metadata={"pattern": pattern, "path": search_path}
                )

            except FileNotFoundError:
                # ripgrep not available, use basic grep
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error="ripgrep (rg) not found. Please install ripgrep for better search performance."
                )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error searching: {str(e)}"
            )

    def _build_rg_command(
        self,
        pattern: str,
        path: str,
        glob: Optional[str],
        case_insensitive: bool,
        output_mode: str,
        context_lines: Optional[int]
    ) -> list:
        cmd = ["rg"]

        if case_insensitive:
            cmd.append("-i")

        if output_mode == "files_with_matches":
            cmd.append("-l")
        elif output_mode == "count":
            cmd.append("-c")
        else:  # content
            cmd.append("-n")  # line numbers
            if context_lines:
                cmd.extend(["-C", str(context_lines)])

        if glob:
            cmd.extend(["-g", glob])

        cmd.extend([pattern, path])

        return cmd
