import os
import re
from pathlib import Path
from typing import List, Optional
from enum import Enum


class SecurityLevel(Enum):
    """Security levels for operations"""
    LOW = "low"  # Read-only operations
    MEDIUM = "medium"  # File modifications
    HIGH = "high"  # System commands
    CRITICAL = "critical"  # Destructive operations


class SecurityValidator:
    """Validates operations for security concerns"""

    # Patterns that indicate potentially dangerous operations
    DANGEROUS_COMMAND_PATTERNS = [
        r'rm\s+-rf\s+/',  # Recursive force remove from root
        r'dd\s+if=',  # Disk operations
        r'mkfs\.',  # Filesystem creation
        r':(){ :|:& };:',  # Fork bomb
        r'curl.*\|\s*bash',  # Pipe curl to bash
        r'wget.*\|\s*bash',  # Pipe wget to bash
        r'chmod\s+777',  # Overly permissive permissions
        r'chown\s+root',  # Change ownership to root
        r'sudo\s+',  # Sudo operations (require explicit permission)
    ]

    # File extensions that should never be executed
    DANGEROUS_EXTENSIONS = [
        '.exe', '.dll', '.so', '.dylib',
        '.scr', '.bat', '.cmd', '.vbs',
        '.app', '.deb', '.rpm'
    ]

    # Sensitive directories
    SENSITIVE_DIRECTORIES = [
        '/etc',
        '/bin',
        '/sbin',
        '/boot',
        '/sys',
        '/proc',
        '/private/etc',
        '/System',
        '/Library/LaunchDaemons',
        '/Library/LaunchAgents',
    ]

    # Sensitive files
    SENSITIVE_FILES = [
        'passwd', 'shadow', 'sudoers', 'hosts',
        'id_rsa', 'id_ed25519', 'authorized_keys',
        '.env', 'credentials', 'secrets'
    ]

    @classmethod
    def validate_command(cls, command: str) -> tuple[bool, Optional[str]]:
        """
        Validate a bash command for security concerns

        Returns:
            (is_safe, warning_message)
        """
        # Check for dangerous patterns
        for pattern in cls.DANGEROUS_COMMAND_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Dangerous command pattern detected: {pattern}"

        # Warn about network operations
        if any(keyword in command.lower() for keyword in ['curl', 'wget', 'nc', 'netcat']):
            return True, "Network operation detected - ensure this is intended"

        # Warn about package installations
        if any(keyword in command.lower() for keyword in ['apt install', 'yum install', 'brew install', 'pip install']):
            return True, "Package installation detected - verify the package source"

        return True, None

    @classmethod
    def validate_file_path(cls, file_path: str, operation: str = "read") -> tuple[bool, Optional[str]]:
        """
        Validate a file path for security concerns

        Args:
            file_path: The path to validate
            operation: Type of operation (read, write, execute)

        Returns:
            (is_safe, warning_message)
        """
        try:
            path = Path(file_path).resolve()

            # Check for path traversal
            cwd = Path.cwd().resolve()
            # Allow operations within reasonable scope (current dir and home)
            home = Path.home().resolve()

            is_in_cwd = str(path).startswith(str(cwd))
            is_in_home = str(path).startswith(str(home))

            if not (is_in_cwd or is_in_home):
                return False, (
                    f"File path '{path}' is outside allowed scope.\n"
                    f"Allowed paths:\n"
                    f"  - Current directory: {cwd}\n"
                    f"  - Home directory: {home}\n"
                    f"Use absolute paths within these directories."
                )

            # Check for sensitive directories
            for sensitive_dir in cls.SENSITIVE_DIRECTORIES:
                if str(path).startswith(sensitive_dir):
                    return False, f"Access to sensitive directory denied: {sensitive_dir}"

            # Check for sensitive files
            if path.name.lower() in cls.SENSITIVE_FILES:
                if operation in ['write', 'execute']:
                    return False, f"Write/execute operation on sensitive file denied: {path.name}"
                else:
                    return True, f"Reading sensitive file: {path.name}"

            # Check file extension for execution
            if operation == "execute":
                if path.suffix.lower() in cls.DANGEROUS_EXTENSIONS:
                    return False, f"Execution of {path.suffix} files is not allowed"

            return True, None

        except Exception as e:
            return False, f"Path validation error: {str(e)}"

    @classmethod
    def validate_network_access(cls, url: str) -> tuple[bool, Optional[str]]:
        """
        Validate network access

        Returns:
            (is_allowed, warning_message)
        """
        # For local-only mode, we might want to restrict network access
        # This is a placeholder for future network security features

        # Warn about non-HTTPS
        if url.startswith('http://') and not url.startswith('http://localhost'):
            return True, "Non-HTTPS URL detected - data may be transmitted insecurely"

        return True, None

    @classmethod
    def get_security_level(cls, operation_type: str) -> SecurityLevel:
        """Get the security level for an operation type"""
        security_levels = {
            "read": SecurityLevel.LOW,
            "write": SecurityLevel.MEDIUM,
            "edit": SecurityLevel.MEDIUM,
            "bash": SecurityLevel.HIGH,
            "git": SecurityLevel.MEDIUM,
            "delete": SecurityLevel.CRITICAL,
        }

        return security_levels.get(operation_type.lower(), SecurityLevel.MEDIUM)

    @classmethod
    def sanitize_output(cls, output: str, max_length: int = 50000) -> str:
        """
        Sanitize output to prevent information leakage.

        Args:
            output: The output string to sanitize
            max_length: Maximum length before truncation (default: 50000)

        Returns:
            Sanitized output with secrets redacted and length limited

        Security:
            Redacts common secret patterns including passwords, tokens, API keys,
            SSH keys, AWS credentials, and connection strings.
        """
        # Truncate
        if len(output) > max_length:
            output = output[:max_length] + "\n... [output truncated for security]"

        # Enhanced redaction patterns (more comprehensive)
        patterns = [
            # Basic credentials
            (r'password["\s:=]+[\'"]?[\w\-\.!@#$%^&*()]+[\'"]?', 'password=***REDACTED***'),
            (r'passwd["\s:=]+[\'"]?[\w\-\.!@#$%^&*()]+[\'"]?', 'passwd=***REDACTED***'),
            (r'pwd["\s:=]+[\'"]?[\w\-\.!@#$%^&*()]+[\'"]?', 'pwd=***REDACTED***'),

            # API keys and tokens
            (r'token["\s:=]+[\'"]?[\w\-\.]+[\'"]?', 'token=***REDACTED***'),
            (r'api[_\-]?key["\s:=]+[\'"]?[\w\-\.]+[\'"]?', 'api_key=***REDACTED***'),
            (r'bearer\s+[\w\-\.]+', 'bearer ***REDACTED***'),
            (r'authorization:\s*[\w\-\.]+', 'authorization: ***REDACTED***'),

            # Secrets
            (r'secret["\s:=]+[\'"]?[\w\-\.]+[\'"]?', 'secret=***REDACTED***'),
            (r'private[_\-]?key["\s:=]+[\'"]?[\w\-\.]+[\'"]?', 'private_key=***REDACTED***'),

            # AWS credentials
            (r'aws[_\-]?access[_\-]?key[_\-]?id["\s:=]+[\'"]?[\w]+[\'"]?', 'aws_access_key_id=***REDACTED***'),
            (r'aws[_\-]?secret[_\-]?access[_\-]?key["\s:=]+[\'"]?[\w\-/+=]+[\'"]?', 'aws_secret_access_key=***REDACTED***'),
            (r'AKIA[0-9A-Z]{16}', '***REDACTED_AWS_KEY***'),

            # SSH keys
            (r'-----BEGIN [\w\s]+ PRIVATE KEY-----[\s\S]*?-----END [\w\s]+ PRIVATE KEY-----', '***REDACTED_PRIVATE_KEY***'),
            (r'ssh-rsa\s+[\w+/=]+', 'ssh-rsa ***REDACTED***'),
            (r'ssh-ed25519\s+[\w+/=]+', 'ssh-ed25519 ***REDACTED***'),

            # Database connection strings
            (r'mongodb(\+srv)?://[^:]+:[^@]+@[\w\-\.]+', 'mongodb://***REDACTED***'),
            (r'postgres://[^:]+:[^@]+@[\w\-\.]+', 'postgres://***REDACTED***'),
            (r'mysql://[^:]+:[^@]+@[\w\-\.]+', 'mysql://***REDACTED***'),

            # JWT tokens
            (r'eyJ[\w\-_]+\.eyJ[\w\-_]+\.[\w\-_]+', '***REDACTED_JWT***'),

            # Generic base64 encoded secrets (high entropy strings)
            (r'(?:secret|key|token|password)["\s:=]+[\'"]?[A-Za-z0-9+/]{32,}={0,2}[\'"]?', 'secret=***REDACTED***'),
        ]

        for pattern, replacement in patterns:
            output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)

        return output
