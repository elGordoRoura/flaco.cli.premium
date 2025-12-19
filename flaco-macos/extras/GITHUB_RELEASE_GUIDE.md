# GitHub Release Guide - Flaco AI v0.0.1

## 📦 Build Complete!

Your v0.0.1 release is ready in the `dist` folder:

```
dist/
├── Flaco AI-0.0.1-arm64.dmg          ← macOS Apple Silicon
├── Flaco AI-0.0.1-arm64-mac.zip      ← Alternative format
└── mac-arm64/
    └── Flaco AI.app                   ← The app itself
```

---

## 🚀 Publishing to GitHub

### Step 1: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `flaco-desktop` (or your choice)
3. Description: "Your Personal AI Coding Team - ChatGPT Alternative That Runs Locally"
4. Choose: **Public** (for sharing with friends)
5. **Don't** initialize with README (we have one)
6. Click **Create repository**

---

### Step 2: Push Code to GitHub

```bash
cd /Users/roura.io/flaco.ai/flaco-macos

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Flaco AI v0.0.1

Features:
- Custom AI agents
- Multi-provider support (Anthropic, OpenAI, Ollama)
- File import/export
- Beautiful desktop UI
- Privacy-first design"

# Add your GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/flaco-desktop.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

### Step 3: Create GitHub Release

#### Option A: Via GitHub Website (Easier)

1. Go to your repo: `https://github.com/YOUR_USERNAME/flaco-desktop`
2. Click **Releases** (right sidebar)
3. Click **Create a new release**
4. Fill in:

   **Tag:** `0.0.1` (no "v" prefix as requested)

   **Release title:** `Flaco AI 0.0.1 - Beta Release`

   **Description:** (Copy from below)

```markdown
# 🦙 Flaco AI v0.0.1 - Beta Release

> Your Personal AI Coding Team - ChatGPT Alternative That Runs Locally

## 🎉 First Beta Release!

This is the initial beta of Flaco AI! 🎊

### ✨ What's Included

- 🤖 **Custom AI Agents** - Create unlimited specialized assistants
- 🔌 **Multi-Provider** - Use Anthropic Claude, OpenAI GPT, or Ollama (local/free)
- 📁 **File Operations** - Import/export markdown files
- 🔒 **Privacy First** - Everything stored locally, encrypted
- 🎨 **Beautiful UI** - Modern desktop app experience

### 📥 Installation

1. Download the DMG below (choose your Mac type)
2. Open and drag to Applications
3. Launch Flaco AI
4. Complete 5-minute setup
5. Start chatting!

### 🎯 Perfect For

- Developers who want privacy
- Teams who can't use cloud AI
- Anyone wanting specialized AI agents
- People exploring local AI (Ollama)

### ⚠️ Beta Notice

This is beta software. Expect bugs! Feedback welcome.

- ✅ Core features work great
- ⚠️ Some polish needed
- 🚧 More features coming in v0.1.0

### 📊 What's Next (v0.1.0)

- Auto-updates
- Chat history persistence
- Cost tracking
- Keyboard shortcuts

### 🐛 Known Issues

- Default Electron icon (custom icon coming)
- No auto-updates yet (manual install for now)
- Chat history doesn't persist between sessions

### 💬 Feedback

Found a bug? Have an idea? Open an issue!

---

**Full Changelog**: First release 🎉
```

5. **Upload binaries:**
   - Click "Attach binaries"
   - Drag these files from `dist` folder:
     - `Flaco AI-0.0.1-arm64.dmg`
     - `Flaco AI-0.0.1-arm64-mac.zip`

6. Check **"Set as a pre-release"** (it's beta)
7. Click **Publish release**

#### Option B: Via Command Line (gh CLI)

```bash
# Install gh if needed: brew install gh

# Login to GitHub
gh auth login

# Create release with files
gh release create 0.0.1 \
  "./dist/Flaco AI-0.0.1-arm64.dmg" \
  "./dist/Flaco AI-0.0.1-arm64-mac.zip" \
  --title "Flaco AI 0.0.1 - Beta Release" \
  --notes-file CHANGELOG.md \
  --prerelease
```

---

## 📧 Sharing with Friends

Once published, your release will be at:
```
https://github.com/YOUR_USERNAME/flaco-desktop/releases/tag/0.0.1
```

### Share Link

Send this message to your friends:

```
Hey! 👋

I just released the first beta of Flaco AI - a ChatGPT alternative
that runs on your Mac with custom AI agents!

Features:
- Create your own specialized AI agents
- Use Claude, GPT, or free local AI (Ollama)
- 100% private - everything stays on your machine
- Import/export markdown files

Download (macOS only for now):
https://github.com/YOUR_USERNAME/flaco-desktop/releases/tag/0.0.1

It's free and open source! Would love your feedback.

Setup takes 5 minutes - just need an API key from Anthropic or OpenAI.
Or use Ollama for completely free local AI.

Let me know what you think! 🚀
```

---

## 📱 Social Media Posts

### Twitter/X
```
🦙 Launching Flaco AI v0.0.1 - A ChatGPT alternative that runs locally on your Mac!

✨ Create custom AI agents
🔒 100% private & local
🆓 Use free local AI (Ollama)

Beta out now! https://github.com/YOUR_USERNAME/flaco-desktop

#AI #Developer #Privacy #OpenSource
```

### LinkedIn
```
🚀 Excited to share Flaco AI v0.0.1 - the first beta of my AI coding assistant!

Unlike ChatGPT, Flaco:
• Runs locally on your Mac (privacy-first)
• Lets you create unlimited custom AI agents
• Works with Claude, GPT, or free local models
• No subscriptions - use your own API keys

Built for developers who want:
✅ Privacy and data control
✅ Specialized AI agents for different tasks
✅ Beautiful UI without terminal complexity

Try the beta: [link]
Feedback welcome!

#ArtificialIntelligence #Developer #Privacy #OpenSource
```

---

## 🔐 Optional: Code Signing Notes

Your app is already code signed! ✅

For full Mac App Store distribution later, you'll need:
- Apple Developer account ($99/year)
- Notarization (for Gatekeeper)
- App Store submission

For now, direct distribution via GitHub releases is perfect for beta testing.

---

## 📊 Tracking Downloads

GitHub shows download counts on your release page!

Check: `https://github.com/YOUR_USERNAME/flaco-desktop/releases`

---

## 🎯 Next Steps

After friends test v0.0.1:

1. **Collect feedback** - Create GitHub issues for bugs
2. **Iterate** - Fix critical issues
3. **v0.1.0** - Add auto-updates, chat history
4. **Promote** - Share more widely
5. **v1.0** - Full public launch!

---

## 💡 Tips

### Getting More Testers

- Post on Reddit: r/MacOS, r/LocalLLaMA, r/programming
- Share on Hacker News: news.ycombinator.com
- Tweet with relevant hashtags
- Share in Discord communities

### Managing Feedback

- Create issue templates on GitHub
- Use GitHub Discussions for feature requests
- Set up a simple feedback form

### Building Trust

- Keep README updated
- Respond to issues quickly
- Be transparent about limitations
- Share your roadmap

---

**You're ready to launch! 🚀**

Good luck with your beta! Let your friends know about it!
