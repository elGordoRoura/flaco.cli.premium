# Flaco CLI - Quick Start Guide

Welcome to Flaco! This guide will get you up and running in 5 minutes.

## Prerequisites

Before installing Flaco, you need:

1. **Python 3.9+**
   ```bash
   python3 --version  # Should be 3.9 or higher
   ```

2. **Ollama** (Local AI engine)
   - Download from: https://ollama.com
   - Or install via Homebrew (Mac): `brew install ollama`

## Step 1: Install Ollama & Pull a Model

```bash
# Start Ollama server (keep this running in a terminal)
ollama serve

# In a new terminal, pull a coding model (recommended for Flaco)
ollama pull qwen2.5-coder:7b

# Verify it's downloaded
ollama list
```

**Model Recommendations:**
- `qwen2.5-coder:7b` - Best balance of speed and quality (4.7GB) ✅ Recommended
- `qwen2.5-coder:1.5b` - Faster, smaller model (1.0GB)
- `llama3.1:8b` - General purpose, good for chat (4.7GB)

## Step 2: Install Flaco

```bash
# Install with pipx (recommended - isolated environment)
pipx install flaco-ai

# Or with pip
pip install flaco-ai
```

## Step 3: Run Flaco

```bash
# Start Flaco
flaco.cli

# Or specify a custom model
flaco.cli --model qwen2.5-coder:1.5b

# Or specify custom Ollama URL
flaco.cli --ollama-url http://localhost:11434
```

## Step 4: Your First Commands

Once Flaco starts, try these:

```
# Ask a coding question
> How do I read a JSON file in Python?

# File operations
> Read the setup.py file

# Create a new file
> Create a hello.py file that prints "Hello World"

# Git operations
> Show git status

# Create a todo list for a task
> Help me refactor this code (Flaco will use TodoWrite to track)
```

## Available Commands

### Slash Commands
- `/exit` - Quit Flaco
- `/clear` - Clear conversation history
- `/help` - Show help
- `/init` - Create FLACO.md context file
- `/context` - Show current context info

### Quick Actions (type `#` to see all)
Type `#` alone and press Enter to see all available quick actions.

### Tools Flaco Can Use

Flaco has access to these tools:
- **Read** - Read files
- **Write** - Create files
- **Edit** - Modify files
- **Glob** - Find files by pattern
- **Grep** - Search file contents
- **Bash** - Run terminal commands
- **Git** - Git operations
- **TodoWrite** - Track multi-step tasks

## Configuration

### Option 1: Command-Line Flags

```bash
flaco.cli \
  --model qwen2.5-coder:7b \
  --ollama-url http://localhost:11434 \
  --headless  # For automation/scripts
```

### Option 2: Project Context File

Create `.flaco/FLACO.md` in your project root:

```markdown
# Project Context

## Project Info
Name: My Awesome Project
Description: A web app built with React and FastAPI

## Tech Stack
- Frontend: React, TypeScript, Tailwind CSS
- Backend: Python, FastAPI, PostgreSQL
- Deployment: Docker, AWS

## Coding Guidelines
- Use TypeScript strict mode
- Follow PEP 8 for Python
- Write tests for all features
- Add JSDoc comments for public APIs
```

Then run:
```bash
flaco.cli /init  # Creates template
# Edit .flaco/FLACO.md with your details
flaco.cli        # Flaco now knows your project context!
```

## Troubleshooting

### "Failed to connect to Ollama"
**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check Ollama is on default port: `http://localhost:11434`
3. If using a different port: `flaco.cli --ollama-url http://localhost:YOUR_PORT`

### "Model not found"
**Solution:**
```bash
# List available models
ollama list

# Pull the model Flaco is trying to use
ollama pull qwen2.5-coder:7b

# Or specify a model you have
flaco.cli --model YOUR_MODEL_NAME
```

### "Permission denied" errors
Flaco has security restrictions:
- Can only access files in current directory or home directory
- Cannot write to sensitive files (.env, id_rsa, etc.)
- Cannot execute dangerous commands

To see allowed paths, the error message will show them.

### Tests failing
Install test dependencies:
```bash
pip install pytest
cd /path/to/flaco.cli
pytest tests/ -v
```

## Advanced Usage

### Running in Headless Mode (for scripts)

```bash
echo "Create a README.md file" | flaco.cli --headless
```

### Custom Slash Commands

Create custom commands in `.flaco/commands/`:

```bash
mkdir -p .flaco/commands
echo "Review this code for bugs and suggest improvements" > .flaco/commands/review.md
```

Then use with `/review` in Flaco.

### Agent Swarms

For complex tasks, Flaco automatically assembles agent teams:

```
> Create a full CRUD API with tests and documentation
# Flaco detects complexity and assigns:
# - 📝 Code Expert (implementation)
# - 🧪 Testing Agent (tests)
# - 📚 Documentation Agent (docs)
```

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Check [CHANGELOG.md](CHANGELOG.md) for latest updates
- Join discussions at https://github.com/RouraIO/flaco.cli/discussions

## Getting Help

- GitHub Issues: https://github.com/RouraIO/flaco.cli/issues
- Documentation: https://github.com/RouraIO/flaco.cli/tree/main/docs

---

Made with ❤️ by [Roura.io](https://github.com/RouraIO)
