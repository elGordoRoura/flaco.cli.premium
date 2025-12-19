const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('flaco', {
  // AI Communication
  sendMessage: (message) => ipcRenderer.invoke('ai:send-message', message),
  streamMessage: (message) => ipcRenderer.invoke('ai:stream-message', message),

  // Settings
  settings: {
    getAll: () => ipcRenderer.invoke('settings:get-all'),
    setProvider: (provider) => ipcRenderer.invoke('settings:set-provider', provider),
    setLocalEndpoint: (endpoint) => ipcRenderer.invoke('settings:set-local-endpoint', endpoint),
    setModel: (model) => ipcRenderer.invoke('settings:set-model', model),
    completeFirstRun: () => ipcRenderer.invoke('settings:complete-first-run'),
    resetFirstRun: () => ipcRenderer.invoke('settings:reset-first-run')
  },

  // Model Fetching
  models: {
    fetchLocal: () => ipcRenderer.invoke('models:fetch-local')
  },

  // Agent Management
  agents: {
    getAll: () => ipcRenderer.invoke('agents:get-all'),
    add: (agent) => ipcRenderer.invoke('agents:add', agent),
    update: (id, updates) => ipcRenderer.invoke('agents:update', id, updates),
    delete: (id) => ipcRenderer.invoke('agents:delete', id),
    setCurrent: (agentId) => ipcRenderer.invoke('agents:set-current', agentId),
    getCurrent: () => ipcRenderer.invoke('agents:get-current')
  },

  // Chat Management
  chats: {
    getAll: () => ipcRenderer.invoke('chats:get-all'),
    getCurrent: () => ipcRenderer.invoke('chats:get-current'),
    create: (name) => ipcRenderer.invoke('chats:create', name),
    switch: (chatId) => ipcRenderer.invoke('chats:switch', chatId),
    rename: (chatId, newName) => ipcRenderer.invoke('chats:rename', chatId, newName),
    toggleStar: (chatId) => ipcRenderer.invoke('chats:toggle-star', chatId),
    delete: (chatId) => ipcRenderer.invoke('chats:delete', chatId),
    getMessages: (chatId) => ipcRenderer.invoke('chats:get-messages', chatId),
    clearMessages: (chatId) => ipcRenderer.invoke('chats:clear-messages', chatId),
    addMessage: (role, content, chatId) => ipcRenderer.invoke('chats:add-message', role, content, chatId),
    deleteMessages: (messageIds, chatId) => ipcRenderer.invoke('chats:delete-messages', messageIds, chatId)
  },

  // File Operations
  files: {
    import: () => ipcRenderer.invoke('file:import'),
    export: (content, defaultName) => ipcRenderer.invoke('file:export', content, defaultName)
  },

  // Context Management
  context: {
    checkFlacoMd: () => ipcRenderer.invoke('context:check-flaco-md'),
    createFlacoMd: () => ipcRenderer.invoke('context:create-flaco-md'),
    getContextInfo: () => ipcRenderer.invoke('context:get-context-info'),
    getCurrent: () => ipcRenderer.invoke('agents:get-current'),
    clearConversation: () => ipcRenderer.invoke('context:clear-conversation')
  },

  // Logs & Support
  logs: {
    openFolder: () => ipcRenderer.invoke('logs:open-folder')
  },

  // Backup & Restore
  backup: {
    create: () => ipcRenderer.invoke('backup:create'),
    list: () => ipcRenderer.invoke('backup:list'),
    restore: (backupName) => ipcRenderer.invoke('backup:restore', backupName),
    delete: (backupName) => ipcRenderer.invoke('backup:delete', backupName),
    openFolder: () => ipcRenderer.invoke('backup:open-folder')
  }
});
