import os
from pathlib import Path
from typing import Optional


def validate_path(path: str, must_exist: bool = False) -> bool:
    """
    Validate a file path for security.

    Args:
        path: The file path to validate
        must_exist: Whether the path must exist on the filesystem

    Returns:
        bool: True if path is safe, False otherwise

    Security:
        Only allows access within current working directory or home directory.
        Prevents path traversal attacks.
    """
    try:
        # Resolve to absolute path
        abs_path = Path(path).resolve()

        # Check for path traversal attempts
        # Allow access within cwd OR home directory (not parent)
        cwd = Path.cwd().resolve()
        home = Path.home().resolve()

        is_in_cwd = str(abs_path).startswith(str(cwd))
        is_in_home = str(abs_path).startswith(str(home))

        if not (is_in_cwd or is_in_home):
            # Path is outside of allowed scope
            return False

        # Check if must exist
        if must_exist and not abs_path.exists():
            return False

        return True

    except Exception:
        return False


def sanitize_command(command: str) -> str:
    """Basic command sanitization (not a complete security solution)"""
    # Remove potentially dangerous characters
    dangerous_patterns = [
        '; rm -rf',
        '&& rm -rf',
        '| rm -rf',
        '; curl',
        '&& curl',
        '| curl',
    ]

    cmd_lower = command.lower()
    for pattern in dangerous_patterns:
        if pattern in cmd_lower:
            raise ValueError(f"Potentially dangerous command pattern detected: {pattern}")

    return command


def is_safe_file_operation(file_path: str, operation: str = "read") -> bool:
    """Check if a file operation is safe"""
    try:
        abs_path = Path(file_path).resolve()

        # Don't allow operations on sensitive system files
        sensitive_patterns = [
            '/etc/passwd',
            '/etc/shadow',
            '/etc/sudoers',
            '/.ssh/',
            '/private/etc/',
        ]

        path_str = str(abs_path)
        for pattern in sensitive_patterns:
            if pattern in path_str:
                return False

        # For write operations, be extra cautious
        if operation in ['write', 'edit']:
            # Don't allow writing to common config files without explicit permission
            dangerous_files = [
                '.bashrc',
                '.zshrc',
                '.bash_profile',
                '.profile',
                'sudoers',
            ]

            if abs_path.name in dangerous_files:
                # Would require explicit user permission
                return False

        return True

    except Exception:
        return False


def truncate_output(output: str, max_length: int = 10000) -> str:
    """Truncate long output"""
    if len(output) <= max_length:
        return output
    return output[:max_length] + f"\n\n... [truncated {len(output) - max_length} characters]"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"
