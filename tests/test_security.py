"""Tests for security validator"""

import unittest
from pathlib import Path
import tempfile
import os
from flaco.utils.security import SecurityValidator


class TestSecurityValidator(unittest.TestCase):
    """Test security validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cwd = Path.cwd()

    def tearDown(self):
        """Clean up"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_allow_current_directory(self):
        """Should allow files in current directory"""
        test_file = self.cwd / "test.txt"
        is_safe, msg = SecurityValidator.validate_file_path(str(test_file), "read")
        self.assertTrue(is_safe)

    def test_block_outside_scope(self):
        """Should block files outside allowed scope"""
        is_safe, msg = SecurityValidator.validate_file_path("/etc/passwd", "read")
        self.assertFalse(is_safe)
        self.assertIn("outside allowed scope", msg)

    def test_block_sensitive_files_write(self):
        """Should block writes to sensitive files"""
        sensitive_file = self.cwd / ".env"
        is_safe, msg = SecurityValidator.validate_file_path(str(sensitive_file), "write")
        self.assertFalse(is_safe)

    def test_allow_sensitive_files_read(self):
        """Should allow reading sensitive files with warning"""
        sensitive_file = self.cwd / "id_rsa"
        is_safe, msg = SecurityValidator.validate_file_path(str(sensitive_file), "read")
        self.assertTrue(is_safe)
        self.assertIn("Reading sensitive file", msg)

    def test_validate_command_dangerous(self):
        """Should block dangerous commands"""
        is_safe, msg = SecurityValidator.validate_command("rm -rf /")
        self.assertFalse(is_safe)

    def test_validate_command_safe(self):
        """Should allow safe commands"""
        is_safe, msg = SecurityValidator.validate_command("ls -la")
        self.assertTrue(is_safe)

    def test_sanitize_output_secrets(self):
        """Should redact secrets from output"""
        output = "API_KEY=sk_test_1234567890"
        sanitized = SecurityValidator.sanitize_output(output)
        self.assertIn("[REDACTED]", sanitized)
        self.assertNotIn("sk_test_1234567890", sanitized)


if __name__ == '__main__':
    unittest.main()
