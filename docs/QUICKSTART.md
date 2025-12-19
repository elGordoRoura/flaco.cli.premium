# ⚡ Flaco AI PREMIUM - 5 Minute Quick Start

Get started with Flaco AI PREMIUM and all 10 specialized agents in 5 minutes or less!

---

## Prerequisites Checklist

Before starting, make sure you have:

- [ ] **macOS 10.15+**, **Linux**, or **Windows 10/11** with WSL2
- [ ] **Python 3.9 or later** (`python3 --version`)
- [ ] **10+ GB free disk space** (for Ollama model)
- [ ] **8+ GB RAM** (16GB recommended for agent swarms)

---

## Step 1: Install Ollama (2 minutes)

### macOS

```bash
# Download from https://ollama.ai and drag to Applications
# OR use Homebrew:
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

```bash
# First install WSL2 (if not already):
wsl --install

# Then in Ubuntu terminal:
curl -fsSL https://ollama.ai/install.sh | sh
```

### Pull a Model

```bash
# Pull recommended model (4.7GB - takes 2-5 minutes depending on connection)
ollama pull qwen2.5-coder:7b

# For better swarm performance, consider the 32B model (18GB)
# ollama pull qwen2.5-coder:32b

# Verify it's running
curl http://localhost:11434/api/tags
```

---

## Step 2: Install Flaco AI PREMIUM (1 minute)

### Install pipx (if not installed)

**macOS:**
```bash
brew install pipx
pipx ensurepath
```

**Linux:**
```bash
sudo apt install pipx  # Ubuntu/Debian
sudo dnf install pipx  # Fedora
pipx ensurepath
```

**Windows (WSL):**
```bash
sudo apt install pipx
pipx ensurepath
```

Close and reopen your terminal after running `pipx ensurepath`.

### Install Flaco AI PREMIUM

```bash
# From PyPI (coming soon)
pipx install flaco-ai-premium

# OR from GitHub (current)
pipx install git+https://github.com/RouraIO/flaco.cli.premium.git
```

---

## Step 3: First Run (2 minutes)

Launch Flaco (use either command):

```bash
flaco-premium
# or
flacopro
```

You'll see a setup wizard:

```
👋 Welcome to Flaco PREMIUM!

? Ollama URL: [http://localhost:11434]
→ Press Enter to accept default

? Model: [qwen2.5-coder:7b]
→ Press Enter to select

? Theme color:
  cyan
  green
  blue
  magenta
→ Choose your preference

? Permission mode:
  interactive  (asks before operations)
  auto         (auto-approves all)
  headless     (denies all operations)
→ Choose "interactive" (recommended)

✅ Setup complete! Your AI team is ready!

👥 10 Specialized Agents Available:
   🌐 Tim (Networking)
   💾 Craig (Database)
   🎨 Jony (Frontend)
   ⚡ Phil (Hardware)
   📈 Katie (Marketing)
   ☁️ Jeff (DevOps)
   🔐 Bob (Security)
   💼 Lisa (Product)
   🏗️ Eddie (Services)
   ⚡ Flaco AI (General)
```

---

## Step 4: Try Premium Features!

### Meet Your AI Team

```bash
> You: I need to optimize database queries

[🔀 Craig - Database Architect activates automatically]

Craig: I'd be happy to help optimize your database queries...
```

### Agent Swarms

```bash
> You: Build a user authentication system

[🔀 Agent Swarm Detected!]
Assembling team:
  🔐 Bob (Security) - Auth strategy
  💾 Craig (Database) - User schema
  🎨 Jony (Frontend) - Login UI
  ☁️ Jeff (DevOps) - Deployment

[Agents collaborate automatically...]
```

### Interactive Code Review

```bash
> /review

📂 Found 50 Python file(s)

#    File                              Lines
1    __init__.py                         120
2    agent.py                            850
3    cli.py                              450
...

Select files to review [1-10]: 1-10,15,20-25

✅ Selected 16 file(s) (5,230 lines total)

[Comprehensive review with all files...]

📂 34 file(s) remaining
Continue reviewing? [Y/n]:
```

### Code Snippets

```bash
> /snippet

📋 Available Code Snippets (20+)
[Shows all production-ready snippets]

> /snippet fastapi_endpoint

[Generates FastAPI code...]

> /snippet create

[Create your own custom snippet...]
```

### Git Workflow

```bash
> /git status

[Shows enhanced git status with insights]

> /git commit

[Interactive commit with AI-assisted message]

> /stats week

[Shows your contribution statistics]
```

### Project Management

```bash
> /project list

[Shows all your projects]

> /project switch my-app

[Switches context to my-app project]
```

---

## Essential Commands

### Core Commands
```bash
/help              # Show all commands
/status            # Current status and active project
/exit              # Exit Flaco
```

### Agent Management
```bash
/agent list        # List custom agents
/agent create      # Create new specialized agent
```

### Code Review
```bash
/review            # Interactive file selection, unlimited files
```

### Code Snippets
```bash
/snippet           # Browse snippets library
/snippet [name]    # Insert specific snippet
/snippet create    # Create custom snippet
```

### Git Operations
```bash
/git status        # Enhanced git status
/git commit        # Interactive commit
/git push          # Push with validation
/git stats         # Commit statistics
```

### Project Management
```bash
/project list      # List all projects
/project switch    # Switch project
/project info      # Current project info
```

### Task Management
```bash
/todos             # Show all tasks
/todos add [task]  # Add new task
/todos complete #  # Mark task complete
```

### Quick Actions
```bash
#Quick commit      # Stage, commit, push
#Code review       # Review recent changes
#Status check      # Full project overview
```

### Analytics
```bash
/stats [period]    # Contribution stats (day/week/month/year)
/recap [period]    # Activity summary
```

---

## Quick Tips

### 1. Create Project Context

Initialize FLACO.md in your project:

```bash
> /init
```

The specialized agents will follow your project guidelines automatically!

### 2. Use Specific Agents

```bash
# Let the system choose automatically
> You: Review this security code

# Or specify an agent
> @Bob review this authentication logic
```

### 3. Leverage Agent Swarms

For complex, multi-domain tasks, agents will automatically collaborate:

```bash
# This triggers a swarm:
> You: Build a complete e-commerce checkout system

[Multiple agents work together]
```

### 4. Manage Multiple Projects

```bash
# Add projects
> /project add frontend ~/projects/react-app
> /project add backend ~/projects/api

# Switch between them
> /project switch frontend

[Context automatically loads for frontend project]
```

---

## Troubleshooting

### "Cannot connect to Ollama"

```bash
# Start Ollama
ollama serve &

# Or on Mac, launch Ollama app from Applications
```

### "command not found: flaco-premium"

```bash
# Re-run pipx ensurepath
pipx ensurepath

# Close and reopen terminal
# OR manually add to PATH:
export PATH="$HOME/.local/bin:$PATH"
```

### "Model not found"

```bash
# Pull the model
ollama pull qwen2.5-coder:7b

# List installed models
ollama list
```

### Agent Swarms are slow

```bash
# Use a smaller model for speed
> /model qwen2.5-coder:7b

# Or use larger model for better quality
> /model qwen2.5-coder:32b
```

---

## Next Steps

Now that you're up and running:

1. **Read the full README**: [README.md](../README.md)
2. **Try Interactive Code Review**: Navigate to your project and run `/review`
3. **Create Custom Agent**: Use `/agent create` to build an agent for your domain
4. **Set Up Projects**: Use `/project add` for your repositories
5. **Explore Agent Swarms**: Try complex multi-domain tasks
6. **OS-Specific Guides**:
   - [Mac Installation](install/MAC.md)
   - [Linux Installation](install/LINUX.md)
   - [Windows Installation](install/WINDOWS.md)

---

## Learn More

- **Agent Guide**: [docs/AGENTS.md](AGENTS.md) - Deep dive into each agent
- **Feature Comparison**: [FEATURE_COMPARISON.md](../FEATURE_COMPARISON.md)
- **Social Share**: [docs/SOCIAL_SHARE.md](SOCIAL_SHARE.md) - Share Flaco with others

---

## Get Help

- **GitHub Issues**: [https://github.com/RouraIO/flaco.cli.premium/issues](https://github.com/RouraIO/flaco.cli.premium/issues)
- **Discussions**: [https://github.com/RouraIO/flaco.cli.premium/discussions](https://github.com/RouraIO/flaco.cli.premium/discussions)
- **Email**: premium@flaco.ai

---

**Happy coding with your AI team!** ⚡

*Made by [Roura.io](https://roura.io)*
