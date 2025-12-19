class ToolRegistry {
  static getAnthropicTools() {
    return [
      {
        name: "execute_bash",
        description: "Execute a bash command in the terminal. Use this to run scripts, install packages, check system status, etc. Returns stdout and stderr.",
        input_schema: {
          type: "object",
          properties: {
            command: {
              type: "string",
              description: "The bash command to execute (e.g., 'ls -la', 'npm install', 'git status')"
            }
          },
          required: ["command"]
        }
      },
      {
        name: "read_file",
        description: "Read the contents of a file. Use this to examine code, configuration, or any text file.",
        input_schema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Absolute or relative path to the file"
            }
          },
          required: ["path"]
        }
      },
      {
        name: "write_file",
        description: "Write content to a file. Creates the file if it doesn't exist, overwrites if it does.",
        input_schema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Absolute or relative path to the file"
            },
            content: {
              type: "string",
              description: "The content to write to the file"
            }
          },
          required: ["path", "content"]
        }
      },
      {
        name: "list_files",
        description: "List files and directories in a given path. Useful for exploring project structure.",
        input_schema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Directory path to list (defaults to current directory)"
            },
            recursive: {
              type: "boolean",
              description: "Whether to list recursively"
            }
          },
          required: ["path"]
        }
      },
      {
        name: "git_status",
        description: "Get the current git repository status. Shows modified files, staged changes, branch info.",
        input_schema: {
          type: "object",
          properties: {
            repo_path: {
              type: "string",
              description: "Path to the git repository (defaults to current directory)"
            }
          },
          required: []
        }
      },
      {
        name: "git_diff",
        description: "Show git diff for modified files.",
        input_schema: {
          type: "object",
          properties: {
            repo_path: {
              type: "string",
              description: "Path to the git repository"
            },
            file_path: {
              type: "string",
              description: "Optional: specific file to diff"
            }
          },
          required: []
        }
      },
      {
        name: "git_commit",
        description: "Create a git commit with staged changes.",
        input_schema: {
          type: "object",
          properties: {
            message: {
              type: "string",
              description: "Commit message"
            },
            repo_path: {
              type: "string",
              description: "Path to the git repository"
            }
          },
          required: ["message"]
        }
      }
    ];
  }

  static getOpenAITools() {
    // Convert Anthropic format to OpenAI format
    return this.getAnthropicTools().map(tool => ({
      type: "function",
      function: {
        name: tool.name,
        description: tool.description,
        parameters: tool.input_schema
      }
    }));
  }
}

module.exports = ToolRegistry;
