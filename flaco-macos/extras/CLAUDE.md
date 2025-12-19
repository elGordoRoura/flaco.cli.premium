# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flaco AI is an Electron-based desktop application that provides a ChatGPT-like interface for local AI models (Ollama/LM Studio). It features custom AI agents, chat management, and a polished macOS-native UI.

**Current Version:** 0.0.10 (First Public Beta)
**Platform:** macOS (Apple Silicon) - Windows/Linux planned for v1.0
**Tech Stack:** Electron, vanilla JavaScript, electron-store for persistence

## Development Commands

### Running the App
```bash
npm start              # Launch Electron app
npm run dev           # Launch with developer logging enabled
```

### Building
```bash
npm run build         # Build DMG and auto-open it
npm run build:quiet   # Build DMG without opening
npm run build:mac     # Build for macOS only
npm run build:win     # Build for Windows (NSIS + ZIP)
npm run build:linux   # Build for Linux (AppImage, deb, rpm)
npm run build:all     # Build for all platforms
```

Build artifacts are output to `/distro/` directory. The naming convention is: `Flaco-AI-${version}-${arch}.${ext}`

### Testing
```bash
npm test              # Run all tests (settings + chat-manager)
npm run test:settings # Run only settings tests
npm run test:chat     # Run only chat manager tests
```

Tests use a simple assertion-based approach with mocked Electron APIs. Run individual test files directly:
```bash
node tests/settings.test.js
node tests/chat-manager.test.js
```

### Icon Generation
```bash
npm run package:icon  # Regenerate app icon from SVG
```

This converts `assets/flaco-logo.svg` to PNG files at all required sizes (16-1024px), then uses macOS `iconutil` to create `assets/icon.icns`. Only works on macOS.

## Architecture

### Electron Process Architecture

**Main Process (`main.js`):**
- Manages BrowserWindow lifecycle
- Hosts IPC handlers for all renderer requests
- Initializes managers: Settings, ChatManager, BackupManager, ConversationManager, AgentContextBuilder
- Handles auto-updates via electron-updater
- Error handling via ErrorHandler class

**Renderer Process (`renderer.js`):**
- Vanilla JavaScript UI logic
- Communicates with main process via `window.flaco` bridge (exposed by preload.js)
- All UI state management and DOM manipulation
- Markdown rendering via marked.js, code highlighting via highlight.js

**Preload Script (`preload.js`):**
- Exposes secure IPC API to renderer via `contextBridge`
- Creates `window.flaco` namespace with typed methods for settings, chats, agents, files, backups
- This is the ONLY way renderer can communicate with main process

### Data Persistence Layer

All data is stored using `electron-store` with encryption:

**Settings (`settings.js`):**
- Stores: AI provider, model selection, custom agents, first-run flag, local endpoint
- Uses encrypted electron-store at `${basePath}/config.json`
- Encryption key stored at `${basePath}/encryption.key` (or migrated from legacy key)
- basePath: `~/Library/Application Support/flaco-desktop` (macOS)

**Chat Manager (`chat-manager.js`):**
- Stores all chats and messages in encrypted `${basePath}/chats.json`
- Each chat has: id, name, messages[], createdAt, updatedAt, starred (optional)
- Messages have: id, role (user/assistant), content, timestamp
- Maintains `currentChatId` pointer for active chat

**Backup Manager (`backup-manager.js`):**
- Creates timestamped backups of entire data directory
- Backups stored in `${basePath}/backups/`
- Includes: config.json, chats.json, encryption.key
- Backup format: `backup-YYYY-MM-DD-HH-mm-ss/`

### UI Component Communication Pattern

**Inline Event Handlers Requirement:**
Since UI is generated via template literals, event handlers must be globally accessible:
```javascript
// ❌ Wrong - won't work from onclick attributes
function doSomething() { ... }

// ✅ Correct - accessible from inline onclick
window.doSomething = function() { ... }
```

This pattern is used for: `startChatRename`, `toggleChatStar`, `switchToChat`, `deleteChat`, `selectAgent`, `deleteAgent`

### IPC Communication Patterns

All renderer-to-main communication follows this pattern:

1. **Renderer calls:** `window.flaco.chats.create('New Chat')`
2. **Preload invokes:** `ipcRenderer.invoke('chats:create', 'New Chat')`
3. **Main handles:** `ipcMain.handle('chats:create', async (event, name) => { ... })`
4. **Main returns:** `{ success: true, chat: {...} }` or error object
5. **Renderer receives** promise result

IPC namespaces:
- `ai:*` - AI message sending
- `settings:*` - App settings
- `models:*` - Model fetching (Ollama)
- `agents:*` - Custom agent CRUD
- `chats:*` - Chat and message management
- `file:*` - Import/export operations
- `context:*` - flaco.md context
- `logs:*` - Log folder access
- `backup:*` - Backup/restore operations

## Key Design Patterns

### Agent System
Custom agents are stored in settings as:
```javascript
{
  id: string,           // Unique ID
  emoji: string,        // Display emoji (e.g., "🐍")
  name: string,         // Agent name
  description: string   // Specialization (markdown supported)
}
```

The current agent's description is prepended to AI requests via `AgentContextBuilder.buildSystemPrompt()`.

### Chat Message Flow
1. User types message → `sendMessage()` in renderer.js
2. Renderer calls `window.flaco.sendMessage(message)`
3. Main process receives IPC → `ai:send-message` handler
4. AgentContextBuilder builds system prompt from current agent
5. ConversationManager retrieves message history
6. AI provider called (local/Ollama by default)
7. Response streamed back to renderer
8. ChatManager persists messages to encrypted store

### Theme System
Flaco uses CSS custom properties for theming. Both dark and light modes are supported via media queries:
```css
@media (prefers-color-scheme: light) {
  /* Light theme variables */
}
@media (prefers-color-scheme: dark) {
  /* Dark theme variables */
}
```

Typography uses Nunito font family. UI components follow macOS design patterns with glass/frosted effects.

## Commit Message Convention

Format: `[FAI-####] type: one-line description`

**Types:** `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `release`

**Examples:**
- `[FAI-0100] docs: update README for v0.0.10 first public beta`
- `[FAI-0099] chore: regenerate icon.icns for FI monogram`
- `[FAI-0075] fix: restore chat rename and agent interaction functionality`

## Version Tagging

Tags use **numeric-only format** (no `v` prefix):
```bash
git tag 0.0.10
git push origin 0.0.10
```

Version is defined in `package.json` and auto-used by electron-builder for artifact naming.

## Release Process

1. Bump version in `package.json`
2. Update `CHANGELOG.md`
3. Commit changes with `[FAI-####] release: X.X.X ...` message
4. Create numeric tag: `git tag X.X.X`
5. Push: `git push origin main && git push origin X.X.X`
6. Build: `npm run build:quiet`
7. Create GitHub release:
   ```bash
   gh release create X.X.X \
     distro/Flaco-AI-X.X.X-arm64.dmg \
     distro/Flaco-AI-X.X.X-arm64.zip \
     --title "Flaco AI vX.X.X - Title" \
     --prerelease  # For beta releases
     --notes "Release notes..."
   ```

## Local Data Locations

**macOS:**
- App data: `~/Library/Application Support/flaco-desktop/`
- Config: `~/Library/Application Support/flaco-desktop/config.json`
- Chats: `~/Library/Application Support/flaco-desktop/chats.json`
- Encryption key: `~/Library/Application Support/flaco-desktop/encryption.key`
- Backups: `~/Library/Application Support/flaco-desktop/backups/`
- Logs: `~/Library/Logs/flaco-desktop/`

Override storage location: `export FLACO_STORE_DIR=/path/to/custom/location`

## Debugging

**Enable verbose logging:**
```bash
npm run dev  # Enables --enable-logging flag
```

**Access logs:**
- Via UI: Settings → Support & Debugging → Open Logs Folder
- Via CLI: `open ~/Library/Logs/flaco-desktop/`

**Check data directory:**
```bash
ls -la ~/Library/Application\ Support/flaco-desktop/
```

## Important UI Patterns

### Markdown Rendering
Messages use marked.js with custom renderer settings. Code blocks get syntax highlighting via highlight.js. Security: All HTML is sanitized to prevent XSS.

### Code Block Copy Buttons
Each code block automatically gets a copy button injected by `addCopyButtonsToCodeBlocks()` in renderer.js.

### Thinking Indicator
Shows active agent name with randomized status phrases. Toggleable with Cmd/Ctrl+O. Updates when agent switches or new messages arrive.

### Chat Rename Flow
- Double-click chat name OR click edit button
- Inline input appears with current name
- Enter = save, Escape = cancel, blur = save
- Immediately updates UI and persists to store

## Known Gotchas

1. **Inline onclick handlers** - Must expose functions globally on `window` object
2. **Encryption key migration** - App automatically migrates from legacy hardcoded key to file-based key
3. **First run detection** - `settings.firstRun` flag controls setup wizard display
4. **Model fetching** - Ollama must be running at configured endpoint for model list to populate
5. **Auto-updater 404s** - Silently ignored in development; only works with published GitHub releases
6. **Icon generation** - Requires macOS (uses `iconutil` command-line tool)
