# 🍎 Flaco AI PREMIUM Installation Guide for macOS

Complete installation guide for Flaco AI PREMIUM tier on macOS.

---

## Prerequisites

### 1. Check macOS Version

Flaco works on **macOS 10.15 (Catalina)** or later.

```bash
sw_vers
```

You should see something like:
```
ProductName:    macOS
ProductVersion: 14.0
BuildVersion:   23A344
```

### 2. Install Homebrew (if not installed)

Homebrew is the package manager for macOS. Check if it's installed:

```bash
brew --version
```

If not installed, install it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Follow the on-screen instructions to add Homebrew to your PATH.

---

## Step 1: Install Python 3.9+

### Check Current Python Version

```bash
python3 --version
```

If you have Python 3.9 or later, skip to Step 2.

### Install Python via Homebrew

```bash
brew install python@3.11
```

Verify installation:

```bash
python3 --version
# Should show: Python 3.11.x
```

---

## Step 2: Install Ollama

### Method 1: Download from Website (Recommended)

1. Visit [https://ollama.ai](https://ollama.ai)
2. Click "Download for Mac"
3. Open the downloaded `.dmg` file
4. Drag Ollama to Applications folder
5. Launch Ollama from Applications

### Method 2: Install via Homebrew

```bash
brew install ollama
```

### Verify Ollama Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve &
```

### Pull Recommended Model

```bash
# Pull the recommended coding model (4.7GB)
ollama pull qwen2.5-coder:7b

# Or for more powerful model (18GB)
ollama pull qwen2.5-coder:32b

# Verify model is installed
ollama list
```

---

## Step 3: Install pipx

pipx allows you to install Python applications in isolated environments.

```bash
brew install pipx
pipx ensurepath
```

**Important**: Close and reopen your terminal after running `pipx ensurepath`.

Verify installation:

```bash
pipx --version
```

---

## Step 4: Install Flaco AI

### Option 1: Install from PyPI (Coming Soon)

```bash
pipx install flaco-ai-premium
```

### Option 2: Install from GitHub (Current Method)

```bash
pipx install git+https://github.com/RouraIO/flaco.cli.premium.git
```

### Option 3: Development Install

If you want to modify Flaco or contribute:

```bash
# Clone the repository
git clone https://github.com/RouraIO/flaco.cli.premium.git
cd flaco.cli.premium

# Install in editable mode
pipx install -e .
```

---

## Step 5: Verify Installation

```bash
# Check if flaco-premium is installed
which flaco-premium

# Should show something like:
# /Users/yourusername/.local/bin/flaco-premium

# Check version
flaco-premium --version
```

---

## Step 6: First Run

Launch Flaco (you can use either command):

```bash
# Primary command
flaco-premium

# Or short alias
flacopro
```

You'll see the setup wizard:

```
  ███████╗██╗      █████╗  ██████╗ ██████╗
  ██╔════╝██║     ██╔══██╗██╔════╝██╔═══██╗
  █████╗  ██║     ███████║██║     ██║   ██║
  ██╔══╝  ██║     ██╔══██║██║     ██║   ██║
  ██║     ███████╗██║  ██║╚██████╗╚██████╔╝
  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝

⚡ Local AI Coding Assistant
   PREMIUM TIER - All Features Unlocked

👋 Welcome to Flaco! Let's get you set up...

? Ollama URL: http://localhost:11434
? Model: qwen2.5-coder:7b
? Theme color: cyan
? Permission mode: interactive

✅ Setup complete! Happy coding!
```

---

## Optional: Install ripgrep for Faster Search

ripgrep makes code searching much faster:

```bash
brew install ripgrep
```

---

## Troubleshooting

### "command not found: flaco-premium"

The pipx binaries directory is not in your PATH. Fix it:

```bash
pipx ensurepath
```

Then close and reopen your terminal.

Or manually add to your shell config (`~/.zshrc` or `~/.bash_profile`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### "Cannot connect to Ollama"

Start Ollama:

```bash
# Method 1: Launch the Ollama app from Applications

# Method 2: Run in terminal
ollama serve
```

Verify it's running:

```bash
curl http://localhost:11434/api/tags
```

### "Model not found"

Pull the model first:

```bash
ollama pull qwen2.5-coder:7b
```

### Permission Denied Errors

Make sure the flaco-premium command is executable:

```bash
chmod +x ~/.local/bin/flaco-premium
```

### Python Version Issues

If you have multiple Python versions, pipx might use the wrong one:

```bash
# Use specific Python version
python3.11 -m pip install --user pipx
python3.11 -m pipx install git+https://github.com/RouraIO/flaco-premium.git
```

---

## Updating Flaco

### Update from PyPI

```bash
pipx upgrade flaco-ai-premium
```

### Update from GitHub

```bash
pipx reinstall git+https://github.com/RouraIO/flaco-premium.git
```

---

## Uninstalling

```bash
# Uninstall Flaco
pipx uninstall flaco-ai-premium

# Remove config (optional)
rm -rf ~/.flaco
```

---

## Next Steps

1. **Read the Quick Start Guide**: [docs/QUICKSTART.md](../QUICKSTART.md)
2. **Create FLACO.md**: Initialize project context with `/init`
3. **Try Interactive Code Review**: Run `/review` with unlimited file selection
4. **Explore Specialized Agents**: Type `/help` to see all 10 agents
5. **Use Agent Swarms**: Let multiple agents collaborate on complex tasks

---

## Additional Resources

- **Main README**: [README.md](../../README.md)
- **Linux Installation**: [LINUX.md](LINUX.md)
- **Windows Installation**: [WINDOWS.md](WINDOWS.md)
- **Feature Comparison**: [FEATURE_COMPARISON.md](../../FEATURE_COMPARISON.md)
- **GitHub Issues**: [https://github.com/RouraIO/flaco.cli.premium/issues](https://github.com/RouraIO/flaco.cli.premium/issues)

---

**Made with ⚡ by [Roura.io](https://roura.io)**
