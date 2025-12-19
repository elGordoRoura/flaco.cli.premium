# Claude Tickets – MVP Beta Release

Each ticket is small, independently releasable, and should be delivered via PR. Keep ASCII-only comments, avoid regressions to auto-updater/logging/cost slash command, and do not force-push `main`.

## 1) Send Behavior: Enter Sends, Cmd/Ctrl+Enter Newline
- **Goal:** In the message input, Enter sends; Cmd/Ctrl+Enter inserts a newline.
- **Files:** `renderer.js` (messageInput handlers, sendMessage trigger).
- **Details:** Prevent default newline on Enter, call `sendMessage()`. Cmd/Ctrl+Enter should insert `\n` at cursor and keep focus. Preserve auto-resize and slash-command handling. Avoid duplicate sends on key repeat.
- **Test:** Type → Enter sends. Type → Cmd/Ctrl+Enter inserts newline, no send. Slash commands still work.

## 2) Backend Context Clear for `/clear`
- **Goal:** `/clear` wipes UI and backend conversation context.
- **Files:** `main.js`, `preload.js`, `renderer.js`.
- **Details:** Add IPC `context:clear-conversation` to call `conversationManager.clearConversation(currentAgent)` and `persist()`. Expose via preload. In renderer `/clear`, call IPC, clear DOM + chat-manager, show confirmation.
- **Test:** Chat, run `/clear`, next AI reply has no prior context references.

## 3) Markdown Rendering Upgrade
- **Goal:** Robust markdown with syntax highlighting and copy buttons.
- **Files:** `renderer.js`, `package.json`.
- **Details:** Use `marked` + `highlight.js` to render messages safely (escape HTML). Preserve copy buttons on code blocks and existing tool-call UI. Style consistent with current theme.
- **Test:** Messages with headings/lists/code render correctly; code blocks have copy and highlight; no XSS.

## 4) Keyboard Shortcuts Set
- **Goal:** Add global shortcuts: Cmd/Ctrl+K new chat, Cmd/Ctrl+L clear chat (calls IPC from ticket #2), Cmd/Ctrl+, open settings, Cmd/Ctrl+Enter newline (from ticket #1), Enter send.
- **Files:** `renderer.js`.
- **Details:** Use keydown listener with meta/ctrl guards, prevent default where needed. Do not break text input focus.
- **Test:** Shortcuts work; no accidental triggers while typing unrelated keys.

## 5) Missing API Key Banner
- **Goal:** User-friendly banner when provider key is absent/invalid.
- **Files:** `renderer.js`.
- **Details:** On init and before send, if selected provider lacks a key, show inline banner with “Open Settings” button; do not crash. AI send should return `{success:false, error}` gracefully (ensure main IPC already does this).
- **Test:** Remove key, banner appears; clicking opens settings; send shows friendly error, not stack trace.

## 6) Cost Guidance in Settings
- **Goal:** Surface per-provider costs inside Settings.
- **Files:** `renderer.js` (settings UI).
- **Details:** Under provider selection, show read-only guidance: Local $0, Anthropic ~$3/1M input & $15/1M output (Sonnet 4), OpenAI ~$10/1M input & $30/1M output (GPT-4 Turbo). Note that Flaco adds no fees.
- **Test:** Costs visible and correct per provider.

## 7) Chat History UX Polish
- **Goal:** Improve chat list: search, sort, rename, star.
- **Files:** `renderer.js`, `chat-manager.js` (if needed).
- **Details:** Add search box to filter chats by name. Add sort toggle (Newest/Name). Add star flag per chat (persist in store). Existing rename inline edit is okay; add explicit edit icon. Favorites surface at top.
- **Test:** Search filters list; sort works; stars persist across reloads.

## 8) Export Selected Messages
- **Goal:** Export only selected messages to markdown.
- **Files:** `renderer.js`.
- **Details:** Add checkboxes per message (hover). New “Export selected” action; if none selected, fall back to full export. Use existing export IPC.
- **Test:** Select subset → export contains only those messages.

## 9) Logs Access for Support
- **Goal:** Quick access to logs for troubleshooting.
- **Files:** `renderer.js`, `main.js` (if IPC needed).
- **Details:** Add “Open logs folder” button in Settings/About that uses IPC to `shell.openPath(autoUpdater.logger.transports.file.getFile().path)` or log dir. If not available, show friendly error.
- **Test:** Button opens log folder; no crash if path missing.

## 10) Release Readiness and Docs
- **Goal:** Prep for 0.0.2 beta release.
- **Files:** `package.json`, `CHANGELOG.md`, `README.md` or `PRODUCTION_READINESS.md`.
- **Details:** Bump version to 0.0.2, add changelog entry summarizing new features/fixes. Add a short “Regenerate icon” note (sips/iconutil) referencing `assets/flaco-logo.svg`. Confirm `build.publish` stays GitHub. Do not remove auto-updater/logging.
- **Test:** `npm install` clean; `npm run build:quiet` succeeds; changelog updated.

## 11) Local Workspace Indexing (Milestone Slice 1: UI + Settings Only)
- **Goal:** Lay groundwork for local project context (no indexing yet).
- **Files:** `renderer.js`, `settings.js`, `preload.js`, `main.js`.
- **Details:** Add Workspace tab with folder picker (IPC `workspace:choose-folder`), display selected path stored in settings (`workspacePath`). Add ignore patterns field (default .gitignore + node_modules, dist, build, .venv) and max file size MB (default 1). No indexing logic; just storage and UI.
- **Test:** Choose folder dialog works; settings persist across reloads; ignore/size fields save.

## 12) Local Workspace Indexing (Milestone Slice 2: Index Skeleton)
- **Goal:** Basic index storage without embeddings.
- **Files:** `indexer.js` (new), `main.js`, `preload.js`.
- **Details:** Implement `workspace:index` IPC: walk files respecting ignore/size, chunk text, persist chunks + metadata to electron-store namespace `workspace-index`. Add `workspace:status` (counts, lastIndexed), `workspace:clear`. No embeddings yet. Add progress events or simple status return.
- **Test:** Index runs without crashing; status shows counts; clear removes data.

## 13) Local Workspace Indexing (Milestone Slice 3: Retrieval Hook)
- **Goal:** Attach top-K chunks to AI prompt (brute-force text match for now).
- **Files:** `indexer.js`, `main.js`.
- **Details:** Add simple similarity (TF-IDF-ish or substring scoring) over stored chunks; on send, fetch top-K and append to system prompt as “Context” with file path and snippet (200 chars). Add per-message toggle “Use project context” (default on if index exists).
- **Test:** With indexed data, messages include context snippets; toggle off removes them.

## 14) Local Workspace Indexing (Milestone Slice 4: Embeddings Local First)
- **Goal:** Upgrade retrieval to embeddings.
- **Files:** `indexer.js`, `package.json`.
- **Details:** Use `@xenova/transformers` with `all-MiniLM-L6-v2` to embed chunks; store vectors; brute-force cosine search is fine. Add fallback to OpenAI embeddings only if user enables and has key; otherwise stay local. Gate with setting “Allow cloud embeddings” (default false).
- **Test:** Local embeddings work offline; if model fails to load and cloud disabled, show friendly error; with cloud enabled and key present, embeddings succeed.

## 15) Citations UI + Reveal
- **Goal:** Show citations for attached context and allow reveal in Finder.
- **Files:** `renderer.js`, `main.js` (IPC for reveal).
- **Details:** When context used, display badge (“🔍 n snippets”) and expandable list with file path + preview. Add buttons: “Copy path” (clipboard) and “Reveal” (IPC to `shell.showItemInFolder`). Handle missing files gracefully.
- **Test:** Citations render; buttons work; no crash if file gone.

## 16) Rate Limit Guard
- **Goal:** Prevent runaway sends.
- **Files:** `renderer.js` (front-end guard), optional `main.js` guard.
- **Details:** Add configurable max sends per minute (default 20) stored in settings. Block send if exceeded, show warning. Reset counter on window focus or time window expiry.
- **Test:** Spamming send hits limit; normal use unaffected.

## 17) Token/Cost Estimator
- **Goal:** Show rough token/cost estimate per message.
- **Files:** `renderer.js`.
- **Details:** Estimate tokens by word/char heuristic; show under input with provider-specific $ estimate (use same rates as cost guidance). Non-blocking; purely informational.
- **Test:** Estimate updates as user types; costs match selected provider.

## 18) Conversation Export to HTML
- **Goal:** Export chat as styled HTML.
- **Files:** `renderer.js`.
- **Details:** Add “Export HTML” option using existing export IPC; include basic styles matching app theme; include timestamps if available.
- **Test:** Exported HTML opens with readable formatting and all messages.

## 19) Logs Tail in Settings
- **Goal:** Show last ~100 log lines inline.
- **Files:** `main.js` (IPC to read log file), `renderer.js`.
- **Details:** Expose `logs:get-latest` IPC to read the electron-log file; render in a scrollable box in Settings. Handle missing file gracefully.
- **Test:** Logs display; handles empty/missing.

## 20) Release Checklist Automation
- **Goal:** Add npm script to regenerate icon and prepare release.
- **Files:** `package.json`, docs.
- **Details:** Add script `package:icon` with sips/iconutil commands for `assets/flaco-logo.svg`. Add `release:prep` script that runs lint (placeholder), builds, and updates version? (document manual version bump). Document in README/PRODUCTION_READINESS.
- **Test:** Scripts run without errors (assuming macOS for icon).
