# 🦙 Flaco AI

> Your Personal AI Coding Team - A ChatGPT Alternative That Runs Locally

[![Version](https://img.shields.io/badge/version-0.0.10%20beta-blue.svg)](https://github.com/RouraIO/flaco.desktop/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)]()

---

## 🎯 Why Flaco AI Exists

**The Problem:** Developers are forced to choose between:
- **ChatGPT/Claude web apps** - Great UX, but limited customization, no privacy, subscription costs
- **Terminal AI tools** - Powerful but intimidating, command-line only, steep learning curve
- **VS Code extensions** - Locked into one editor, limited conversation history

**The Solution:** Flaco AI bridges the gap by offering:
- 🎨 **Beautiful desktop UI** - Like ChatGPT, but yours
- 🔒 **100% Local & Private** - All chats stay on your machine
- 🤖 **Custom AI Agents** - Create unlimited specialized assistants
- 🧠 **Local Models Only** - Runs through Ollama/LM Studio; no cloud API keys required
- 📁 **File Integration** - Import/export markdown files seamlessly
- ⚡ **Fast & Lightweight** - Native app, not a web wrapper

---

## 🆚 How Flaco Differs from Terminal AI

### vs Claude Code / Terminal AI Tools

| Feature | Terminal AI (claude-code, aider, etc.) | Flaco AI |
|---------|---------------------------------------|----------|
| **Interface** | Command-line only | Beautiful desktop UI |
| **Learning Curve** | Steep (need CLI knowledge) | Easy (point & click) |
| **Conversation History** | Limited/hard to browse | Full chat history, searchable |
| **Multiple Agents** | Single AI instance | Unlimited custom agents |
| **File Operations** | Complex commands | Drag & drop, file picker |
| **Accessibility** | Technical users only | Anyone can use |
| **Context Switching** | Terminal → Editor → Terminal | All in one place |

**Terminal AI is great when you:**
- Want direct code file manipulation
- Are comfortable with command-line
- Need git integration in terminal
- Want automated code changes

**Flaco AI is better when you:**
- Want a visual, intuitive interface
- Need to review/edit responses before applying
- Want organized conversation history
- Need custom specialized agents
- Want privacy without complexity

---

## 🌟 Key Features

### 🤖 **Custom AI Agents**
Create unlimited specialized agents for different tasks:
- 🐍 Python Expert - Data science & ML
- ⚛️ React Specialist - Frontend development
- 🗄️ Database Architect - SQL optimization
- 🔒 Security Analyst - Vulnerability assessment
- *...and any other specialty you need*

Each agent has its own:
- Custom emoji and name
- Specialized knowledge description
- Context for better responses

### 🔌 **Local Model Support**
Flaco Desktop now ships in **local-only** mode:
- Uses **Ollama/LM Studio** on your machine
- No cloud calls or third-party API keys
- Private by default, zero recurring API cost

### 📁 **File Operations**
- **Import** markdown files for context
- **Export** conversations as `.md` files
- Seamless integration with your docs/notes
- No more copy/paste hell

### 🔒 **Privacy First**
- All chats stored locally (encrypted)
- No cloud sync, no tracking, no analytics
- You control your data
- API keys never leave your machine

### 💰 **Cost Control**
- Use your own API keys
- Pay only for what you use
- Ollama support for $0 AI
- No monthly subscriptions

---

## 🚀 Getting Started

### Installation

1. **Download** the latest release:
   - [macOS (Apple Silicon)](https://github.com/RouraIO/flaco.desktop/releases/download/0.0.10/Flaco-AI-0.0.10-arm64.dmg)
   - Windows/Linux builds coming soon

2. **Open** the DMG and drag Flaco AI to Applications

3. **Launch** Flaco AI

### First-Time Setup (< 5 minutes)

1. **Start your local model runtime**
   - Install and run [Ollama](https://ollama.ai) or [LM Studio](https://lmstudio.ai)
   - Pull a model, e.g., `ollama pull llama3`

2. **Set your endpoint and model**
   - Endpoint defaults to `http://localhost:11434`
   - Click "Fetch Models" in setup, pick your pulled model

3. **Start Chatting!** 🎉

---

## 💡 Usage Examples

### Creating Custom Agents

```
1. Click the + button in the sidebar
2. Choose an emoji (e.g., 🐍)
3. Name your agent (e.g., "Alex - Python Expert")
4. Describe specialization:
   "Python expert specializing in data science,
    pandas, numpy, and machine learning workflows"
5. Click Create!
```

Now when you chat, select your custom agent for specialized responses.

### Importing Files

```
1. Click the 📁 import button
2. Select a .md file
3. File content appears in chat
4. Ask questions about it!
```

**Example:**
```
You: [Import architecture.md]
Flaco: I've received your architecture document. What would you like to know?
You: Can you identify potential security issues?
```

### Exporting Conversations

```
1. Click the 💾 export button
2. Choose save location
3. Entire conversation exported as markdown
4. Review/share later!
```

---

## 🔧 Configuration

### Switching AI Providers

1. Click ⚙️ Settings
2. Choose new provider
3. Enter API key
4. Click Save

### Managing Agents

- **Create:** Click + button
- **Select:** Click agent in sidebar
- **Delete:** Hover over agent, click ×

---

## 📊 Pricing

### Flaco AI (Free)
- ✅ Unlimited custom agents
- ✅ All features included
- ✅ No subscriptions
- ✅ MIT licensed

### AI Compute Costs
- **Local only** via Ollama/LM Studio
- No per-token API billing; performance depends on your hardware
| **OpenAI** | GPT-4 Turbo | ~$10/1M tokens (~$0.03-0.10/conversation) |
| **Ollama** | Any local model | **$0** (Runs on your machine) |

**Example:** 50 conversations/month with Claude ≈ $2-5/month

---

## 🛣️ Roadmap

### ✅ v0.0.10 (First Public Beta - Current)
- Custom AI agents with specialized knowledge
- Local-first architecture (Ollama/LM Studio support)
- Beautiful macOS-native UI with glass polish
- Chat management with rename, star, and search
- File import/export (markdown)
- Multiple agent management
- Theme-aware code blocks with syntax highlighting
- Inline chat rename and thinking indicator

### 🎯 v0.1.0 (Next Release)
- Auto-updates
- Enhanced chat history search
- Cost tracking dashboard
- More keyboard shortcuts
- Agent templates library

### 🔮 v1.0 (Planned)
- Code editor integration
- Terminal integration
- Windows/Linux support
- Context-aware agent selection
- Agent swarm collaboration

---

## 🤝 Contributing

Flaco AI is open source! Contributions welcome.

### Development Setup

```bash
git clone https://github.com/RouraIO/flaco.desktop
cd flaco.desktop/flaco-macos
npm install
npm start
```

### Building

```bash
npm run build
```

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

Built with:
- [Electron](https://www.electronjs.org/)
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-typescript)
- [OpenAI SDK](https://github.com/openai/openai-node)
- [Ollama](https://ollama.ai/)

---

## 🛠 Development

### Regenerating the App Icon

If you modify `assets/flaco-logo.svg`, regenerate the `.icns` file:

```bash
npm run package:icon
```

This runs `generate-icon.js` which:
1. Uses `sharp` to convert SVG to PNG files at all required sizes (16-1024px)
2. Uses macOS `iconutil` to create `assets/icon.icns`
3. Auto-cleans temporary files

### Building

```bash
npm install          # Install dependencies
npm run build        # Build and open DMG
npm run build:quiet  # Build without opening
```

---

## 💬 Support

- **Bug Reports:** [GitHub Issues](https://github.com/RouraIO/flaco.desktop/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/RouraIO/flaco.desktop/discussions)
- **Questions:** Join our community on [Discord](https://discord.gg/flaco-ai)

---

## ⚠️ Beta Notice

**This is v0.0.10 - First Public Beta**

Flaco AI is in active development. While we've built a solid foundation with custom agents, local AI support, and a polished macOS UI, you may encounter bugs or rough edges.

We'd love your feedback! Please report issues or suggest features on [GitHub Issues](https://github.com/RouraIO/flaco.desktop/issues).

---

## 🌟 Star History

If you like Flaco AI, give us a star! ⭐

---

Made with ❤️ by developers, for developers.
