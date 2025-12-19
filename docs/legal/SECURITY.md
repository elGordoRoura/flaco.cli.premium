# Security Policy

## Overview

Flaco AI is designed with security and privacy as core principles. This document outlines the security features and policies.

## Security Features

### 1. Local-Only Processing
- All AI processing happens on your local Ollama instance
- No data is sent to external servers
- Complete data privacy and control

### 2. Command Validation
Flaco automatically blocks dangerous commands including:
- Recursive force deletions (`rm -rf /`)
- Disk operations (`dd`, `mkfs`)
- Fork bombs
- Piping untrusted downloads to shell
- Overly permissive file permissions

### 3. File System Protection
Protected files and directories:
- System configuration files (`/etc`, `/sys`, `/proc`)
- SSH keys and credentials
- Sudo configuration
- Private system directories

### 4. Output Sanitization
Flaco automatically redacts sensitive information from outputs:
- Passwords
- API keys
- Authentication tokens
- Secret keys

### 5. Permission System
Three permission modes for different security needs:
- **Interactive**: Asks for permission before destructive operations (default)
- **Auto-approve**: Auto-approves all operations (use with caution)
- **Headless**: Denies all operations requiring permission (safest for automation)

## Reporting Security Vulnerabilities

If you discover a security vulnerability, please report it by:

1. **DO NOT** open a public issue
2. Email the details to: [your-security-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### For Users

1. **Use Interactive Mode**: Always use interactive mode unless you fully trust the operations
2. **Review Permissions**: Carefully review permission requests before approving
3. **Keep Updated**: Regularly update Flaco and dependencies
4. **Secure Ollama**: Ensure your Ollama instance is not exposed to the public internet
5. **Use FLACO.md**: Define clear guidelines to guide AI behavior

### For Developers

1. **Code Review**: All contributions undergo security review
2. **Input Validation**: Always validate and sanitize inputs
3. **Least Privilege**: Tools request minimum necessary permissions
4. **Secure Defaults**: Security features enabled by default
5. **Regular Audits**: Periodic security audits of the codebase

## Known Limitations

1. **Shell Commands**: Cannot guarantee 100% prevention of all dangerous commands
2. **LLM Behavior**: AI behavior depends on the underlying model
3. **Permissions**: User must exercise judgment when approving operations
4. **Network**: No network isolation for Ollama connections

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1 → 1.0.2).

Subscribe to releases on GitHub to be notified of security updates.

## Compliance

Flaco is designed to support:
- GDPR compliance (no external data transfer)
- HIPAA compliance (when properly configured)
- SOC 2 requirements (local processing)
- Enterprise security policies

## License

See [LICENSE](LICENSE) for license information.

---

Last Updated: 2024-12-07
