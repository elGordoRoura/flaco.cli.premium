# ⚡ Flaco AI PREMIUM

**Advanced Local AI Coding Assistant with 10 Specialized Agents**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/RouraIO/flaco.cli.premium/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org)
[![Tier](https://img.shields.io/badge/tier-PREMIUM-gold.svg)](https://flaco.ai/premium)

**100% Local. 100% Private. Supercharged with AI Agents.**

---

## 🎯 What is Flaco PREMIUM?

Flaco PREMIUM is the **advanced tier** of Flaco - a privacy-first AI coding assistant with **10 specialized AI agents**, multi-agent collaboration, and enterprise-grade features. All processing runs locally using Ollama.

### Why PREMIUM?

- **🤖 10 Specialized AI Agents**: Experts in networking, databases, frontend, security, and more
- **🔀 Agent Swarms**: Multi-agent collaboration on complex tasks
- **🔍 Interactive Code Review**: Unlimited file selection with batch processing
- **⚡ Advanced Workflows**: Git, project management, snippets, and more
- **🔒 Complete Privacy**: Still 100% local - no cloud, no tracking
- **💎 Enterprise Ready**: Built for professional teams and complex projects

---

## 🤖 Meet Your AI Team

PREMIUM includes **10 specialized AI agents**, each with unique expertise:

### 🌐 Tim - Networking Expert
**Expertise**: DNS, CDN, load balancing, networking protocols
- Optimize network architecture
- Debug connectivity issues
- Design scalable infrastructure

### 💾 Craig - Database Architect
**Expertise**: SQL, NoSQL, query optimization, database design
- Design efficient schemas
- Optimize complex queries
- Database migration strategies

### 🎨 Jony - Frontend Master
**Expertise**: React, Vue, Angular, design systems, UI/UX
- Build beautiful interfaces
- Implement design systems
- Optimize frontend performance

### ⚡ Phil - Hardware Engineer
**Expertise**: Performance optimization, hardware integration, systems programming
- Low-level optimizations
- Hardware-software integration
- Performance profiling

### 📈 Katie - Marketing Strategist
**Expertise**: Growth hacking, analytics, SEO, marketing automation
- Marketing strategy and campaigns
- Analytics and metrics
- SEO optimization

### ☁️ Jeff - DevOps Lead
**Expertise**: AWS, Docker, Kubernetes, CI/CD, infrastructure as code
- Cloud infrastructure setup
- CI/CD pipeline design
- Container orchestration

### 🔐 Bob - Security Expert
**Expertise**: Security auditing, compliance, penetration testing, cryptography
- Security assessments
- Compliance requirements
- Vulnerability analysis

### 💼 Lisa - Product Manager
**Expertise**: Product strategy, roadmaps, user research, feature prioritization
- Product strategy and vision
- Feature prioritization
- User research and feedback

### 🏗️ Eddie - Service Architect
**Expertise**: Microservices, APIs, event-driven architecture, cloud design
- Microservices architecture
- API design and implementation
- Distributed systems

### ⚡ Flaco AI - General Assistant
**Expertise**: General software engineering and problem-solving
- Code generation and refactoring
- Bug fixing and debugging
- General assistance

---

## 📦 PREMIUM vs FREE

| Feature | FREE Tier | PREMIUM Tier |
|---------|-----------|--------------|
| **Basic AI Assistant** | ✅ 1 general agent | ✅ 10 specialized agents |
| **Code Tools** (Read, Write, Edit, Glob, Grep) | ✅ | ✅ |
| **Context Loading** (FLACO.md) | ✅ | ✅ |
| **Model Management** | ✅ | ✅ |
| **Conversation History** | ✅ | ✅ |
| **Permissions System** | ✅ | ✅ |
| **Auto-update Notifications** | ✅ | ✅ |
| **Code Review** | ✅ Basic (10 files) | ✅ Interactive (unlimited) |
| **Agent Swarms** | ❌ | ✅ Multi-agent collaboration |
| **Git Operations** | ❌ | ✅ Full workflow |
| **Project Management** | ❌ | ✅ Multi-project support |
| **Code Snippets Library** | ❌ | ✅ 20+ snippets |
| **Todo Management** | ❌ | ✅ Task tracking |
| **Quick Actions** | ❌ | ✅ Multi-step workflows |
| **Custom Agents** | ❌ | ✅ Create your own |
| **Contribution Stats** | ❌ | ✅ Analytics |
| **Activity Recaps** | ❌ | ✅ Summaries |

---

## 🚀 Quick Start

### Prerequisites

1. **Ollama** (required)
   ```bash
   # Install from https://ollama.ai

   # Pull recommended model
   ollama pull qwen2.5-coder:7b
   ```

2. **Python 3.9+** (required)
   ```bash
   python --version  # Check your version
   ```

### Installation

**Option 1: Install from PyPI (Coming Soon)**
```bash
pipx install flaco-ai-premium
```

**Option 2: Install from GitHub**
```bash
# Using pipx (recommended)
pipx install git+https://github.com/RouraIO/flaco.cli.premium.git

# Or using pip
pip install git+https://github.com/RouraIO/flaco.cli.premium.git
```

**Option 3: Development Install**
```bash
git clone https://github.com/RouraIO/flaco.cli.premium.git
cd flaco.cli.premium
pipx install -e .
```

### First Run

```bash
# Run with either command
flaco-premium
# or
flacopro
```

The setup wizard will guide you through:
1. Ollama URL configuration (default: http://localhost:11434)
2. Model selection (recommended: qwen2.5-coder:7b)
3. Theme customization
4. Permission mode setup

---

## 📖 Usage

### Interactive Mode

```bash
$ flaco-premium

  ███████╗██╗      █████╗  ██████╗ ██████╗
  ██╔════╝██║     ██╔══██╗██╔════╝██╔═══██╗
  █████╗  ██║     ███████║██║     ██║   ██║
  ██╔══╝  ██║     ██╔══██║██║     ██║   ██║
  ██║     ███████╗██║  ██║╚██████╗╚██████╔╝
  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝

⚡ Advanced Local AI Coding Assistant
   Powered by Ollama
   PREMIUM TIER - All Features Unlocked

╭─────────────────────────── Session Info ───────────────────────────╮
│  📁 Working Dir:  /Users/you/projects/myapp                        │
│  📄 Context:      ✅ FLACO.md loaded                                │
│  🔗 Ollama:       ✅ Connected (http://localhost:11434)            │
│  🤖 Model:        qwen2.5-coder:7b                                 │
│  🔐 Permissions:  interactive                                      │
│  📦 Version:      v1.0.0 (PREMIUM)                                 │
│  👥 AI Team:      10 specialized agents ready                      │
╰────────────────────────────────────────────────────────────────────╯

Type your message or '/' for commands

> You: I need to design a scalable microservices architecture
[Eddie - Service Architect will be selected automatically]
```

### Specialized Agents in Action

Flaco PREMIUM automatically routes tasks to the right expert:

```bash
# Networking task → Tim
> You: Help me configure a CDN for my application

# Database task → Craig
> You: Optimize this SQL query for better performance

# Frontend task → Jony
> You: Create a React component with animations

# Security task → Bob
> You: Review this authentication code for vulnerabilities
```

### Agent Swarms

For complex tasks, multiple agents collaborate automatically:

```bash
> You: Build a complete user authentication system

🔀 Agent Swarm Detected!
Assembling team for this task:
  🔐 Bob (Security) - Auth strategy and security
  💾 Craig (Database) - User schema and sessions
  🎨 Jony (Frontend) - Login UI components
  ☁️ Jeff (DevOps) - Deployment and scaling

✅ Task decomposed into 4 sub-tasks
Starting collaborative execution...
```

---

## 💎 PREMIUM Features

### 🔍 Interactive Code Review

Select exactly which files to review, in any order:

```bash
> /review

📂 Found 50 Python file(s) in current directory

#    File                              Lines
1    __init__.py                         120
2    agent.py                            850
3    cli.py                              450
4    ollama_client.py                    300
5    specialized_agents.py               600
...

Select files to review [1-10]: 1-5,10,15-20

✅ Selected 14 file(s) (4,230 lines total)

🔍 Starting comprehensive code review...

[Detailed review with quality, security, performance analysis]

📂 36 file(s) remaining
Continue reviewing? [Y/n]:
```

### 📋 Code Snippets Library

20+ production-ready code patterns across multiple categories:

```bash
> /snippet

📋 Available Code Snippets (20+)
┌─────────────────────┬──────────┬────────────────────────────────┐
│ Name                │ Category │ Description                    │
├─────────────────────┼──────────┼────────────────────────────────┤
│ fastapi_endpoint    │ fastapi  │ FastAPI REST endpoint          │
│ async_retry         │ python   │ Async function with retry      │
│ react_component     │ react    │ React functional component     │
│ dockerfile_prod     │ docker   │ Production Dockerfile          │
│ pytest_fixture      │ testing  │ Pytest fixture with cleanup    │
│ microservice_base   │ arch     │ Microservice template          │
│ oauth_flow          │ auth     │ OAuth 2.0 flow                 │
│ redis_cache         │ cache    │ Redis caching pattern          │
│ ... 12 more         │          │                                │
└─────────────────────┴──────────┴────────────────────────────────┘

💡 Usage: /snippet <name> to insert
💡 Create custom: /snippet create
```

### 📁 Project Management

Manage multiple projects with context switching:

```bash
> /project list

📁 Your Projects
┌────┬─────────────────┬──────────┬─────────────────────┐
│ #  │ Name            │ Type     │ Last Active         │
├────┼─────────────────┼──────────┼─────────────────────┤
│ 1  │ ecommerce-api   │ FastAPI  │ 2 hours ago         │
│ 2  │ mobile-app      │ React    │ Yesterday           │
│ 3  │ ml-pipeline     │ Python   │ 3 days ago          │
└────┴─────────────────┴──────────┴─────────────────────┘

> /project switch mobile-app
✅ Switched to mobile-app
📄 Loaded project context
```

### ✅ Todo Management

Built-in task tracking with AI assistance:

```bash
> /todos

📋 Current Tasks
┌────┬─────────────────────────┬──────────┬──────────┐
│ #  │ Task                    │ Priority │ Status   │
├────┼─────────────────────────┼──────────┼──────────┤
│ 1  │ Fix authentication bug  │ High     │ In Progress│
│ 2  │ Add payment integration │ Medium   │ Pending  │
│ 3  │ Write API docs          │ Low      │ Pending  │
└────┴─────────────────────────┴──────────┴──────────┘

> /todos add Optimize database queries
✅ Added task #4
```

### ⚡ Quick Actions

Multi-step workflows with a single command:

```bash
> #Quick commit

🚀 Running: Quick commit
  ✓ git status
  ✓ git add .
  ✓ git commit -m 'Add user authentication'
  ✓ git push origin main
✅ Complete!

Available quick actions:
  #Quick commit      - Stage, commit, and push
  #Fresh start       - Clear context, start new
  #Code review       - Review recent changes
  #Test and build    - Run tests then build
  #Status check      - Full project overview
  #Project scan      - Deep analysis
  #Deploy            - Run deployment workflow
```

### 📊 Contribution Stats

Track your productivity:

```bash
> /stats week

📊 Contribution Statistics (This Week)

Commits:        42 commits
Lines Added:    +2,340 lines
Lines Deleted:  -856 lines
Files Changed:  87 files
Top Language:   Python (68%)

Productivity:
Monday:     ████████░ 8 commits
Tuesday:    ██████░░░ 6 commits
Wednesday:  ████████████ 12 commits
Thursday:   ██████████░ 10 commits
Friday:     ██████░░░ 6 commits

> /recap week
📝 This week you focused on authentication system refactoring,
   added OAuth integration, and improved test coverage from 45% to 78%.
```

### 🎨 Custom Agents

Create your own specialized agents:

```bash
> /agent create

Agent Name: Python Tester
Expertise: Python testing, pytest, mocking, TDD
Personality: Meticulous and thorough, focuses on edge cases
Thinking messages:
  - Analyzing test coverage
  - Designing test cases
  - Checking edge cases

✅ Agent created! Use with: @Python Tester
```

---

## 🛠️ All PREMIUM Commands

```bash
# Core Commands
/help                 # Show all commands
/status               # Current status
/exit                 # Exit Flaco

# Agent Management
/agent list           # List custom agents
/agent create         # Create new agent
/agent delete [name]  # Remove agent

# Code Review (Interactive)
/review               # Interactive file selection
                      # Unlimited files, batch processing

# Code Snippets
/snippet              # Browse snippets library
/snippet [name]       # Insert snippet
/snippet search [q]   # Search snippets
/snippet create       # Create custom snippet

# Git Operations
/git status           # Git status with insights
/git commit           # Interactive commit
/git push             # Push with validation
/git history          # Formatted git log
/git stats            # Commit statistics

# Project Management
/project list         # List all projects
/project switch [name]# Switch project
/project info         # Current project info
/project scan         # Deep project analysis

# Task Management
/todos                # Show all tasks
/todos add [task]     # Add new task
/todos complete [#]   # Mark complete
/todos delete [#]     # Remove task

# Quick Actions
#Quick commit         # Stage, commit, push
#Fresh start          # Reset context
#Code review          # Review changes
#Test and build       # Run test suite
#Status check         # Project overview
#Project scan         # Deep analysis

# Analytics
/stats [period]       # Contribution stats
                      # day/week/month/year
/recap [period]       # Activity summary

# Configuration
/model [name]         # Change model
/models               # List models
/permissions [mode]   # Change permissions
/setup                # Run setup wizard
/reset-config         # Reset configuration
```

---

## ⚙️ Configuration

### User Configuration

Configuration is stored in `~/.flaco/config.json`:

```json
{
  "ollama_url": "http://localhost:11434",
  "ollama_model": "qwen2.5-coder:7b",
  "theme_color": "cyan",
  "permission_mode": "interactive",
  "setup_completed": true,
  "tier": "premium"
}
```

### FLACO.md Context System

Create `FLACO.md` in your project root:

```markdown
---
project: E-Commerce Platform
version: 2.0.0
team: Backend Team
---

# Project Guidelines

## Architecture
- Microservices with event-driven communication
- Docker containers on Kubernetes
- PostgreSQL for transactional data
- Redis for caching and sessions

## Code Style
- Python: Black formatter, type hints required
- FastAPI for all new APIs
- Comprehensive error handling
- 80%+ test coverage mandatory

## CI/CD
- All PRs require code review
- Automated tests must pass
- Security scans on every commit
- Deploy to staging before production
```

Specialized agents will follow these guidelines automatically!

---

## 🔐 Security & Privacy

### Privacy Guarantees

- **100% Local Processing**: All AI runs on your local Ollama
- **No External APIs**: Zero network calls to cloud services
- **No Telemetry**: We don't track, collect, or transmit anything
- **Your Data Stays Yours**: Code never leaves your machine
- **GDPR/HIPAA Compliant**: By design

### Enterprise Security Features

- Multi-layer command validation
- Dangerous pattern detection
- Sensitive file protection
- Comprehensive secret redaction (15+ patterns)
- Granular permission system

---

## 🌟 Why Upgrade to PREMIUM?

### For Individual Developers

- **10x Productivity**: Specialized agents understand your domain
- **Better Code Quality**: Expert review and suggestions
- **Learn Faster**: Learn from specialized experts
- **Stay Organized**: Project and task management built-in

### For Teams

- **Consistent Standards**: Share FLACO.md configs across team
- **Knowledge Sharing**: Capture team expertise in custom agents
- **Better Collaboration**: Track contributions and activity
- **Faster Onboarding**: New developers get expert guidance

### For Enterprises

- **Complete Privacy**: Enterprise-grade local AI
- **Scalable**: Handle large, complex codebases
- **Auditable**: Full conversation and decision history
- **Customizable**: Build agents for your tech stack

---

## 📚 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[Mac Installation Guide](docs/install/MAC.md)** - macOS setup
- **[Linux Installation Guide](docs/install/LINUX.md)** - Linux setup
- **[Windows Installation Guide](docs/install/WINDOWS.md)** - Windows/WSL setup
- **[Agent Guide](docs/AGENTS.md)** - Using specialized agents
- **[Feature Comparison](FEATURE_COMPARISON.md)** - FREE vs PREMIUM
- **[Changelog](CHANGELOG.md)** - Release notes

---

## 🐛 Troubleshooting

### Cannot connect to Ollama

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve

# Verify config
cat ~/.flaco/config.json
```

### Agent not responding correctly

```bash
# Reset agent context
/reset

# Or switch to different agent
@Bob help me review this security code
```

---

## 💎 Pricing

**One-time purchase or subscription** (coming soon)

- Monthly: $19/month
- Annual: $190/year (save 17%)
- Lifetime: $399 (limited time)

**Current beta pricing**: FREE while in beta!

---

## 🤝 Contributing

We welcome contributions!

```bash
# Fork and clone
git clone https://github.com/YOUR-USERNAME/flaco.cli.premium.git
cd flaco.cli.premium

# Create feature branch
git checkout -b feature/amazing-feature

# Install in dev mode
pip install -e .

# Make changes and test
pytest

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/RouraIO/flaco.cli.premium/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RouraIO/flaco.cli.premium/discussions)
- **Website**: [https://flaco.ai/premium](https://flaco.ai/premium)
- **Email**: premium@flaco.ai

---

## 🙏 Acknowledgments

- Powered by [Ollama](https://ollama.ai)
- Built with [Rich](https://rich.readthedocs.io/) for terminal UI
- Inspired by modern AI coding assistants

---

**Made with ⚡ by [Roura.io](https://roura.io)**

*Flaco v1.0.0 PREMIUM - Your privacy-first AI coding team*
