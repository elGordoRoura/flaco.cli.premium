# 🚀 Flaco AI - Quick Start Guide

Get up and running with Flaco in 5 minutes!

## Prerequisites

1. **Ollama** installed and running
   ```bash
   # macOS/Linux
   curl https://ollama.ai/install.sh | sh

   # Or download from https://ollama.ai
   ```

2. **Pull a model**
   ```bash
   ollama pull llama3.1
   ```

3. **Python 3.9+**
   ```bash
   python3 --version
   ```

## Installation

### Option 1: Automated (Recommended)

```bash
git clone https://github.com/yourusername/flaco.ai.git
cd flaco.ai
./install.sh
```

### Option 2: Manual

```bash
git clone https://github.com/yourusername/flaco.ai.git
cd flaco.ai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Flaco
pip install -e .
```

## First Run

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Start Flaco
flaco
```

You should see:
```
╔═══════════════════════════════════════╗
║                                       ║
║          🦙 FLACO AI                  ║
║                                       ║
║    Local AI Coding Assistant          ║
║    Powered by Ollama                  ║
║                                       ║
╚═══════════════════════════════════════╝

✅ Connected to Ollama - Model: llama3.1:latest

🦙 You:
```

## Basic Usage

### Example 1: File Reading
```
🦙 You: Read the README.md file and summarize it
```

### Example 2: Code Writing
```
🦙 You: Create a Python script that sorts a list of numbers
```

### Example 3: Git Operations
```
🦙 You: Show me the git status and recent commits
```

### Example 4: Code Search
```
🦙 You: Find all Python files that import requests
```

## Configuration

### Change Ollama URL (if not using default)

```bash
flaco --ollama-url http://localhost:11434
```

### Change Model

```bash
flaco --model llama3.2
```

Or use the slash command:
```
🦙 You: /model llama3.2
```

### Set Up Project Context

Create a `FLACO.md` file in your project:

```bash
cp FLACO.md.template FLACO.md
# Edit FLACO.md with your project guidelines
```

Flaco will automatically load it on startup!

## Slash Commands

Type `/help` to see all commands:

- `/status` - Show current status
- `/models` - List available models
- `/context` - Show loaded FLACO.md
- `/todos` - Show task list
- `/clear` - Clear screen
- `/exit` - Exit Flaco

## Tips

1. **Use Interactive Mode**: Default mode asks before destructive operations
2. **Create FLACO.md**: Helps Flaco understand your project better
3. **Try Multimodal**: `@image:/path/to/image.png What's in this?`
4. **Check /status**: See what Flaco knows about your environment

## Troubleshooting

### Cannot connect to Ollama
```bash
# Check if Ollama is running
curl http://192.168.20.3:11434/api/tags

# Start Ollama (if needed)
ollama serve
```

### Permission denied
```bash
# Use auto-approve mode (careful!)
flaco --auto-approve
```

### Model not found
```bash
# List available models
ollama list

# Pull a model
ollama pull llama3.1
```

## Next Steps

1. ✅ Read the [README.md](README.md) for full documentation
2. ✅ Create a [FLACO.md](FLACO.md.template) for your project
3. ✅ Try custom commands in `.flaco/commands/`
4. ✅ Set up MCP servers for extended capabilities

## Getting Help

- Type `/help` in Flaco
- Read [README.md](README.md)
- Check [SECURITY.md](SECURITY.md) for security info
- Report issues on GitHub

---

**Happy coding with Flaco! 🦙**
