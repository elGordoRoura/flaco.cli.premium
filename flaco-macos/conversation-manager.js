class ConversationManager {
  constructor(settings) {
    this.settings = settings;
    this.conversations = new Map(); // agentId -> messages[]
    this.currentConversation = null;
  }

  startConversation(agentId) {
    this.currentConversation = agentId;
    if (!this.conversations.has(agentId)) {
      this.conversations.set(agentId, []);
    }
  }

  addUserMessage(content) {
    if (!this.currentConversation) {
      // Default conversation if none selected
      this.startConversation('default');
    }

    const messages = this.conversations.get(this.currentConversation);
    messages.push({ role: 'user', content });
  }

  addAssistantMessage(content, toolCalls = null) {
    const messages = this.conversations.get(this.currentConversation);
    const message = { role: 'assistant', content };
    if (toolCalls) {
      message.tool_calls = toolCalls;
    }
    messages.push(message);
  }

  addToolResult(toolUseId, result) {
    const messages = this.conversations.get(this.currentConversation);
    messages.push({
      role: 'user',
      content: [{
        type: 'tool_result',
        tool_use_id: toolUseId,
        content: result
      }]
    });
  }

  getMessages() {
    if (!this.currentConversation) {
      return [];
    }
    return this.conversations.get(this.currentConversation) || [];
  }

  // Limit history to prevent token overflow
  getRecentMessages(limit = 20) {
    const messages = this.getMessages();
    if (messages.length <= limit) {
      return messages;
    }
    return messages.slice(-limit);
  }

  clearConversation(agentId = null) {
    const id = agentId || this.currentConversation;
    if (id) {
      this.conversations.set(id, []);
    }
  }

  persist() {
    // Save to electron-store
    // Convert Map to array for JSON serialization
    const conversationsArray = Array.from(this.conversations.entries());
    this.settings.store.set('conversations', conversationsArray);
  }

  load() {
    // Load from electron-store
    const saved = this.settings.store.get('conversations', []);
    this.conversations = new Map(saved);
  }
}

module.exports = ConversationManager;
