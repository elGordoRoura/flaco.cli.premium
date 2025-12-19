# 👑 Flaco AI - Owner Setup Guide

**For: Product Owner/Developer**
**Private - Do not share with customers**

---

## 🎯 **Your Setup (Development)**

### 1. **Initial Setup**

```bash
cd /Users/roura.io/flaco.ai

# Activate virtual environment (Mac requirement)
source venv/bin/activate

# Install in development mode
pip install -e .

# Add global alias (one-time setup)
cat >> ~/.zshrc << 'EOF'

# Flaco shortcut - automatically activates venv and runs flaco
alias flaco='source /Users/roura.io/flaco.ai/venv/bin/activate && /Users/roura.io/flaco.ai/venv/bin/flaco'
EOF

# Reload configuration
source ~/.zshrc

# Test it works (from any directory now!)
flaco
```

**After setup:** Just type `flaco` from any directory - the alias handles venv activation automatically!

### 2. **Making Changes**

All source code is in:
```
flaco/                  # Main Python package
├── agents/            # Specialized agents
├── analytics/         # Contribution tracking
├── intelligence/      # Project scanning, swarm
├── projects/          # Project management
├── tools/             # File, git, bash tools
├── agent.py           # Main orchestrator
└── cli.py             # CLI interface

flaco-macos/           # Electron desktop app
```

After making changes:
```bash
# Test changes immediately (no reinstall needed)
flaco

# Commit changes
git add .
git commit -m "Your changes"
```

### 3. **Testing Before Release**

```bash
# Test CLI
flaco
/scan
/project create test
/git status

# Test Desktop App
cd flaco-macos
npm start
```

---

## 📦 **Creating Releases for Customers**

### Quick Release Process:

```bash
# 1. Update version in setup.py
# Edit: version="1.0.0" → version="1.1.0"

# 2. Create release package
./scripts/create_release.sh 1.1.0

# 3. Upload to GitHub
# Go to: github.com/your-repo/releases
# Create new release
# Upload: flaco-1.1.0.zip
```

### What Customers Get:
- Complete source code
- Installation script
- Desktop app
- Documentation
- Your license key system (optional)

---

## 💰 **Selling & Distribution**

### Option 1: Gumroad (Easiest)
1. Create product on gumroad.com
2. Set price ($29-$299)
3. Upload `flaco-1.0.0.zip`
4. Customers download after purchase

### Option 2: GitHub Releases
1. Create private repository
2. Add buyers as collaborators
3. They get access to releases

### Option 3: Your Own Website
1. Set up payment (Stripe/PayPal)
2. Send download link after purchase
3. Use license keys (optional)

---

## 🔒 **Protecting Your Work**

### Already Protected:
- ✅ Copyright notice in all files
- ✅ LICENSE file (proprietary)
- ✅ Trademark notice for "Flaco"

### Additional Protection:
1. **Don't share this repo publicly** (keep it private)
2. **Use license keys** (optional, for tracking)
3. **Monitor for piracy** (DMCA takedowns if needed)
4. **Trademark registration** (see LEGAL.md)

---

## 🛠️ **Maintenance**

### Updating Customer Licenses:
```bash
# 1. Make improvements
# 2. Test thoroughly
# 3. Create new release (1.1.0, 1.2.0, etc.)
# 4. Notify customers
# 5. They download new version
```

### Support Customers:
- Email support
- Discord community (optional)
- GitHub issues (if you want)
- Documentation updates

---

## 📊 **Track Sales & Usage**

### Simple Tracking:
- Count Gumroad sales
- Survey customers
- Track GitHub downloads

### Advanced Tracking (Optional):
- Add license key system
- Phone-home telemetry (ask permission!)
- Usage analytics

---

## 🚀 **Your Action Items**

### Before First Sale:
- [ ] Test everything on clean Mac
- [ ] Create first release (1.0.0)
- [ ] Set up Gumroad/payment
- [ ] Write sales page
- [ ] Register trademark (see LEGAL.md)
- [ ] Prepare demo video

### After First Sale:
- [ ] Send customer CUSTOMER_SETUP.md
- [ ] Provide support
- [ ] Gather feedback
- [ ] Plan updates

---

## 💡 **Tips for Success**

1. **Price It Right**: $49-$99 for individuals, $299+ for teams
2. **Offer Updates**: 1 year of free updates builds loyalty
3. **Build Community**: Discord/Slack for power users
4. **Create Content**: Blog posts, videos, tutorials
5. **Listen to Customers**: Their feedback = your roadmap

---

## 🔗 **Quick Links**

- Your code: `/Users/roura.io/flaco.ai`
- Releases: Create with `scripts/create_release.sh`
- Customer docs: `CUSTOMER_SETUP.md`
- Legal info: `LEGAL.md`

---

**You're ready to sell Flaco!** 💰🚀

*Keep this file private - only for you!*
