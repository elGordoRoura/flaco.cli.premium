"""Tests for file tools"""

import unittest
import tempfile
import os
from pathlib import Path
from flaco.tools.file_tools import ReadTool, WriteTool, EditTool, GlobTool
from flaco.tools.base import ToolStatus


class TestFileTools(unittest.TestCase):
    """Test file operation tools"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")

    def tearDown(self):
        """Clean up"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_tool(self):
        """Test writing a file"""
        write_tool = WriteTool()
        result = write_tool.execute(
            file_path=self.test_file,
            content="Hello, World!"
        )
        self.assertEqual(result.status, ToolStatus.SUCCESS)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), "Hello, World!")

    def test_read_tool(self):
        """Test reading a file"""
        # Write test content first
        with open(self.test_file, 'w') as f:
            f.write("Test content\nLine 2\nLine 3")

        read_tool = ReadTool()
        result = read_tool.execute(file_path=self.test_file)

        self.assertEqual(result.status, ToolStatus.SUCCESS)
        self.assertIn("Test content", result.output)
        self.assertIn("Line 2", result.output)

    def test_read_tool_nonexistent(self):
        """Test reading nonexistent file"""
        read_tool = ReadTool()
        result = read_tool.execute(file_path="/nonexistent/file.txt")
        self.assertEqual(result.status, ToolStatus.ERROR)

    def test_edit_tool_success(self):
        """Test editing a file"""
        # Write initial content
        with open(self.test_file, 'w') as f:
            f.write("Hello World")

        edit_tool = EditTool()
        result = edit_tool.execute(
            file_path=self.test_file,
            old_string="World",
            new_string="Flaco"
        )

        self.assertEqual(result.status, ToolStatus.SUCCESS)

        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), "Hello Flaco")

    def test_edit_tool_string_not_found(self):
        """Test editing with nonexistent string"""
        with open(self.test_file, 'w') as f:
            f.write("Hello World")

        edit_tool = EditTool()
        result = edit_tool.execute(
            file_path=self.test_file,
            old_string="Nonexistent",
            new_string="Replacement"
        )

        self.assertEqual(result.status, ToolStatus.ERROR)
        self.assertIn("not found", result.error)

    def test_edit_tool_multiple_occurrences(self):
        """Test editing with multiple occurrences"""
        with open(self.test_file, 'w') as f:
            f.write("test test test")

        edit_tool = EditTool()
        result = edit_tool.execute(
            file_path=self.test_file,
            old_string="test",
            new_string="replaced",
            replace_all=True
        )

        self.assertEqual(result.status, ToolStatus.SUCCESS)

        with open(self.test_file, 'r') as f:
            self.assertEqual(f.read(), "replaced replaced replaced")

    def test_glob_tool(self):
        """Test file globbing"""
        # Create test files
        os.makedirs(os.path.join(self.temp_dir, "subdir"), exist_ok=True)
        Path(os.path.join(self.temp_dir, "file1.py")).touch()
        Path(os.path.join(self.temp_dir, "file2.py")).touch()
        Path(os.path.join(self.temp_dir, "file3.txt")).touch()
        Path(os.path.join(self.temp_dir, "subdir", "file4.py")).touch()

        glob_tool = GlobTool()
        result = glob_tool.execute(
            pattern="**/*.py",
            path=self.temp_dir
        )

        self.assertEqual(result.status, ToolStatus.SUCCESS)
        self.assertIn("file1.py", result.output)
        self.assertIn("file2.py", result.output)
        self.assertIn("file4.py", result.output)
        self.assertNotIn("file3.txt", result.output)


if __name__ == '__main__':
    unittest.main()
