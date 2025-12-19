# 🦙 Flaco AI - Customer Setup Guide

**Thank you for purchasing Flaco AI!**

Get up and running in **under 5 minutes**. ⚡

---

## 📋 **What You Need**

Before installing:
- ✅ **Mac** or Linux computer
- ✅ **Python 3.8+** ([Download](https://python.org))
- ✅ **Ollama** AI runtime ([Download](https://ollama.ai))

---

## 🚀 **Quick Install (3 Steps)**

### Step 1: Extract Files

```bash
# Unzip the download
unzip flaco-1.0.0.zip
cd flaco-1.0.0
```

### Step 2: Run Installer

```bash
# Run the installer
./scripts/install.sh

# Add global command (one-time setup)
cat >> ~/.zshrc << 'EOF'

# Flaco shortcut
alias flaco='source ~/flaco-1.0.0/venv/bin/activate && ~/flaco-1.0.0/venv/bin/flaco'
EOF

# Reload shell
source ~/.zshrc
```

**That's it!** ✨

### Step 3: Start Flaco

```bash
# Close and reopen terminal, then:
flaco
```

You can now run `flaco` from **anywhere**!

---

## 🎮 **First Time Usage**

Once Flaco starts, try these commands:

```bash
# See all features
/help

# Scan your project
/scan

# Create a project
/project create myapp

# Check git status
/git status

# View your stats
/stats week

# Get a weekly recap
/recap week
```

---

## 🖥️ **Desktop App (Optional)**

For the beautiful desktop interface:

```bash
cd flaco-macos
npm install
npm start
```

**Build standalone app:**
```bash
npm run build
```

This creates a `.dmg` installer you can keep!

---

## 💡 **Quick Start Examples**

### Example 1: Scan Your Project
```bash
flaco
/scan
```

### Example 2: Auto-Commit Changes
```bash
flaco
/git commit
```

### Example 3: Create a New Project
```bash
flaco
/project create my-awesome-app
```

---

## 🎯 **All Available Commands**

Once inside Flaco, type `/help` or try these:

**Project Management:**
- `/project list` - View all projects
- `/project create <name>` - Create new project
- `/project switch <name>` - Switch projects
- `/project info` - Project details

**Git Operations:**
- `/git status` - View git status
- `/git commit` - Smart auto-commit
- `/git push` - Push to remote
- `/git history` - Commit history

**Analytics:**
- `/scan` - Project intelligence
- `/stats [day|week|month|year]` - Statistics
- `/recap [day|week|month|year]` - Activity recap

**Other:**
- `/status` - System status
- `/model [name]` - Change AI model
- `/help` - Show all commands

---

## ⚙️ **Configuration**

### Change AI Model

```bash
# Inside Flaco
/model qwen2.5-coder:32b

# Or start with specific model
flaco -m llama3.1:latest
```

### Set Ollama URL (if not default)

```bash
flaco -u http://localhost:11434
```

---

## 🚨 **Troubleshooting**

### "Command not found: flaco"

```bash
# Reinstall
cd flaco-1.0.0
pip install -e .

# Or manually
python3 -m pip install -e .
```

### "Cannot connect to Ollama"

```bash
# Check Ollama is running
ollama list

# Pull a model if needed
ollama pull qwen2.5-coder:32b
```

### Desktop App Won't Start

```bash
cd flaco-macos
rm -rf node_modules package-lock.json
npm install
npm start
```

### Python Version Too Old

```bash
# Check version
python3 --version

# Need 3.8 or higher
# Download from: https://python.org
```

---

## 📚 **Features Overview**

### 🤖 **10 Specialized AI Agents**
- Each expert in different domains
- Automatic routing to best agent
- Funny names (Steve Jobsworth, Tim Cookiejar, etc.)

### 🌟 **Agent Swarm Mode**
- Multiple agents collaborate
- Activated for complex tasks
- Shows team composition

### 🧠 **Project Intelligence**
- Auto-scans your codebase
- Provides health score (0-100)
- Suggests improvements

### 📊 **GitHub-Style Contributions**
- Tracks all your activity
- Daily streaks
- Beautiful contribution graphs
- Weekly/monthly/yearly recaps

### 📁 **Project Management**
- Organize multiple projects
- Quick switching
- Project templates
- Import existing projects

### 🔄 **Smart Git Versioning**
- AI-generated commit messages
- Auto-commit and push
- Commit history
- Smart change detection

---

## 🎓 **Learn More**

Want to master Flaco? Check these out:

- **Full README** - In-depth documentation
- **Examples folder** - Sample projects
- **Community** - Join Discord (link in README)

---

## 💬 **Support**

Need help?

- **Email**: support@yourcompany.com
- **Discord**: [Your Discord Link]
- **GitHub Issues**: [If you offer this]

**Response time**: Within 24 hours

---

## 📜 **License & Terms**

- ✅ Licensed for **personal or commercial use**
- ✅ **One license per user** (team licenses available)
- ✅ **Source code included** for customization
- ✅ **1 year of free updates**
- ❌ **No redistribution** - see LICENSE file for details

---

## 🎉 **You're All Set!**

Start building amazing projects with Flaco:

```bash
flaco
```

**Enjoy your AI-powered coding assistant!** 🦙✨

---

*Flaco AI v1.0.0 - © 2024 All Rights Reserved*
*Protected by U.S. Copyright Law and Trade Secret Law*
