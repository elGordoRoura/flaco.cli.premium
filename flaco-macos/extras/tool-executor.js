const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs').promises;
const path = require('path');

const execAsync = promisify(exec);

class ToolExecutor {
  constructor() {
    this.workingDirectory = process.cwd();
  }

  async executeBash(command) {
    try {
      const { stdout, stderr } = await execAsync(command, {
        cwd: this.workingDirectory,
        timeout: 30000, // 30 second timeout
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer
      });

      return {
        success: true,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        output: stdout.trim() || stderr.trim()
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        stdout: error.stdout || '',
        stderr: error.stderr || '',
        output: `Error: ${error.message}\n${error.stderr || ''}`
      };
    }
  }

  async readFile(filePath) {
    try {
      const resolvedPath = path.resolve(this.workingDirectory, filePath);
      const content = await fs.readFile(resolvedPath, 'utf-8');

      return {
        success: true,
        content,
        path: resolvedPath
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to read file: ${error.message}`
      };
    }
  }

  async writeFile(filePath, content) {
    try {
      const resolvedPath = path.resolve(this.workingDirectory, filePath);

      // Ensure directory exists
      await fs.mkdir(path.dirname(resolvedPath), { recursive: true });

      await fs.writeFile(resolvedPath, content, 'utf-8');

      return {
        success: true,
        path: resolvedPath,
        message: `File written successfully: ${resolvedPath}`
      };
    } catch (error) {
      return {
        success: false,
        error: `Failed to write file: ${error.message}`
      };
    }
  }

  async listFiles(dirPath, recursive = false) {
    try {
      const resolvedPath = path.resolve(this.workingDirectory, dirPath);

      if (recursive) {
        // Use bash for recursive listing
        const { stdout } = await execAsync(`find "${resolvedPath}" -type f`, {
          cwd: this.workingDirectory
        });
        return {
          success: true,
          files: stdout.trim().split('\n').filter(f => f)
        };
      } else {
        const files = await fs.readdir(resolvedPath);
        return {
          success: true,
          files
        };
      }
    } catch (error) {
      return {
        success: false,
        error: `Failed to list files: ${error.message}`
      };
    }
  }

  async gitStatus(repoPath = '.') {
    try {
      const { stdout } = await execAsync('git status', {
        cwd: path.resolve(this.workingDirectory, repoPath)
      });

      return {
        success: true,
        output: stdout.trim()
      };
    } catch (error) {
      return {
        success: false,
        error: `Git status failed: ${error.message}`
      };
    }
  }

  async gitDiff(repoPath = '.', filePath = null) {
    try {
      const command = filePath
        ? `git diff "${filePath}"`
        : 'git diff';

      const { stdout } = await execAsync(command, {
        cwd: path.resolve(this.workingDirectory, repoPath)
      });

      return {
        success: true,
        diff: stdout.trim()
      };
    } catch (error) {
      return {
        success: false,
        error: `Git diff failed: ${error.message}`
      };
    }
  }

  async gitCommit(message, repoPath = '.') {
    try {
      // Escape quotes in message
      const escapedMessage = message.replace(/"/g, '\\"');

      const { stdout } = await execAsync(`git commit -m "${escapedMessage}"`, {
        cwd: path.resolve(this.workingDirectory, repoPath)
      });

      return {
        success: true,
        output: stdout.trim()
      };
    } catch (error) {
      return {
        success: false,
        error: `Git commit failed: ${error.message}`,
        output: error.stderr || error.message
      };
    }
  }

  async executeToolCall(toolName, input) {
    console.log(`[ToolExecutor] Executing tool: ${toolName}`, input);

    switch (toolName) {
      case 'execute_bash':
        return await this.executeBash(input.command);

      case 'read_file':
        return await this.readFile(input.path);

      case 'write_file':
        return await this.writeFile(input.path, input.content);

      case 'list_files':
        return await this.listFiles(input.path, input.recursive);

      case 'git_status':
        return await this.gitStatus(input.repo_path);

      case 'git_diff':
        return await this.gitDiff(input.repo_path, input.file_path);

      case 'git_commit':
        return await this.gitCommit(input.message, input.repo_path);

      default:
        return {
          success: false,
          error: `Unknown tool: ${toolName}`
        };
    }
  }
}

module.exports = ToolExecutor;
