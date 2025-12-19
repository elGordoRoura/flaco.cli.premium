const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const fs = require('fs').promises;
const { spawn } = require('child_process');
const settings = require('./settings');
const { autoUpdater } = require('electron-updater');
const log = require('electron-log');

// Import new v0.2.0 components
const ConversationManager = require('./conversation-manager');
const AgentContextBuilder = require('./agent-context-builder');
const ChatManager = require('./chat-manager');
const BackupManager = require('./backup-manager');
const ErrorHandler = require('./error-handler');

// Initialize error handling first (before anything else can fail)
const errorHandler = new ErrorHandler();

// Set app name BEFORE creating window (macOS menu bar)
if (process.platform === 'darwin') {
  app.setName('Flaco AI');
}

// Configure logging
log.transports.file.level = 'info';
autoUpdater.logger = log;

// Configure auto-updater
function configureAutoUpdater() {
  // Don't check for updates in development
  if (process.env.NODE_ENV === 'development') {
    log.info('Auto-updater disabled in development');
    return;
  }

  // Safely check for updates (don't crash if repo doesn't exist)
  async function safeCheckForUpdates() {
    try {
      await autoUpdater.checkForUpdatesAndNotify();
    } catch (error) {
      // Silently ignore 404 errors (repo not public yet)
      if (error.message && error.message.includes('404')) {
        log.info('GitHub releases not available yet (404) - skipping update check');
      } else {
        log.error('Auto-updater error:', error);
      }
    }
  }

  // Check for updates on startup (after 3 seconds to let app settle)
  setTimeout(() => {
    safeCheckForUpdates();
  }, 3000);

  // Check for updates every 6 hours
  setInterval(() => {
    safeCheckForUpdates();
  }, 6 * 60 * 60 * 1000);

  // Auto-updater events
  autoUpdater.on('checking-for-update', () => {
    log.info('Checking for updates...');
  });

  autoUpdater.on('update-available', (info) => {
    log.info('Update available:', info.version);
  });

  autoUpdater.on('update-not-available', (info) => {
    log.info('Update not available', info);
  });

  autoUpdater.on('error', (err) => {
    log.error('Auto-updater error:', err);
    dialog.showMessageBox({
      type: 'error',
      title: 'Auto-updater Error',
      message: 'An error occurred while checking for updates. Please check the logs for more information.',
      detail: err.message,
      buttons: ['OK']
    });
  });

  autoUpdater.on('download-progress', (progress) => {
    log.info(`Download progress: ${Math.round(progress.percent)}%`);
  });

  autoUpdater.on('update-downloaded', (info) => {
    log.info('Update downloaded:', info.version);

    // Notify user
    dialog.showMessageBox({
      type: 'info',
      title: 'Update Ready',
      message: `Flaco AI ${info.version} is ready to install`,
      detail: 'The update will be installed when you restart the application.',
      buttons: ['Restart Now', 'Later']
    }).then((result) => {
      if (result.response === 0) {
        autoUpdater.quitAndInstall();
      }
    });
  });
}

let mainWindow;
let pythonProcess;

// v0.2.0 components
let conversationManager = null;
let chatManager = null;
let backupManager = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'Flaco AI',
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#000000',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false
  });

  mainWindow.loadFile('index.html');

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

function startPythonBackend() {
  // Start the Flaco CLI in the background
  // This assumes flaco is installed and available in PATH
  console.log('Starting Flaco backend...');

  // You can also start a FastAPI server here if needed
  // pythonProcess = spawn('python3', ['-m', 'flaco.server'], {
  //   cwd: path.join(__dirname, '..')
  // });
}

app.whenReady().then(() => {
  initializeAIClients();

  // Initialize v0.2.0 components
  conversationManager = new ConversationManager(settings);
  conversationManager.load();
  chatManager = new ChatManager();
  backupManager = new BackupManager();

  // Initialize backup system
  backupManager.initialize().then(() => {
    // Create initial backup
    backupManager.createBackup();

    // Schedule daily backups (every 24 hours)
    setInterval(() => {
      backupManager.createBackup();
    }, 24 * 60 * 60 * 1000);
  });

  // Get current agent and start conversation
  const currentAgentId = settings.getCurrentAgent() || 'default';
  conversationManager.startConversation(currentAgentId);

  createWindow();
  startPythonBackend();
  configureAutoUpdater();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

// Initialize AI clients
function initializeAIClients() {
  const provider = settings.getProvider();
  if (provider !== 'local') {
    settings.setProvider('local');
  }
  console.log('Local AI mode - endpoint:', settings.getLocalEndpoint());
}

// IPC handlers for settings
ipcMain.handle('settings:get-all', async () => {
  return settings.getAll();
});

ipcMain.handle('settings:set-provider', async (event, provider) => {
  settings.setProvider(provider);
  initializeAIClients();
  return { success: true };
});

ipcMain.handle('settings:set-model', async (event, model) => {
  settings.setModel(model);
  return { success: true };
});

ipcMain.handle('settings:complete-first-run', async () => {
  settings.setFirstRunComplete();
  return { success: true };
});

ipcMain.handle('settings:reset-first-run', async () => {
  settings.store.set('firstRun', true);
  return { success: true };
});

ipcMain.handle('settings:set-local-endpoint', async (event, endpoint) => {
  settings.setLocalEndpoint(endpoint);
  return { success: true };
});

// IPC handlers for custom agents
ipcMain.handle('agents:get-all', async () => {
  return { success: true, agents: settings.getAgents() };
});

ipcMain.handle('agents:add', async (event, agent) => {
  settings.addAgent(agent);
  return { success: true };
});

ipcMain.handle('agents:update', async (event, id, updates) => {
  settings.updateAgent(id, updates);
  return { success: true };
});

ipcMain.handle('agents:delete', async (event, id) => {
  settings.deleteAgent(id);
  return { success: true };
});

ipcMain.handle('agents:set-current', async (event, agentId) => {
  settings.setCurrentAgent(agentId);
  return { success: true };
});

ipcMain.handle('agents:get-current', async () => {
  return settings.getCurrentAgent();
});

// IPC handlers for chat management
ipcMain.handle('chats:get-all', async () => {
  return { success: true, chats: chatManager.getAllChats() };
});

ipcMain.handle('chats:get-current', async () => {
  return { success: true, chatId: chatManager.getCurrentChatId() };
});

ipcMain.handle('chats:create', async (event, name) => {
  const newChat = chatManager.createChat(name);
  return { success: true, chat: newChat };
});

ipcMain.handle('chats:switch', async (event, chatId) => {
  const chat = chatManager.switchChat(chatId);
  if (chat) {
    return { success: true, chat };
  }
  return { success: false, error: 'Chat not found' };
});

ipcMain.handle('chats:rename', async (event, chatId, newName) => {
  const chat = chatManager.renameChat(chatId, newName);
  if (chat) {
    return { success: true, chat };
  }
  return { success: false, error: 'Chat not found' };
});

ipcMain.handle('chats:toggle-star', async (event, chatId) => {
  const chat = chatManager.toggleStar(chatId);
  if (chat) {
    return { success: true, chat };
  }
  return { success: false, error: 'Chat not found' };
});

ipcMain.handle('chats:delete', async (event, chatId) => {
  return chatManager.deleteChat(chatId);
});

ipcMain.handle('chats:get-messages', async (event, chatId) => {
  return { success: true, messages: chatManager.getMessages(chatId) };
});

ipcMain.handle('chats:clear-messages', async (event, chatId) => {
  const success = chatManager.clearMessages(chatId);
  return { success };
});

ipcMain.handle('chats:delete-messages', async (event, messageIds, chatId) => {
  const result = chatManager.deleteMessages(messageIds, chatId);
  return result;
});

ipcMain.handle('chats:add-message', async (event, role, content, chatId) => {
  const message = chatManager.addMessage(role, content, chatId);
  if (message) {
    return { success: true, message };
  }
  return { success: false, error: 'Failed to add message' };
});

// IPC handlers for file operations
ipcMain.handle('file:import', async () => {
  try {
    const result = await dialog.showOpenDialog(mainWindow, {
      properties: ['openFile'],
      filters: [
        { name: 'Markdown Files', extensions: ['md', 'markdown'] },
        { name: 'Text Files', extensions: ['txt'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    });

    if (result.canceled) {
      return { success: false, canceled: true };
    }

    const filePath = result.filePaths[0];
    const content = await fs.readFile(filePath, 'utf-8');
    const fileName = path.basename(filePath);

    return {
      success: true,
      content,
      fileName,
      filePath
    };

  } catch (error) {
    console.error('File import error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('file:export', async (event, content, defaultName) => {
  try {
    const result = await dialog.showSaveDialog(mainWindow, {
      defaultPath: defaultName || 'flaco-export.md',
      filters: [
        { name: 'Markdown Files', extensions: ['md'] },
        { name: 'Text Files', extensions: ['txt'] }
      ]
    });

    if (result.canceled) {
      return { success: false, canceled: true };
    }

    await fs.writeFile(result.filePath, content, 'utf-8');

    return {
      success: true,
      filePath: result.filePath
    };

  } catch (error) {
    console.error('File export error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

// IPC handler for context management (flaco.md)
ipcMain.handle('context:check-flaco-md', async () => {
  try {
    const flacoMdPath = path.join(process.cwd(), 'flaco.md');

    try {
      const content = await fs.readFile(flacoMdPath, 'utf-8');
      return {
        exists: true,
        content: content.trim(),
        path: flacoMdPath
      };
    } catch (error) {
      // File doesn't exist
      return {
        exists: false,
        path: flacoMdPath
      };
    }

  } catch (error) {
    console.error('Error checking flaco.md:', error);
    return {
      exists: false,
      error: error.message
    };
  }
});

ipcMain.handle('context:create-flaco-md', async () => {
  try {
    const flacoMdPath = path.join(process.cwd(), 'flaco.md');

    // Check if file already exists
    try {
      await fs.access(flacoMdPath);
      return {
        success: false,
        exists: true,
        path: flacoMdPath
      };
    } catch (error) {
      // File doesn't exist, create it
    }

    // Create template content
    const template = `# Flaco Context

Welcome to your Flaco context file! This file provides persistent context to your AI agents across all conversations.

## About This Project

Describe your project here. What does it do? What technologies does it use?

## Key Files & Structure

List important files and directories:
- \`src/\` - Source code
- \`tests/\` - Test files
- \`README.md\` - Project documentation

## Coding Standards

Your preferred coding style and conventions:
- Use TypeScript for new files
- Prefer async/await over promises
- Write tests for all new features
- Keep functions under 50 lines

## Common Commands

Frequently used commands in your project:
- \`npm run dev\` - Start development server
- \`npm test\` - Run tests
- \`npm run build\` - Build for production

## Current Work

What are you currently working on? Any context the AI should know?

## Notes

Any other important information...

---

**Tip:** Edit this file to customize the context for your project. The AI will load this on every message!
`;

    await fs.writeFile(flacoMdPath, template, 'utf-8');

    return {
      success: true,
      path: flacoMdPath
    };

  } catch (error) {
    console.error('Error creating flaco.md:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

ipcMain.handle('context:get-context-info', async () => {
  try {
    const messageCount = conversationManager.getMessages().length;
    const limit = 20; // Same as in getRecentMessages

    return {
      messageCount,
      limit
    };

  } catch (error) {
    console.error('Error getting context info:', error);
    return {
      messageCount: 0,
      limit: 20,
      error: error.message
    };
  }
});

ipcMain.handle('context:clear-conversation', async () => {
  try {
    const currentAgentId = settings.getCurrentAgent();
    conversationManager.clearConversation(currentAgentId);
    conversationManager.persist();
    return { success: true };
  } catch (error) {
    console.error('Error clearing conversation:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('logs:open-folder', async () => {
  try {
    const userDataPath = app.getPath('userData');
    const logsPath = path.join(userDataPath);

    // Check if directory exists
    try {
      await fs.access(logsPath);
      await shell.openPath(logsPath);
      return { success: true, path: logsPath };
    } catch (err) {
      return { success: false, error: 'Logs folder not found', path: logsPath };
    }
  } catch (error) {
    console.error('Error opening logs folder:', error);
    return { success: false, error: error.message };
  }
});

// Backup IPC handlers
ipcMain.handle('backup:create', async () => {
  return await backupManager.createBackup();
});

ipcMain.handle('backup:list', async () => {
  return await backupManager.listBackups();
});

ipcMain.handle('backup:restore', async (event, backupName) => {
  return await backupManager.restoreBackup(backupName);
});

ipcMain.handle('backup:delete', async (event, backupName) => {
  return await backupManager.deleteBackup(backupName);
});

ipcMain.handle('backup:open-folder', async () => {
  try {
    await shell.openPath(backupManager.backupDir);
    return { success: true, path: backupManager.backupDir };
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// IPC handlers for model fetching
ipcMain.handle('models:fetch-local', async () => {
  try {
    const endpoint = settings.getLocalEndpoint();
    const response = await fetch(`${endpoint}/api/tags`);

    if (!response.ok) {
      throw new Error('Failed to fetch models from Ollama');
    }

    const data = await response.json();
    const models = data.models.map(model => ({
      id: model.name,
      name: model.name,
      description: `Size: ${(model.size / 1024 / 1024 / 1024).toFixed(2)} GB`
    }));

    return { success: true, models };
  } catch (error) {
    console.error('Error fetching local models:', error);
    return {
      success: false,
      error: error.message,
      models: []
    };
  }
});

async function handleOllamaChat(model, message, systemPrompt, conversationHistory) {
  // Ollama doesn't support tools - just simple chat
  const endpoint = settings.getLocalEndpoint();

  const historyText = (conversationHistory || []).map((entry) => {
    const prefix = entry.role === 'assistant' ? 'Assistant' : 'User';
    if (typeof entry.content === 'string') {
      return `${prefix}: ${entry.content}`;
    }
    // Fallback for structured content
    return `${prefix}: ${JSON.stringify(entry.content)}`;
  }).join('\n');

  const prompt = `${systemPrompt || ''}\n\n${historyText}\nUser: ${message}\nAssistant:`;

  const response = await fetch(`${endpoint}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model,
      prompt: prompt,
      stream: false
    })
  });

  if (!response.ok) {
    throw new Error(`Ollama API error: ${response.statusText}`);
  }

  const data = await response.json();

  conversationManager.addAssistantMessage(data.response);
  conversationManager.persist();

  return {
    success: true,
    response: data.response
  };
}

// IPC handlers for AI communication
ipcMain.handle('ai:send-message', async (event, message) => {
  try {
    const provider = settings.getProvider();
    const model = settings.getModel();

    console.log('[AI] Sending message with provider:', provider);

    // Add user message to conversation history
    conversationManager.addUserMessage(message);

    // Build system prompt with agent context
    const agentContextBuilder = new AgentContextBuilder(settings);
    const systemPrompt = await agentContextBuilder.buildSystemPrompt();

    // Get conversation history (limited to recent messages)
    const conversationHistory = conversationManager.getRecentMessages(20);

    console.log('[AI] Conversation history length:', conversationHistory.length);

    // Local-only provider path
    settings.setProvider('local');
    return await handleOllamaChat(model, message, systemPrompt, conversationHistory);

  } catch (error) {
    console.error('AI Error:', error);
    return {
      success: false,
      error: error.message
    };
  }
});

// IPC handlers for streaming (for future enhancement)
ipcMain.handle('ai:stream-message', async (event, message) => {
  // TODO: Implement streaming for real-time responses
  return { success: false, error: 'Streaming not yet implemented' };
});
