# Privacy Policy for Flaco AI

**Effective Date:** December 11, 2024
**Last Updated:** December 11, 2024

## Overview

Flaco AI is a desktop application that runs entirely on your local machine. We take your privacy seriously and have designed Flaco AI to minimize data collection and maximize user control.

**TL;DR:** We don't collect, store, or transmit your personal data. Your API keys, conversations, and settings never leave your computer unless you explicitly share them.

---

## What Flaco AI Does

Flaco AI is a desktop application that:
- Connects to AI providers (Anthropic, OpenAI, or local Ollama) using YOUR API keys
- Stores conversations, settings, and custom agents locally on your device
- Provides coding assistance through AI models

---

## Data Storage

### What is Stored Locally

All data is stored on YOUR computer in:
- **macOS:** `~/Library/Application Support/flaco-desktop/`
- **Windows:** `%APPDATA%\flaco-desktop\`
- **Linux:** `~/.config/flaco-desktop/`

**Stored data includes:**
1. **API Keys** - Encrypted using AES-256
2. **Conversations** - Your chat history with AI
3. **Custom Agents** - Agent descriptions you create
4. **Settings** - Your preferences and configuration
5. **Backups** - Automatic daily backups (last 7 days)

### Encryption

- API keys are encrypted at rest using `electron-store` with AES-256 encryption
- Encryption key is stored locally on your machine
- No master key, no cloud backup of your encryption key

### Data Access

- **Only you** have access to your data
- **Only Flaco AI** (running on your machine) can read your encrypted data
- We (the developers) **cannot** access your data

---

## Data Transmission

### What Gets Sent to AI Providers

When you use Flaco AI, your messages are sent to:

1. **Anthropic (if you choose Anthropic)**
   - Your conversation messages
   - Your API key (in request headers)
   - [Anthropic Privacy Policy](https://www.anthropic.com/legal/privacy)

2. **OpenAI (if you choose OpenAI)**
   - Your conversation messages
   - Your API key (in request headers)
   - [OpenAI Privacy Policy](https://openai.com/policies/privacy-policy)

3. **Local Ollama (if you choose local)**
   - Your conversation messages
   - Never leaves your computer
   - No external network requests

**Important:** Flaco AI does NOT intercept, log, or store what you send to AI providers. The communication is direct between your computer and the AI provider's API.

### What We Never Collect

- ❌ Your conversations
- ❌ Your API keys
- ❌ Your personal information
- ❌ Your IP address
- ❌ Your usage patterns
- ❌ Your custom agent descriptions
- ❌ Your file contents
- ❌ Any telemetry or analytics

---

## Auto-Updates

Flaco AI checks for updates by:
- Connecting to GitHub Releases (public repository)
- Checking version number of latest release
- Downloading updates if available

**What is sent:**
- HTTP request to `api.github.com` (public API)
- No personal data is transmitted
- GitHub may log your IP address (see [GitHub Privacy](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement))

**You can disable auto-updates** in Settings if you prefer manual updates.

---

## Third-Party Services

### AI Providers

When you use Flaco AI, you are subject to the privacy policies of your chosen AI provider:

- **Anthropic:** [Privacy Policy](https://www.anthropic.com/legal/privacy) | [Commercial Terms](https://www.anthropic.com/legal/commercial-terms)
- **OpenAI:** [Privacy Policy](https://openai.com/policies/privacy-policy) | [Terms of Use](https://openai.com/policies/terms-of-use)
- **Ollama:** Runs locally, no data leaves your computer

**Important:** These services may:
- Store your conversations for training (unless you opt out)
- Use your data to improve their models
- Have their own data retention policies

**Check each provider's privacy policy and opt-out options.**

### GitHub (for updates)

- Used only for checking and downloading updates
- Subject to [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement)
- You can disable auto-updates to avoid GitHub connections

---

## Data Retention

### On Your Computer

- **Conversations:** Kept until you delete them
- **Settings:** Kept until you reset them
- **Backups:** Last 7 days, then auto-deleted
- **Logs:** Kept for debugging, stored locally only

### Deleting Your Data

To completely remove all Flaco AI data:

**macOS:**
```bash
rm -rf ~/Library/Application\ Support/flaco-desktop/
```

**Windows:**
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\flaco-desktop"
```

**Linux:**
```bash
rm -rf ~/.config/flaco-desktop/
```

Or use Settings → Reset All Data (coming in v0.3.0).

---

## Children's Privacy

Flaco AI is not directed at children under 13. We do not knowingly collect data from children. If you are a parent and believe your child has used Flaco AI, please contact us to delete any data.

---

## Security

### How We Protect Your Data

1. **Encryption** - API keys encrypted with AES-256
2. **Local Storage** - No cloud sync, no remote servers
3. **Sandboxing** - Electron security features enabled
4. **Code Signing** - Verified builds (macOS signed, Windows in progress)
5. **Open Source** - Code is public for audit (coming soon)

### Your Responsibilities

1. **Protect your device** - Use a password, encrypt your disk
2. **Protect your API keys** - Don't share screenshots of Settings
3. **Keep Flaco AI updated** - Security patches via auto-update
4. **Verify downloads** - Only download from official sources

### Reporting Security Issues

Found a security vulnerability? Please email:
- **Security Email:** security@flaco.ai (coming soon)
- **GitHub:** Open a private security advisory

**Do not** post security vulnerabilities publicly.

---

## Changes to This Policy

We may update this Privacy Policy. Changes will be:
- Posted on GitHub
- Included in app updates
- Effective immediately upon update

**How to stay informed:**
- Check GitHub releases for policy updates
- Review PRIVACY_POLICY.md in your installation folder

---

## Your Rights

Depending on your location, you may have rights under:
- **GDPR (EU)** - Right to access, delete, port data
- **CCPA (California)** - Right to know what data is collected
- **Other laws** - Various regional privacy laws

**Good news:** Since Flaco AI doesn't collect your data, there's nothing for us to access, delete, or port. You have complete control of your local data.

---

## International Users

Flaco AI can be used worldwide. When you use third-party AI providers:
- Your data may be transmitted to their servers (US, EU, etc.)
- Subject to their privacy policies and data transfer rules
- Check your provider's policy for international data transfers

**Local Ollama users:** Data never leaves your computer, no international transfers.

---

## Business Use

If you use Flaco AI for business:
- Your organization's data policies apply
- You are responsible for API key management
- Consider your organization's data retention requirements
- Review AI provider business agreements

---

## Contact Us

Questions about this Privacy Policy?

- **Email:** support@flaco.ai (coming soon)
- **GitHub Issues:** [github.com/RouraIO/flaco.desktop/issues](https://github.com/RouraIO/flaco.desktop/issues)
- **Website:** (coming soon)

---

## Summary

**What we collect:** Nothing
**What we store:** Everything locally on your machine
**What we share:** Nothing
**Your control:** 100%

Flaco AI is designed for privacy. Your data stays on your computer, under your control, encrypted and secure.

---

**Last Updated:** December 11, 2024
**Version:** 1.0
