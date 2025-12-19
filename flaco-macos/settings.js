const { app } = require('electron');
const Store = require('electron-store');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const schema = {
  aiProvider: {
    type: 'string',
    enum: ['anthropic', 'openai', 'local'],
    default: 'local'
  },
  selectedModel: {
    type: 'string',
    default: 'llama3'
  },
  firstRun: {
    type: 'boolean',
    default: true
  },
  localModelEndpoint: {
    type: 'string',
    default: 'http://localhost:11434'
  },
  customAgents: {
    type: 'array',
    default: []
  },
  currentAgent: {
    type: 'string',
    default: 'default'
  }
};

class Settings {
  constructor() {
    this.basePath = process.env.FLACO_STORE_DIR || this.getUserDataPath();
    this.encryptionKey = this.ensureEncryptionKey();
    this.store = new Store({
      schema,
      encryptionKey: this.encryptionKey,
      name: 'config',
      cwd: this.basePath
    });
  }

  ensureEncryptionKey() {
    const legacyKey = 'flaco-ai-secure-storage';
    const keyPath = path.join(this.basePath, 'encryption.key');
    const storePath = path.join(this.basePath, 'config.json');

    try {
      // Ensure base directory exists
      fs.mkdirSync(this.basePath, { recursive: true, mode: 0o700 });

      // Reuse existing key if present
      if (fs.existsSync(keyPath)) {
        return fs.readFileSync(keyPath, 'utf-8');
      }

      // If a store already exists, keep using the legacy key to avoid data loss
      if (fs.existsSync(storePath)) {
        fs.writeFileSync(keyPath, legacyKey, { mode: 0o600 });
        return legacyKey;
      }

      // Fresh install: generate a unique key and persist it
      const newKey = crypto.randomBytes(32).toString('hex');
      fs.writeFileSync(keyPath, newKey, { mode: 0o600 });
      return newKey;
    } catch (error) {
      console.warn('Failed to set up encryption key; falling back to legacy key:', error);
      return legacyKey;
    }
  }

  getEncryptionKey() {
    return this.encryptionKey;
  }

  // Safely get userData path even before app "ready"
  getUserDataPath() {
    try {
      if (app && typeof app.getPath === 'function') {
        return app.getPath('userData');
      }
    } catch (error) {
      // fall through to fallback
    }

    // Fallback for early calls; ensure directory exists
    const fallback = path.join(process.cwd(), 'user-data');
    if (!fs.existsSync(fallback)) {
      fs.mkdirSync(fallback, { recursive: true, mode: 0o700 });
    }
    return fallback;
  }

  // AI Provider
  getProvider() {
    const provider = this.store.get('aiProvider');
    if (provider !== 'local') {
      this.store.set('aiProvider', 'local');
      return 'local';
    }
    return provider;
  }

  setProvider(provider) {
    // Force local-only provider
    this.store.set('aiProvider', 'local');
  }

  // Model Selection
  getModel() {
    return this.store.get('selectedModel');
  }

  setModel(model) {
    this.store.set('selectedModel', model);
  }

  // First Run
  isFirstRun() {
    return this.store.get('firstRun');
  }

  setFirstRunComplete() {
    this.store.set('firstRun', false);
  }

  // Local Model
  getLocalEndpoint() {
    return this.store.get('localModelEndpoint');
  }

  setLocalEndpoint(endpoint) {
    this.store.set('localModelEndpoint', endpoint);
  }

  // Validation
  hasValidConfig() {
    return this.getLocalEndpoint().length > 0;
  }

  // Custom Agents
  getAgents() {
    const agents = this.store.get('customAgents');

    // Initialize default agents if none exist
    if (agents.length === 0) {
      this.initializeDefaultAgents();
      return this.store.get('customAgents');
    }

    return agents;
  }

  initializeDefaultAgents() {
    const defaultAgents = [
      {
        id: 'default-python',
        emoji: '🐍',
        name: 'Python Expert',
        description: '**Python specialist** focusing on:\n- Data science and machine learning\n- Backend development with Django/Flask\n- Automation and scripting\n- Testing and debugging'
      },
      {
        id: 'default-frontend',
        emoji: '⚛️',
        name: 'Frontend Developer',
        description: '**Frontend specialist** focusing on:\n- React, Vue, and modern JavaScript\n- TypeScript and type-safe development\n- Responsive design and CSS\n- Performance optimization'
      },
      {
        id: 'default-devops',
        emoji: '🔧',
        name: 'DevOps Engineer',
        description: '**DevOps specialist** focusing on:\n- Docker and Kubernetes\n- CI/CD pipelines\n- AWS, Azure, and cloud infrastructure\n- Monitoring and observability'
      }
    ];

    this.store.set('customAgents', defaultAgents);
  }

  addAgent(agent) {
    const agents = this.getAgents();
    agents.push({
      id: Date.now().toString(),
      ...agent
    });
    this.store.set('customAgents', agents);
  }

  updateAgent(id, updates) {
    const agents = this.getAgents();
    const index = agents.findIndex(a => a.id === id);
    if (index !== -1) {
      agents[index] = { ...agents[index], ...updates };
      this.store.set('customAgents', agents);
    }
  }

  deleteAgent(id) {
    const agents = this.getAgents().filter(a => a.id !== id);
    this.store.set('customAgents', agents);
  }

  getCurrentAgent() {
    return this.store.get('currentAgent');
  }

  setCurrentAgent(agentId) {
    this.store.set('currentAgent', agentId);
  }

  // Get all settings (for UI)
  getAll() {
    return {
      provider: this.getProvider(),
      model: this.getModel(),
      localEndpoint: this.getLocalEndpoint(),
      firstRun: this.isFirstRun(),
      agents: this.getAgents(),
      currentAgent: this.getCurrentAgent()
    };
  }
}

module.exports = new Settings();
