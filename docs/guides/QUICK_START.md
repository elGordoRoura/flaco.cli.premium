# 🚀 Flaco v2.0 - Quick Start Guide

**Updated**: December 8, 2024

---

## 🎯 Three Ways to Use Flaco

### 1️⃣ CLI (Terminal) - With Loading Animation

```bash
cd /Users/roura.io/flaco.ai
source venv/bin/activate
flaco

# Features:
# - Default model: qwen2.5-coder:32b
# - Loading animation: "🦙 Thinking..."
# - All Flaco tools available
```

### 2️⃣ Web Server (API)

```bash
cd /Users/roura.io/flaco.ai

# Run the helper script
./FlacoApp/run_server.sh

# Server starts at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### 3️⃣ Swift App (Frosted Glass UI)

**Step 1: Start the server first**
```bash
cd /Users/roura.io/flaco.ai
./FlacoApp/run_server.sh
```

**Step 2: Open in Xcode**
```bash
# Use the helper script
./FlacoApp/open_xcode.sh

# Or manually:
cd /Users/roura.io/flaco.ai/FlacoApp
xed .
```

**Step 3: Build and Run**
- In Xcode, select "FlacoApp" scheme
- Choose "My Mac" as destination
- Press `Cmd + R` to run

---

## ✨ What You'll See

### CLI
```
╔═══════════════════════════════════════╗
║                                       ║
║          🦙 FLACO AI                  ║
║                                       ║
║    Local AI Coding Assistant          ║
║    Powered by Ollama                  ║
║                                       ║
╚═══════════════════════════════════════╝

✅ Connected to Ollama - Model: qwen2.5-coder:32b

🦙 You: Hello
🦙 Thinking... [animated dots]
🤖 Flaco: [response]
```

### Swift App
- 🎨 Frosted glass interface
- ✨ Animated gradient background
- 💬 Real-time chat with WebSocket
- 🦙 "Thinking..." loading states
- 🎯 Beautiful modern design

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Make sure you're in the right directory
cd /Users/roura.io/flaco.ai

# Run the script
./FlacoApp/run_server.sh

# It will automatically:
# - Create venv if missing
# - Install dependencies
# - Start the server
```

### Xcode won't open
```bash
# Make sure Xcode is installed
xcode-select --install

# Use the helper script
cd /Users/roura.io/flaco.ai
./FlacoApp/open_xcode.sh
```

### "Virtual environment not found"
```bash
# The script will create it automatically
# Or create manually:
cd /Users/roura.io/flaco.ai
python3 -m venv venv
```

### Swift build errors
In Xcode:
1. Product → Clean Build Folder (`Cmd + Shift + K`)
2. Close and reopen Xcode
3. Try building again

---

## 📱 Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Status
curl http://localhost:8000/status

# Send message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Flaco!"}'
```

---

## 🎓 Tips

1. **Always start the server first** before running the Swift app
2. **Use the helper scripts** (`run_server.sh` and `open_xcode.sh`)
3. **Check Ollama is running** at http://192.168.20.3:11434
4. **Use xed .** to open SPM packages in modern Xcode versions

---

## 📚 Full Documentation

- **FlacoApp/README.md** - Complete Swift app guide
- **FLACO_V2_SUMMARY.md** - Technical details
- **README.md** - Main Flaco documentation

---

**Ready to go! 🚀**

*Run `./FlacoApp/run_server.sh` to start!*
