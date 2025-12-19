# 🪟 Flaco AI PREMIUM Installation Guide for Windows

Complete installation guide for Flaco AI PREMIUM tier on Windows 10/11 using WSL2 (Windows Subsystem for Linux).

**Note**: Flaco AI runs natively on Linux/macOS. For Windows, we use WSL2 which provides a full Linux environment.

---

## Why WSL2?

- **Native Linux Experience**: Run Flaco exactly as intended
- **Better Performance**: Direct access to system resources
- **Full Compatibility**: All features work without workarounds
- **Easy Setup**: Microsoft makes WSL2 installation simple

---

## Prerequisites

- **Windows 10** version 2004+ (Build 19041+) or **Windows 11**
- **Administrator access** to install WSL2
- **At least 8GB RAM** (16GB recommended for larger models)
- **20GB free disk space**

---

## Step 1: Install WSL2

### Quick Installation (Windows 11 or Windows 10 version 2004+)

Open **PowerShell** or **Command Prompt** as Administrator and run:

```powershell
wsl --install
```

This command will:
- Enable WSL and Virtual Machine Platform
- Download and install Ubuntu (default Linux distribution)
- Set WSL2 as the default version

**Restart your computer** after installation.

### Manual Installation (if quick install doesn't work)

1. **Enable WSL**:
   ```powershell
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   ```

2. **Enable Virtual Machine Platform**:
   ```powershell
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

3. **Restart your computer**

4. **Download and install the WSL2 Linux kernel update**:
   - Visit: https://aka.ms/wsl2kernel
   - Download and run the installer

5. **Set WSL2 as default**:
   ```powershell
   wsl --set-default-version 2
   ```

6. **Install Ubuntu from Microsoft Store**:
   - Open Microsoft Store
   - Search for "Ubuntu 22.04 LTS"
   - Click "Get" to install

---

## Step 2: Set Up Ubuntu

### First Launch

1. Launch "Ubuntu" from the Start menu
2. Wait for installation to complete (1-2 minutes)
3. Create your Linux username and password

```
Installing, this may take a few minutes...
Enter new UNIX username: yourname
New password:
Retype new password:
```

### Update Ubuntu

```bash
sudo apt update && sudo apt upgrade -y
```

---

## Step 3: Install Python 3.9+

Ubuntu 22.04 comes with Python 3.10, but let's ensure we have everything:

```bash
# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
# Should show: Python 3.10.x or higher
```

---

## Step 4: Install Ollama

### Install Ollama in WSL

```bash
# Run the official install script
curl -fsSL https://ollama.ai/install.sh | sh
```

### Start Ollama Service

```bash
# Start Ollama
ollama serve &

# Wait a few seconds, then verify it's running
curl http://localhost:11434/api/tags
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

## Step 5: Install pipx

```bash
# Install pipx
sudo apt install -y pipx

# Add pipx to PATH
pipx ensurepath

# Reload shell configuration
source ~/.bashrc
```

Verify installation:

```bash
pipx --version
```

---

## Step 6: Install Flaco AI

### Option 1: Install from PyPI (Coming Soon)

```bash
pipx install flaco-ai-premium
```

### Option 2: Install from GitHub (Current Method)

```bash
# Install git first
sudo apt install -y git

# Install Flaco
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

## Step 7: Verify Installation

```bash
# Check if flaco-premium is installed
which flaco-premium

# Should show something like:
# /home/yourusername/.local/bin/flaco-premium

# Check version
flaco-premium --version
```

---

## Step 8: First Run

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
sudo apt install -y ripgrep
```

---

## Working with Windows Files

### Access Windows Files from WSL

Your Windows drives are mounted under `/mnt/`:

```bash
# Navigate to C:\Users\YourName\Documents
cd /mnt/c/Users/YourName/Documents

# Or use the Windows path directly
cd "$(wslpath 'C:\Users\YourName\Documents')"
```

### Access WSL Files from Windows

In File Explorer, type:
```
\\wsl$\Ubuntu\home\yourname
```

Or use Windows Terminal to directly access WSL files.

---

## Tips for Better Experience

### 1. Use Windows Terminal

Download from Microsoft Store for a better terminal experience:
- Multiple tabs
- Split panes
- Better fonts and colors

### 2. Install VS Code Remote - WSL Extension

If you use VS Code:
1. Install "Remote - WSL" extension
2. Open WSL from VS Code: `code .`
3. Full VS Code experience with WSL backend

### 3. Auto-start Ollama

Add to your `~/.bashrc`:

```bash
# Auto-start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    ollama serve > /dev/null 2>&1 &
fi
```

---

## Troubleshooting

### "command not found: flaco-premium"

The pipx binaries directory is not in your PATH. Fix it:

```bash
pipx ensurepath
source ~/.bashrc
```

### "Cannot connect to Ollama"

Start Ollama manually:

```bash
ollama serve &
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

### WSL2 Not Starting

```powershell
# In PowerShell as Administrator
wsl --shutdown
wsl
```

### Slow Performance

1. **Allocate more resources to WSL2**

   Create or edit `C:\Users\YourName\.wslconfig`:

   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

2. **Restart WSL**:
   ```powershell
   wsl --shutdown
   wsl
   ```

### Windows Defender Slowing Things Down

Add WSL2 processes to Windows Defender exclusions:
1. Open Windows Security
2. Virus & threat protection settings
3. Add exclusions
4. Add: `%USERPROFILE%\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu*`

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

# Remove config (optional)
rm -rf ~/.flaco

# To completely remove WSL (optional)
# In PowerShell as Administrator:
# wsl --unregister Ubuntu
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
- **Linux Installation**: [LINUX.md](LINUX.md)
- **Feature Comparison**: [FEATURE_COMPARISON.md](../../FEATURE_COMPARISON.md)
- **WSL Documentation**: [https://docs.microsoft.com/en-us/windows/wsl/](https://docs.microsoft.com/en-us/windows/wsl/)
- **GitHub Issues**: [https://github.com/RouraIO/flaco.cli.premium/issues](https://github.com/RouraIO/flaco.cli.premium/issues)

---

**Made with ⚡ by [Roura.io](https://roura.io)**
