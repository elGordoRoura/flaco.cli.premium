# 📦 Flaco Installation Guide

Complete installation guide for new users.

## 📋 Prerequisites

Before installing Flaco, ensure you have:

1. **Python 3.9 or higher**
   ```bash
   python3 --version  # Should show 3.9 or higher
   ```

2. **Ollama installed and running**
   - Download from: https://ollama.ai
   - Verify it's running:
     ```bash
     ollama list  # Should show your models
     ```

3. **Git** (for cloning the repository)
   ```bash
   git --version
   ```

## 🚀 Installation Methods

### Method 1: Quick Install (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flaco.ai.git
   cd flaco.ai
   ```

2. **Run the installer:**
   ```bash
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```

3. **Run Flaco:**
   ```bash
   flaco.cli
   ```

### Method 2: Manual Install

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/flaco.ai.git
   cd flaco.ai
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Run Flaco:**
   ```bash
   python -m flaco.cli
   ```

### Method 3: Global Install with pipx (Advanced)

1. **Install pipx** (if not already installed):
   ```bash
   python3 -m pip install --user pipx
   python3 -m pipx ensurepath
   ```

2. **Install Flaco globally:**
   ```bash
   cd flaco.ai
   pipx install .
   ```

3. **Run from anywhere:**
   ```bash
   flaco.cli
   ```

## ⚙️ First-Run Setup

When you run Flaco for the first time, it will guide you through setup:

1. **Ollama Configuration**
   - Enter your Ollama server URL (default: `192.168.20.3:11434`)
   - URL will automatically get `http://` prepended

2. **Model Selection**
   - Choose from your available Ollama models
   - Default: `qwen2.5-coder:32b`

3. **Theme Selection**
   - Choose your preferred color theme
   - Options: cyan (default), green, magenta, yellow, blue, white

4. **Permission Mode**
   - Interactive (asks before running commands)
   - Auto-approve (runs all commands automatically)
   - Headless (for automation, denies by default)

## 🔧 Configuration

Flaco stores configuration in `~/.flaco/config.json`

To reconfigure:
```bash
flaco.cli
# Then type: /setup
```

## 📍 Making Flaco Available Globally

### Option 1: Symlink to /usr/local/bin
```bash
sudo ln -sf /path/to/flaco.ai/bin/flaco.cli /usr/local/bin/flaco.cli
```

### Option 2: Add to PATH
Add to your `~/.zshrc` or `~/.bashrc`:
```bash
export PATH="/path/to/flaco.ai/bin:$PATH"
```

Then reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

## ✅ Verify Installation

Test that Flaco is working:

```bash
flaco.cli
```

You should see:
```
  ███████╗██╗      █████╗  ██████╗ ██████╗
  ██╔════╝██║     ██╔══██╗██╔════╝██╔═══██╗
  █████╗  ██║     ███████║██║     ██║   ██║
  ██╔══╝  ██║     ██╔══██║██║     ██║   ██║
  ██║     ███████╗██║  ██║╚██████╗╚██████╔╝
  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝

      ⚡ Local AI Coding Assistant
         Powered by Ollama
         Made by Roura.io
```

## 🐛 Troubleshooting

### "Command not found: flaco.cli"
- Check that the installation completed successfully
- Verify the PATH is set correctly
- Try using the full path: `python -m flaco.cli`

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama list`
- Check your Ollama URL in setup: `/setup`
- Verify network access to Ollama server

### "urllib3 OpenSSL warning"
- This warning has been suppressed in the code
- If you still see it, update to the latest version

### Python version errors
- Flaco requires Python 3.9+
- Check version: `python3 --version`
- Install newer Python if needed

## 🔄 Updating Flaco

To update to the latest version:

```bash
cd flaco.ai
git pull origin main
pip install -e . --upgrade
```

## 🗑️ Uninstalling

### If installed with pipx:
```bash
pipx uninstall flaco
```

### If installed manually:
```bash
rm -rf /path/to/flaco.ai
rm ~/.flaco/config.json  # Optional: removes config
rm ~/.flaco_history      # Optional: removes history
```

### Remove symlink:
```bash
sudo rm /usr/local/bin/flaco.cli
```

## 📚 Next Steps

- Read the [Quick Start Guide](QUICK_START.md)
- Learn about [Autocomplete Features](AUTOCOMPLETE_GUIDE.md)
- Explore [Quick Actions](TEST_COMMANDS.md)

## 💬 Support

Having issues?
- Check [GitHub Issues](https://github.com/yourusername/flaco.ai/issues)
- Read the [FAQ](CUSTOMER_SETUP.md)
- Contact support: support@roura.io

---

**Made by ⚡ Roura.io**
