# Changelog

All notable changes to Flaco AI will be documented in this file.

## [0.0.7] - 2024-12-12

### Added
- Inline chat rename input with focus on click/double-click plus Enter/Escape/blur handling.
- Sort picker now uses a clear options menu beside search with active state highlighting.
- Code blocks now use theme-aware styling with copy buttons that respect light/dark mode.

### Changed
- Thinking indicator shows the active agent name with shorter randomized phrases and updates the header agent indicator.
- Message rendering tightened: numbered lists stay inside bubbles, dropdown carets/padding breathe better, and delete controls are clearly red.
- Light mode gains higher contrast backgrounds/borders and more saturated accent blue; dropdown focus states use the accent color.

### Fixed
- Chat responses process FIFO to avoid out-of-order answers.
- Assistant bubbles and tool-call blocks are readable in light mode.
- Chat rename immediately refreshes the list after saving.

## [0.0.8] - 2024-12-12

### Changed
- Switched typography to Nunito with clearer hierarchy for headers, titles, and subtitles.
- Refreshed dark/light themes with glassy Tahoe-inspired surfaces, higher contrast, and vibrant accent blues.
- Buttons, inputs, and chat/search controls now echo macOS styling with rounded glass, gradients, and inset highlights.
- Chat and agent lists gain Apple-like cards, shadows, and selection gradients for clearer focus.
- Message bubbles and code blocks pick up frosted, high-contrast styling for readability in both themes.

## [0.0.9] - 2024-12-12

### Changed
- Chat bubbles now match the capsule treatment used in chats/agents (solid gradients, crisp borders, softer shadows) in dark and light modes.
- User bubble keeps a bright gradient with a defined border; assistant bubble gains card-like fill for readability.
- Thinking indicator widened, glassy, and kept single-line labels to avoid wrapping.

## [0.0.10] - 2024-12-12

### Changed
- Light-mode system/assistant bubbles mirror sidebar capsules; thinking pill gets matching light styling.
- Links in messages brightened for better readability in both themes.
- Cached agent name now used on thinking badges and assistant messages loaded from history.
- App icon refreshed to FI monogram with a subtle circuit backdrop (SVG); regenerate icns when packaging.
- Icon refined to centered FI monogram with pixel sparks (run icon generation on host to rebuild icns).

## [0.0.6] - 2024-12-12

### Changed
- Build artifacts now live under `distro/<version>/` with consistent hyphenated names across platforms.
- Desktop build workflow updated to Node 20 and uploads only release artifacts (dmg/zip/blockmaps/latest-mac.yml/mac-*).
- Reinstall helper standardized as `reinstall-flaco`; numeric tags only (no `v` prefix).

### Fixed
- Package-lock version aligned to 0.0.6 locally (to avoid caching/version drift in tooling).
- Removed builder debug/effective config files from release bundles.

## [0.0.5] - 2024-12-12

### Added
- Code review quick action to prime review prompts with language-aware guidance.
- Thinking indicator now shows the active agent name with randomized status phrases; toggle with Cmd/Ctrl+O.
- Message input starts at four lines for more breathing room.

### Changed
- Dark theme refreshed with higher contrast, slate assistant bubbles, and header/sidebar gradients.
- Build artifacts now output to `distro/`; reinstall helper renamed to `reinstall-flaco`.

### Fixed
- Chat rename immediately updates the UI without needing a reload.
- Settings modal scrollbar stays inside rounded corners.

## [0.0.4] - 2024-12-12

### Added
- Local-only mode by default (Ollama/LM Studio), with UI copy updated to remove cloud providers.
- Message selection actions now surface a toolbar trash icon; delete selected messages or clear the whole chat.
- Sanitized markdown rendering to strip scripts/inline events and harden against injected HTML.
- Daily backups now include `encryption.key` so restores work on fresh machines.

### Fixed
- Chat rename now trims/validates names and reports errors when a rename fails.
- Numbered lists inside message bubbles keep their layout without overflowing the container.
- Sorting UI replaced with a clear picker for “Newest” vs “Name”.

### Changed
- Export simplified to markdown only (removed multiple export buttons).
- Default model set to `llama3` for local setups; token estimates always show as free.
- Version bump to 0.0.4.

## [0.0.2] - 2024-12-11

### 🎉 MVP Beta Release - Major UX Improvements!

#### ✨ New Features
- **Enter to Send** - Press Enter to send, Cmd/Ctrl+Enter for newline (natural messaging UX)
- **Markdown Rendering** - Professional syntax highlighting with marked + highlight.js
- **Keyboard Shortcuts** - Cmd/Ctrl+K (new chat), Cmd/Ctrl+L (clear), Cmd/Ctrl+, (settings)
- **API Key Banner** - Friendly inline warning when configuration is missing
- **Cost Guidance** - Transparent per-provider pricing in Settings (Local $0, Claude ~$3-15/1M tokens, GPT-4 ~$10-30/1M tokens)
- **Multi-Chat System** - Create, switch, rename, and delete multiple conversations
- **Custom App Icon** - Professional icon with code brackets and AI neural network design
- **Chat History Polish** - Search, sort (newest/name), star favorites, explicit edit button
- **Selective Export** - Export selected messages with checkboxes (hover to reveal)
- **HTML Export** - Beautiful styled HTML exports alongside markdown
- **Token/Cost Estimator** - Real-time estimation as you type with provider-specific costs
- **Rate Limit Guard** - Prevent API spam with 20 msgs/min limit and friendly warnings
- **Logs Access** - Quick access to logs folder from Settings for troubleshooting

#### 🔧 Improvements
- **/clear now resets AI context** - Properly clears backend conversation memory (no more context leakage)
- **Better Code Display** - Syntax highlighting on all code blocks with copy buttons
- **Improved Settings UI** - Inline cost breakdown and clearer configuration
- **Starred chats always at top** - Regardless of sort mode
- **Message checkboxes** - Hover over messages to select for export

#### 🐛 Fixes
- Fixed /clear command not resetting AI conversation history
- Fixed chat messages not persisting across sessions
- Fixed agent context not being included in AI prompts

#### 📚 Documentation
- Added `npm run package:icon` script to regenerate icon from SVG
- Updated CHANGELOG with detailed release notes
- Comprehensive commit messages for all 7 new features

---

## [0.0.1] - 2024-12-10

### 🎉 First Release - Full Featured!

**Flaco AI v0.0.1 is here!** Your personal AI coding team with Claude Code features, custom agents, multi-provider support, and privacy-first design.

### ✨ Features

#### Core Functionality
- **Custom AI Agents** - Create unlimited specialized agents with custom emojis, names, and descriptions
- **Multi-Provider Support** - Choose between Anthropic Claude, OpenAI GPT, or local Ollama models
- **Beautiful UI** - Clean, modern interface with dark/light mode support
- **Privacy First** - All data stored locally with encrypted settings
- **Conversation History** - Full message history with persistence across sessions
- **Agent Context Integration** - Agents use their specializations in every response

#### 🔧 Claude Code Features
- **Terminal Integration** - Execute bash commands directly from chat
- **File System Access** - Read, write, and list files
- **Git Operations** - Status, diff, commit operations
- **Tool Calling** - Full implementation for Anthropic and OpenAI providers
- **Automatic Execution** - AI can use tools without permission prompts
- **Tool Display** - Inline expandable blocks showing tool executions

#### 📄 Context Management
- **flaco.md Support** - Load project context from flaco.md file
- **Persistent Memory** - Context survives refreshes and new sessions
- **Refresh Button** - Check and preview flaco.md content
- **Example Template** - Included flaco.md.example for guidance

#### AI Providers
- ✅ **Anthropic Claude** integration (Sonnet 4, 3.5 Sonnet, Opus, Sonnet 3)
- ✅ **OpenAI GPT** integration (GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- ✅ **Ollama** local AI support with dynamic model fetching

#### File Operations
- 📁 **Import** markdown/text files for context
- 💾 **Export** conversations as markdown files
- Native file picker dialogs

#### Setup & Onboarding
- 🎯 Beautiful 3-step setup wizard
- Provider selection with recommendations
- API key management with secure storage
- Dynamic model fetching based on your API permissions

#### Agent Management
- ➕ Create custom agents with emoji picker
- 🎲 Random name generator
- 🗑️ Delete agents
- 🎯 Select active agent per conversation
- Agent sidebar with specialization descriptions

#### Settings
- ⚙️ Change AI provider anytime
- 🔄 Switch between models
- 🔐 Update API keys securely
- 💾 All settings encrypted locally

### 🎨 UI/UX
- Clean gradient-based design
- Smooth animations and transitions
- Responsive layout
- Keyboard shortcuts (Cmd+Enter to send)
- Status indicators
- Loading states
- Error handling

### 🔒 Security
- Encrypted local storage (electron-store)
- API keys never transmitted except to provider APIs
- No telemetry or tracking
- No cloud backend

### 📦 Platform Support
- macOS (Apple Silicon)
- macOS (Intel)
- Code signed for macOS

### 🐛 Known Issues
- Auto-updates not yet implemented (coming in v0.1.0)
- No cost tracking yet (coming in v0.1.0)
- Default Electron icon (custom icon coming soon)
- No streaming responses yet (coming in v0.1.0)

### 📋 Requirements
- macOS 10.12 or later
- API key from Anthropic or OpenAI (or Ollama installed locally)

---

## Coming in v0.1.0

- 🔄 Auto-updates
- 💰 Cost tracking and usage statistics
- ⌨️ More keyboard shortcuts
- 🎨 Custom app icon
- 🔍 Search conversations
- 📊 Better markdown rendering
- 🌊 Streaming responses
- 🔐 Permission system for dangerous operations
- 📂 Working directory selector

---

## How to Update

Since auto-updates aren't implemented yet:

1. Download the new DMG from [releases](https://github.com/yourusername/flaco-desktop/releases)
2. Replace the old app in Applications
3. Your settings and agents will be preserved!

---

**Full Changelog**: First release! 🎉
