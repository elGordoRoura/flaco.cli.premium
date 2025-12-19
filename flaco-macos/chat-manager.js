const Store = require('electron-store');
const settings = require('./settings');

class ChatManager {
  constructor() {
    this.store = new Store({
      encryptionKey: settings.getEncryptionKey(),
      name: 'chats',
      cwd: settings.basePath
    });
    this.currentChatId = null;
    this.ensureChatsExist();
  }

  ensureChatsExist() {
    const chats = this.store.get('chats', []);

    // Create default chat if none exist
    if (chats.length === 0) {
      const defaultChat = {
        id: Date.now().toString(),
        name: 'Chat 1',
        messages: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      this.store.set('chats', [defaultChat]);
      this.currentChatId = defaultChat.id;
      this.store.set('currentChatId', this.currentChatId);
    } else {
      // Restore current chat ID
      this.currentChatId = this.store.get('currentChatId', chats[0].id);
    }
  }

  getAllChats() {
    return this.store.get('chats', []);
  }

  getCurrentChatId() {
    return this.currentChatId;
  }

  getCurrentChat() {
    const chats = this.getAllChats();
    return chats.find(chat => chat.id === this.currentChatId);
  }

  createChat(name = null) {
    const chats = this.getAllChats();
    const chatNumber = chats.length + 1;

    const newChat = {
      id: Date.now().toString(),
      name: name || `Chat ${chatNumber}`,
      messages: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    chats.push(newChat);
    this.store.set('chats', chats);

    // Switch to new chat
    this.currentChatId = newChat.id;
    this.store.set('currentChatId', this.currentChatId);

    return newChat;
  }

  switchChat(chatId) {
    const chats = this.getAllChats();
    const chat = chats.find(c => c.id === chatId);

    if (chat) {
      this.currentChatId = chatId;
      this.store.set('currentChatId', chatId);
      return chat;
    }

    return null;
  }

  renameChat(chatId, newName) {
    if (!newName || !newName.trim()) {
      return null;
    }

    const chats = this.getAllChats();
    const chatIndex = chats.findIndex(c => c.id === chatId);

    if (chatIndex !== -1) {
      const trimmed = newName.trim();
      chats[chatIndex].name = trimmed;
      chats[chatIndex].updatedAt = new Date().toISOString();
      this.store.set('chats', chats);
      // Persist current chat pointer so rename survives restarts
      this.store.set('currentChatId', this.currentChatId || chats[chatIndex].id);
      return chats[chatIndex];
    }

    return null;
  }

  toggleStar(chatId) {
    const chats = this.getAllChats();
    const chatIndex = chats.findIndex(c => c.id === chatId);

    if (chatIndex !== -1) {
      chats[chatIndex].starred = !chats[chatIndex].starred;
      chats[chatIndex].updatedAt = new Date().toISOString();
      this.store.set('chats', chats);
      return chats[chatIndex];
    }

    return null;
  }

  deleteChat(chatId) {
    let chats = this.getAllChats();

    // Don't delete if it's the only chat
    if (chats.length === 1) {
      return { success: false, error: 'Cannot delete the only chat' };
    }

    const chatIndex = chats.findIndex(c => c.id === chatId);

    if (chatIndex !== -1) {
      chats = chats.filter(c => c.id !== chatId);
      this.store.set('chats', chats);

      // If we deleted the current chat, switch to the first chat
      if (this.currentChatId === chatId) {
        this.currentChatId = chats[0].id;
        this.store.set('currentChatId', this.currentChatId);
      }

      return { success: true, newCurrentChatId: this.currentChatId };
    }

    return { success: false, error: 'Chat not found' };
  }

  addMessage(role, content, chatId = null) {
    const targetChatId = chatId || this.currentChatId;
    const chats = this.getAllChats();
    const chatIndex = chats.findIndex(c => c.id === targetChatId);

    if (chatIndex !== -1) {
      const message = {
        id: Date.now().toString() + Math.random(),
        role,
        content,
        timestamp: new Date().toISOString()
      };

      chats[chatIndex].messages.push(message);
      chats[chatIndex].updatedAt = new Date().toISOString();
      this.store.set('chats', chats);

      return message;
    }

    return null;
  }

  getMessages(chatId = null) {
    const targetChatId = chatId || this.currentChatId;
    const chat = this.getAllChats().find(c => c.id === targetChatId);
    return chat ? chat.messages : [];
  }

  clearMessages(chatId = null) {
    const targetChatId = chatId || this.currentChatId;
    const chats = this.getAllChats();
    const chatIndex = chats.findIndex(c => c.id === targetChatId);

    if (chatIndex !== -1) {
      chats[chatIndex].messages = [];
      chats[chatIndex].updatedAt = new Date().toISOString();
      this.store.set('chats', chats);
      return true;
    }

    return false;
  }

  deleteMessages(messageIds = [], chatId = null) {
    if (!Array.isArray(messageIds) || messageIds.length === 0) {
      return { success: false, error: 'No messages specified' };
    }

    const targetChatId = chatId || this.currentChatId;
    const chats = this.getAllChats();
    const chatIndex = chats.findIndex(c => c.id === targetChatId);

    if (chatIndex === -1) {
      return { success: false, error: 'Chat not found' };
    }

    const beforeCount = chats[chatIndex].messages.length;
    chats[chatIndex].messages = chats[chatIndex].messages.filter(
      (msg) => !messageIds.includes(msg.id)
    );
    chats[chatIndex].updatedAt = new Date().toISOString();
    this.store.set('chats', chats);

    return {
      success: true,
      removed: beforeCount - chats[chatIndex].messages.length
    };
  }
}

module.exports = ChatManager;
