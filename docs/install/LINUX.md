# 🐧 Flaco AI PREMIUM Installation Guide for Linux

Complete installation guide for Flaco AI PREMIUM tier on Linux (Ubuntu, Debian, Fedora, Arch).

---

## Prerequisites

### Check Your Linux Distribution

```bash
cat /etc/os-release
```

This guide covers:
- Ubuntu 20.04+
- Debian 11+
- Fedora 35+
- Arch Linux

---

## Step 1: Install Python 3.9+

### Ubuntu / Debian

```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
```

### Fedora

```bash
# Install Python 3.11
sudo dnf install -y python3.11 python3-pip

# Verify installation
python3.11 --version
```

### Arch Linux

```bash
# Install Python
sudo pacman -S python python-pip

# Verify installation
python --version
```

---

## Step 2: Install Ollama

### Method 1: Official Install Script (Recommended)

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

This will:
- Download and install Ollama
- Set up systemd service
- Start Ollama automatically

### Method 2: Manual Installation

**Ubuntu / Debian:**

```bash
# Download Ollama
curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
chmod +x ollama

# Move to system path
sudo mv ollama /usr/local/bin/

# Create systemd service
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=$USER
Group=$USER
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF

# Start Ollama service
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Verify Ollama Installation

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Check service status
systemctl status ollama
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

### Ubuntu / Debian

```bash
sudo apt install -y pipx
pipx ensurepath
```

### Fedora

```bash
sudo dnf install -y pipx
pipx ensurepath
```

### Arch Linux

```bash
sudo pacman -S python-pipx
pipx ensurepath
```

### Manual Installation (if package not available)

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
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
# Install git if needed
sudo apt install -y git  # Ubuntu/Debian
sudo dnf install -y git  # Fedora
sudo pacman -S git       # Arch

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
# /home/yourusername/.local/bin/flaco-premium

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

### Ubuntu / Debian

```bash
sudo apt install -y ripgrep
```

### Fedora

```bash
sudo dnf install -y ripgrep
```

### Arch Linux

```bash
sudo pacman -S ripgrep
```

---

## Troubleshooting

### "command not found: flaco-premium"

The pipx binaries directory is not in your PATH. Fix it:

```bash
pipx ensurepath
```

Then close and reopen your terminal.

Or manually add to your shell config (`~/.bashrc` or `~/.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc  # or source ~/.zshrc
```

### "Cannot connect to Ollama"

Check if Ollama service is running:

```bash
systemctl status ollama
```

If not running, start it:

```bash
sudo systemctl start ollama
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

### Firewall Issues

If you're using a firewall, allow Ollama port:

```bash
# UFW (Ubuntu/Debian)
sudo ufw allow 11434

# firewalld (Fedora)
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

### Python Version Issues

If you have multiple Python versions, pipx might use the wrong one:

```bash
# Use specific Python version
python3.11 -m pip install --user pipx
python3.11 -m pipx install git+https://github.com/RouraIO/flaco.cli.premium.git
```

### SELinux Issues (Fedora/RHEL)

If you encounter SELinux errors:

```bash
# Temporarily disable SELinux (not recommended for production)
sudo setenforce 0

# Or create proper SELinux policy (recommended)
sudo ausearch -c 'ollama' --raw | audit2allow -M my-ollama
sudo semodule -X 300 -i my-ollama.pp
```

---

## Updating Flaco

### Update from PyPI

```bash
pipx upgrade flaco-ai-premium
```

### Update from GitHub

```bash
pipx reinstall git+https://github.com/RouraIO/flaco.cli.premium.git
```

---

## Uninstalling

```bash
# Uninstall Flaco
pipx uninstall flaco-ai-premium

# Stop and disable Ollama service
sudo systemctl stop ollama
sudo systemctl disable ollama

# Remove Ollama (optional)
sudo rm /usr/local/bin/ollama
sudo rm /etc/systemd/system/ollama.service

# Remove config (optional)
rm -rf ~/.flaco
rm -rf ~/.ollama
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
- **Mac Installation**: [MAC.md](MAC.md)
- **Windows Installation**: [WINDOWS.md](WINDOWS.md)
- **Feature Comparison**: [FEATURE_COMPARISON.md](../../FEATURE_COMPARISON.md)
- **GitHub Issues**: [https://github.com/RouraIO/flaco.cli.premium/issues](https://github.com/RouraIO/flaco.cli.premium/issues)

---

**Made with ⚡ by [Roura.io](https://roura.io)**
