// Flaco Desktop App - Renderer Process
// marked and hljs are loaded globally from index.html

const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');
const deleteMessagesBtn = document.getElementById('deleteMessagesBtn');
let editingChatId = null;
let sendQueue = [];
let isSending = false;
let lastAgentDisplay = '🤖 Flaco';

// State
let selectedProvider = null;
let currentSetupStep = 1;
let selectedMessageIds = new Set();
let showThinkingIndicators = true;
let chatSortMenuOpen = false;

// ===========================================
// INITIALIZATION
// ===========================================

async function initialize() {
    console.log('Flaco Desktop App Initializing...');

    // Check if first run
    const settings = await window.flaco.settings.getAll();
    console.log('Settings:', settings);

    // Load custom agents and chats
    await loadAgents();
    await loadChats();
    updateSelectionActions();

    if (settings.firstRun) {
        showSetupWizard();
    } else {
        const agentDisplay = await getCurrentAgentDisplay();
        updateStatus('Ready', agentDisplay);
        checkAPIKeyStatus();
    }
}

async function checkAPIKeyStatus() {
    const settings = await window.flaco.settings.getAll();
    const banner = document.getElementById('apiKeyBanner');

    if (!settings || !banner) return;

    const needsEndpoint = !settings.localEndpoint;

    if (needsEndpoint) {
        banner.style.display = 'block';
    } else {
        banner.style.display = 'none';
    }
}

window.dismissBanner = function() {
    const banner = document.getElementById('apiKeyBanner');
    if (banner) banner.style.display = 'none';
}

// ===========================================
// SETUP WIZARD
// ===========================================

function showSetupWizard() {
    document.getElementById('setupWizard').style.display = 'flex';
    const topBtn = document.getElementById('setupTopButton');
    if (topBtn) {
        topBtn.textContent = '✕';
        topBtn.dataset.mode = 'close';
    }
    currentSetupStep = 1;
    showSetupStep(1);
}

function hideSetupWizard() {
    document.getElementById('setupWizard').style.display = 'none';
}

function showSetupStep(step) {
    // Hide all steps
    for (let i = 1; i <= 3; i++) {
        const stepEl = document.getElementById(`setupStep${i}`);
        if (stepEl) stepEl.style.display = 'none';
    }

    // Show current step
    const currentStep = document.getElementById(`setupStep${step}`);
    if (currentStep) {
        currentStep.style.display = 'block';
        currentSetupStep = step;
        const topBtn = document.getElementById('setupTopButton');
        if (topBtn) {
            if (step === 1) {
                topBtn.textContent = '✕';
                topBtn.dataset.mode = 'close';
            } else {
                topBtn.textContent = '←';
                topBtn.dataset.mode = 'back';
            }
        }
    }
}

window.nextSetupStep = function(step) {
    showSetupStep(step);
};

// New local-only setup functions
window.startLocalSetup = function() {
    selectedProvider = 'local';
    showSetupStep(3); // Go directly to local AI setup (step 3)
};

window.setupTopButtonAction = function() {
    const topBtn = document.getElementById('setupTopButton');
    if (!topBtn) return;
    const mode = topBtn.dataset.mode;
    if (mode === 'back') {
        nextSetupStep(1);
    } else {
        hideSetupWizard();
    }
};

window.fetchOllamaModels = async function() {
    const endpoint = document.getElementById('apiKeyInput').value.trim();
    const modelSelect = document.getElementById('modelSelect');
    const completeSetupBtn = document.getElementById('completeSetupBtn');

    if (!endpoint) {
        alert('Please enter your Ollama endpoint URL');
        return;
    }

    // Show loading state
    modelSelect.innerHTML = '<option value="">Fetching models...</option>';
    modelSelect.disabled = true;

    try {
        // Temporarily set endpoint to fetch models
        await window.flaco.settings.setLocalEndpoint(endpoint);

        const result = await window.flaco.models.fetchLocal();

        if (result.success && result.models.length > 0) {
            // Populate models
            modelSelect.innerHTML = result.models.map(model =>
                `<option value="${model.id}">${model.name}</option>`
            ).join('');
            modelSelect.disabled = false;

            // Enable complete setup button
            completeSetupBtn.disabled = false;
            completeSetupBtn.style.opacity = '1';
            completeSetupBtn.style.cursor = 'pointer';

            // Show success message
            addMessage('system', `✅ Found ${result.models.length} model(s)! Select one and complete setup.`);
        } else {
            modelSelect.innerHTML = '<option value="">No models found</option>';
            alert('No models found. Please make sure Ollama is running and you have pulled at least one model.');
        }
    } catch (error) {
        modelSelect.innerHTML = '<option value="">Error fetching models</option>';
        alert(`Failed to fetch models: ${error.message}\n\nMake sure Ollama is running with: ollama serve`);
    }
};

window.completeLocalSetup = async function() {
    const endpoint = document.getElementById('apiKeyInput').value.trim();
    const model = document.getElementById('modelSelect').value;

    if (!endpoint) {
        alert('Please enter your Ollama endpoint URL');
        return;
    }

    if (!model) {
        alert('Please fetch models and select one first');
        return;
    }

    // Save settings
    await window.flaco.settings.setProvider('local');
    await window.flaco.settings.setLocalEndpoint(endpoint);
    await window.flaco.settings.setModel(model);
    await window.flaco.settings.completeFirstRun();

    // Hide setup wizard
    hideSetupWizard();

    // Show success message
    updateStatus('Ready');
    addMessage('system', `✅ Setup complete! Connected to ${model} on ${endpoint}`);
};

// Single-provider (local) setup only

window.toggleApiKeyVisibility = function() {
    const input = document.getElementById('apiKeyInput');
    const btn = event.currentTarget;

    if (input.type === 'password') {
        input.type = 'text';
        btn.textContent = '🙈';
    } else {
        input.type = 'password';
        btn.textContent = '👁️';
    }
};

window.completeSetup = async function() {
    // Legacy entry point: defer to local-only setup
    await completeLocalSetup();
};

// ===========================================
// SETTINGS MODAL
// ===========================================

window.openSettings = async function() {
    const settings = await window.flaco.settings.getAll();

    // Populate current endpoint and model
    document.getElementById('settingsApiKey').value = settings.localEndpoint || 'http://localhost:11434';

    // Try to fetch and populate models
    const modelSelect = document.getElementById('settingsModel');
    modelSelect.innerHTML = '<option value="">Loading models...</option>';
    modelSelect.disabled = true;

    try {
        const result = await window.flaco.models.fetchLocal();
        if (result.success && result.models.length > 0) {
            modelSelect.innerHTML = result.models.map(model =>
                `<option value="${model.id}">${model.name}</option>`
            ).join('');
            modelSelect.value = settings.model || result.models[0].id;
            modelSelect.disabled = false;
        } else {
            modelSelect.innerHTML = '<option value="">Click "Fetch Models" first</option>';
        }
    } catch (error) {
        modelSelect.innerHTML = '<option value="">Click "Fetch Models" first</option>';
    }

    document.getElementById('settingsModal').style.display = 'flex';
};

window.fetchModelsInSettings = async function() {
    const endpoint = document.getElementById('settingsApiKey').value.trim();
    const modelSelect = document.getElementById('settingsModel');

    if (!endpoint) {
        alert('Please enter your Ollama endpoint URL');
        return;
    }

    modelSelect.innerHTML = '<option value="">Fetching models...</option>';
    modelSelect.disabled = true;

    try {
        await window.flaco.settings.setLocalEndpoint(endpoint);
        const result = await window.flaco.models.fetchLocal();

        if (result.success && result.models.length > 0) {
            modelSelect.innerHTML = result.models.map(model =>
                `<option value="${model.id}">${model.name}</option>`
            ).join('');
            modelSelect.disabled = false;
            alert(`✅ Found ${result.models.length} model(s)!`);
        } else {
            modelSelect.innerHTML = '<option value="">No models found</option>';
            alert('No models found. Please make sure Ollama is running and you have pulled at least one model.');
        }
    } catch (error) {
        modelSelect.innerHTML = '<option value="">Error fetching models</option>';
        alert(`Failed to fetch models: ${error.message}\n\nMake sure Ollama is running with: ollama serve`);
    }
};

window.closeSettings = async function() {
    const endpoint = document.getElementById('settingsApiKey').value.trim();
    const model = document.getElementById('settingsModel').value;

    if (endpoint && model) {
        await window.flaco.settings.setProvider('local');
        await window.flaco.settings.setLocalEndpoint(endpoint);
        await window.flaco.settings.setModel(model);
    }

    document.getElementById('settingsModal').style.display = 'none';
};

window.openLogsFolder = async function() {
    try {
        const result = await window.flaco.logs.openFolder();
        if (!result.success) {
            alert(`Could not open logs folder: ${result.error}\nPath: ${result.path || 'unknown'}`);
        }
    } catch (error) {
        console.error('Error opening logs folder:', error);
        alert(`Error opening logs folder: ${error.message}`);
    }
};


// ===========================================
// AGENT MANAGEMENT
// ===========================================

let currentAgents = [];

const randomNames = [
    'Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Taylor', 'Cameron',
    'Avery', 'Parker', 'Quinn', 'Reese', 'Skyler', 'Drew', 'Finley'
];

const specializations = [
    'Expert', 'Specialist', 'Architect', 'Engineer', 'Developer',
    'Analyst', 'Consultant', 'Advisor'
];

async function loadAgents() {
    const result = await window.flaco.agents.getAll();
    if (result.success) {
        currentAgents = result.agents;
        displayAgents();

        // Update agent indicator with current agent
        const currentAgentId = await window.flaco.agents.getCurrent();
        const currentAgent = currentAgents.find(a => a.id === currentAgentId);
        if (currentAgent) {
            updateAgentIndicator(currentAgent);
        }
    }
}

function displayAgents() {
    const agentList = document.getElementById('agentList');

    if (currentAgents.length === 0) {
        agentList.innerHTML = `
            <div class="no-agents-message">
                <p>No agents yet! Create your first specialized agent.</p>
            </div>
        `;
        return;
    }

    agentList.innerHTML = currentAgents.map(agent => `
        <div class="agent-item" onclick="selectAgent('${agent.id}')">
            <div class="agent-item-header">
                <div class="agent-name">${agent.emoji} ${agent.name}</div>
                <button class="agent-delete-btn" onclick="event.stopPropagation(); deleteAgent('${agent.id}')" title="Delete agent">
                    ×
                </button>
            </div>
        </div>
    `).join('');
}

window.openAgentCreator = function() {
    document.getElementById('agentCreatorModal').style.display = 'flex';
    // Reset form
    document.getElementById('agentEmoji').value = '';
    document.getElementById('agentName').value = '';
    document.getElementById('agentDescription').value = '';
};

window.closeAgentCreator = function() {
    document.getElementById('agentCreatorModal').style.display = 'none';
};

window.generateRandomName = function() {
    const name = randomNames[Math.floor(Math.random() * randomNames.length)];
    const spec = specializations[Math.floor(Math.random() * specializations.length)];
    document.getElementById('agentName').value = `${name} - ${spec}`;
};

window.saveNewAgent = async function() {
    const name = document.getElementById('agentName').value.trim();
    const description = document.getElementById('agentDescription').value.trim();

    if (!name) {
        alert('Please enter an agent name');
        return;
    }

    if (!description) {
        alert('Please enter a description for your agent');
        return;
    }

    // Auto-assign emoji based on keywords
    const emoji = getEmojiForAgent(name, description);

    try {
        await window.flaco.agents.add({
            emoji,
            name,
            description
        });

        closeAgentCreator();
        await loadAgents();

        // Don't show a message - just silently add the agent to sidebar

    } catch (error) {
        console.error('Error creating agent:', error);
        alert('Error creating agent. Please try again.');
    }
};

// Auto-assign emoji based on agent name and description
function getEmojiForAgent(name, description) {
    const text = `${name} ${description}`.toLowerCase();

    // Programming languages
    if (text.includes('python')) return '🐍';
    if (text.includes('javascript') || text.includes('js') || text.includes('node')) return '💛';
    if (text.includes('typescript') || text.includes('ts')) return '💙';
    if (text.includes('react')) return '⚛️';
    if (text.includes('vue')) return '💚';
    if (text.includes('angular')) return '🅰️';
    if (text.includes('rust')) return '🦀';
    if (text.includes('go') || text.includes('golang')) return '🐹';
    if (text.includes('java')) return '☕';
    if (text.includes('swift')) return '🕊️';
    if (text.includes('kotlin')) return '🟣';

    // Domains
    if (text.includes('frontend') || text.includes('ui') || text.includes('design')) return '🎨';
    if (text.includes('backend') || text.includes('api')) return '⚙️';
    if (text.includes('fullstack') || text.includes('full-stack')) return '🌐';
    if (text.includes('devops') || text.includes('infrastructure')) return '🔧';
    if (text.includes('database') || text.includes('sql')) return '🗄️';
    if (text.includes('security') || text.includes('pentester')) return '🔒';
    if (text.includes('ml') || text.includes('machine learning') || text.includes('ai')) return '🧠';
    if (text.includes('data science') || text.includes('data')) return '📊';
    if (text.includes('mobile') || text.includes('ios') || text.includes('android')) return '📱';
    if (text.includes('cloud') || text.includes('aws') || text.includes('azure')) return '☁️';
    if (text.includes('docker') || text.includes('container')) return '🐳';

    // Default
    return '🤖';
}

window.selectAgent = async function(agentId) {
    const agent = currentAgents.find(a => a.id === agentId);
    if (agent) {
        await window.flaco.agents.setCurrent(agentId);
        updateStatus('Ready', `${agent.emoji} ${agent.name}`);

        // Update agent indicator in header
        updateAgentIndicator(agent);

        // Highlight selected agent
        document.querySelectorAll('.agent-item').forEach(item => {
            item.classList.remove('agent-selected');
        });
        event.currentTarget.classList.add('agent-selected');
    }
}

function updateAgentIndicator(agent) {
    const iconElement = document.getElementById('current-agent-icon');
    const displayElement = document.getElementById('current-agent-display');

    if (agent) {
        // Show: emoji name(description)
        iconElement.textContent = agent.emoji;
        displayElement.textContent = `${agent.name} (${agent.description})`;

        // Update tooltip
        document.getElementById('agent-indicator').title = `Current Agent: ${agent.name}\n${agent.description}`;
    } else {
        iconElement.textContent = '🤖';
        displayElement.textContent = 'Flaco AI';
        document.getElementById('agent-indicator').title = 'No agent selected';
    }
}

window.deleteAgent = async function(agentId) {
    const agent = currentAgents.find(a => a.id === agentId);
    if (!agent) return;

    if (confirm(`Delete agent "${agent.name}"?`)) {
        try {
            await window.flaco.agents.delete(agentId);
            await loadAgents();
            addMessage('assistant', `Agent "${agent.name}" has been deleted.`, '✨ System');
        } catch (error) {
            console.error('Error deleting agent:', error);
            alert('Error deleting agent. Please try again.');
        }
    }
}

// ===========================================
// CHAT MANAGEMENT
// ===========================================

let currentChats = [];
let currentChatId = null;

async function loadChats() {
    const result = await window.flaco.chats.getAll();
    if (result.success) {
        currentChats = result.chats;

        // Get current chat ID
        const currentResult = await window.flaco.chats.getCurrent();
        if (currentResult.success) {
            currentChatId = currentResult.chatId;
        }

        displayChats();

        // Load messages for current chat
        if (currentChatId) {
            await loadChatMessages(currentChatId);
        }
    }
}

let currentSortMode = 'newest'; // 'newest' or 'name'
let chatSearchQuery = '';

function displayChats() {
    const chatList = document.getElementById('chatList');

    if (currentChats.length === 0) {
        chatList.innerHTML = `
            <div class="no-chats-message">
                <p>Click + to start a new conversation</p>
            </div>
        `;
        return;
    }

    // Filter chats by search query
    let filteredChats = currentChats;
    if (chatSearchQuery) {
        filteredChats = currentChats.filter(chat =>
            chat.name.toLowerCase().includes(chatSearchQuery.toLowerCase())
        );
    }

    // Sort chats
    let sortedChats = [...filteredChats];
    if (currentSortMode === 'newest') {
        sortedChats.sort((a, b) => {
            // Starred chats first
            if (a.starred && !b.starred) return -1;
            if (!a.starred && b.starred) return 1;
            // Then by updatedAt
            return new Date(b.updatedAt) - new Date(a.updatedAt);
        });
    } else if (currentSortMode === 'name') {
        sortedChats.sort((a, b) => {
            // Starred chats first
            if (a.starred && !b.starred) return -1;
            if (!a.starred && b.starred) return 1;
            // Then alphabetically
            return a.name.localeCompare(b.name);
        });
    }

    chatList.innerHTML = sortedChats.map(chat => `
        <div class="chat-item ${chat.id === currentChatId ? 'chat-selected' : ''}" onclick="switchToChat('${chat.id}')">
            <div class="chat-item-header">
                <button class="chat-star-btn ${chat.starred ? 'starred' : ''}" onclick="event.stopPropagation(); toggleChatStar('${chat.id}')" title="${chat.starred ? 'Unstar' : 'Star'} chat">
                    ${chat.starred ? '⭐' : '☆'}
                </button>
                <div class="chat-name">
                    ${editingChatId === chat.id
                        ? `<input class="chat-rename-input" id="rename-${chat.id}" value="${chat.name}" onkeydown="handleRenameKey(event,'${chat.id}')" onblur="commitChatRename('${chat.id}')">`
                        : `<span ondblclick="event.stopPropagation(); startChatRename('${chat.id}')">${chat.name}</span>`
                    }
                </div>
                <button class="chat-edit-btn" onclick="event.stopPropagation(); startChatRename('${chat.id}')" title="Rename chat">✏️</button>
                <button class="chat-delete-btn" onclick="event.stopPropagation(); deleteChat('${chat.id}')" title="Delete chat">×</button>
            </div>
        </div>
    `).join('');
}

window.filterChats = function() {
    const searchInput = document.getElementById('chatSearch');
    chatSearchQuery = searchInput.value.trim();
    displayChats();
};

window.toggleSortMenu = function() {
    const menu = document.getElementById('chatSortMenu');
    if (!menu) return;
    refreshSortMenuState();
    chatSortMenuOpen = !chatSortMenuOpen;
    menu.style.display = chatSortMenuOpen ? 'flex' : 'none';
};

window.setSortMode = function(mode) {
    currentSortMode = mode;
    chatSortMenuOpen = false;
    const menu = document.getElementById('chatSortMenu');
    if (menu) menu.style.display = 'none';
    displayChats();
};

function refreshSortMenuState() {
    const menu = document.getElementById('chatSortMenu');
    if (!menu) return;
    menu.querySelectorAll('button').forEach(btn => {
        const mode = btn.dataset.mode;
        btn.classList.toggle('active', mode === currentSortMode);
    });
}

document.addEventListener('click', (event) => {
    const menu = document.getElementById('chatSortMenu');
    const toggle = document.querySelector('.chat-sort-btn');
    if (!menu || !toggle) return;
    if (!menu.contains(event.target) && !toggle.contains(event.target)) {
        chatSortMenuOpen = false;
        menu.style.display = 'none';
    }
});

window.toggleChatStar = async function(chatId) {
    try {
        const result = await window.flaco.chats.toggleStar(chatId);
        if (result.success) {
            await loadChats();
        }
    } catch (error) {
        console.error('Error toggling chat star:', error);
    }
}

window.createNewChat = async function() {
    try {
        const result = await window.flaco.chats.create();
        if (result.success) {
            currentChatId = result.chat.id;
            await loadChats();
        }
    } catch (error) {
        console.error('Error creating chat:', error);
        alert('Error creating chat. Please try again.');
    }
};

window.switchToChat = async function(chatId) {
    try {
        const result = await window.flaco.chats.switch(chatId);
        if (result.success) {
            currentChatId = chatId;
            displayChats();
            await loadChatMessages(chatId);
        }
    } catch (error) {
        console.error('Error switching chat:', error);
    }
}

async function loadChatMessages(chatId) {
    try {
        // Clear current messages in UI
        const chatMessagesDiv = document.getElementById('chatMessages');
        chatMessagesDiv.innerHTML = '';
        clearSelections();

        // Load messages from chat
        const result = await window.flaco.chats.getMessages(chatId);
        if (result.success && result.messages.length > 0) {
            // Display each message
            result.messages.forEach(msg => {
                const agentForMessage = msg.role === 'assistant' ? lastAgentDisplay : null;
                addMessage(msg.role, msg.content, agentForMessage, msg.tool_calls, msg.id);
            });
        }
    } catch (error) {
        console.error('Error loading chat messages:', error);
    }
}

window.startChatRename = function(chatId) {
    const chat = currentChats.find(c => c.id === chatId);
    if (!chat) return;

    editingChatId = chatId;
    displayChats();
    setTimeout(() => {
        const input = document.getElementById(`rename-${chatId}`);
        if (input) {
            input.focus();
            input.select();
        }
    }, 0);
}

function handleRenameKey(e, chatId) {
    if (e.key === 'Enter') {
        e.preventDefault();
        commitChatRename(chatId);
    } else if (e.key === 'Escape') {
        editingChatId = null;
        displayChats();
    }
}

async function commitChatRename(chatId) {
    const input = document.getElementById(`rename-${chatId}`);
    if (!input) return;
    const newName = input.value.trim();
    if (!newName) {
        editingChatId = null;
        displayChats();
        return;
    }
    try {
        const result = await window.flaco.chats.rename(chatId, newName);
        editingChatId = null;
        if (result.success) {
            await loadChats();
            currentChatId = chatId;
        } else {
            alert(result.error || 'Could not rename chat');
        }
    } catch (error) {
        editingChatId = null;
        console.error('Error renaming chat:', error);
        alert('Error renaming chat. Please try again.');
    }
}
window.handleRenameKey = handleRenameKey;
window.commitChatRename = commitChatRename;

window.deleteChat = async function(chatId) {
    const chat = currentChats.find(c => c.id === chatId);
    if (!chat) return;

    if (confirm(`Delete chat "${chat.name}"?`)) {
        try {
            const result = await window.flaco.chats.delete(chatId);
            if (result.success) {
                currentChatId = result.newCurrentChatId || null;
                await loadChats();
            }
        } catch (error) {
            console.error('Error deleting chat:', error);
            alert('Error deleting chat. Please try again.');
        }
    }
}

// ===========================================
// FILE OPERATIONS
// ===========================================

let conversationHistory = [];

window.importFile = async function() {
    try {
        const result = await window.flaco.files.import();

        if (result.canceled) return;

        if (result.success) {
            // Add imported content as a user message
            const message = `Here's the content from ${result.fileName}:\n\n${result.content}`;
            addMessage('user', `📁 Imported: ${result.fileName}`);
            addMessage('assistant', `I've received the content from **${result.fileName}**. What would you like me to do with it?`, '✨ System');

            // Auto-send the file content as context
            messageInput.value = `Please review this file:\n\n${result.content}`;

        } else {
            alert(`Error importing file: ${result.error}`);
        }
    } catch (error) {
        console.error('Import error:', error);
        alert('Error importing file. Please try again.');
    }
};

window.exportConversation = async function() {
    try {
        // Build markdown from conversation
        let markdown = '# Flaco AI Conversation\n\n';
        markdown += `*Exported: ${new Date().toLocaleString()}*\n\n`;
        markdown += '---\n\n';

        const messages = document.querySelectorAll('.message');
        messages.forEach(msg => {
            const sender = msg.querySelector('.message-sender')?.textContent || 'Unknown';
            const content = msg.querySelector('.message-content')?.textContent || '';

            if (sender === 'You') {
                markdown += `## 👤 You\n\n${content}\n\n`;
            } else {
                markdown += `## 🤖 ${sender}\n\n${content}\n\n`;
            }

            markdown += '---\n\n';
        });

        const timestamp = new Date().toISOString().split('T')[0];
        const defaultName = `flaco-conversation-${timestamp}.md`;

        const result = await window.flaco.files.export(markdown, defaultName);

        if (result.canceled) return;

        if (result.success) {
            addMessage('assistant', `✅ Conversation exported successfully to:\n\n${result.filePath}`, '✨ System');
        } else {
            alert(`Error exporting conversation: ${result.error}`);
        }

    } catch (error) {
        console.error('Export error:', error);
        alert('Error exporting conversation. Please try again.');
    }
};

// Quick code review helper
window.startCodeReview = function() {
    const template = `Project review request
Language/stack: <fill in>
Goal: <what you’re building>
Focus: bugs, readability, maintainability, edge cases, security

Provide actionable recommendations and code snippets in the project’s language. Use fenced code blocks with the right language tag. If you need context, ask for specific files.`;

    messageInput.value = template;
    messageInput.focus();
    addMessage('assistant', 'Code review mode primed. Paste code snippets or import files, then hit Send. I will reply with language-specific suggestions and code blocks.', '🧠 Review');
};

// ===========================================
// MESSAGE SELECTION & DELETION
// ===========================================

function updateSelectionActions() {
    if (!deleteMessagesBtn) return;
    deleteMessagesBtn.style.display = selectedMessageIds.size > 0 ? 'inline-flex' : 'none';
}

function attachSelectionHandler(messageDiv, messageId) {
    const checkbox = messageDiv.querySelector('.message-checkbox');
    if (!checkbox) return;

    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            selectedMessageIds.add(messageId);
        } else {
            selectedMessageIds.delete(messageId);
        }
        updateSelectionActions();
    });
}

function clearSelections() {
    selectedMessageIds.clear();
    document.querySelectorAll('.message-checkbox').forEach(box => { box.checked = false; });
    updateSelectionActions();
}

function updateMessageId(oldId, newId) {
    const node = document.querySelector(`.message[data-message-id="${oldId}"]`);
    if (node) {
        node.setAttribute('data-message-id', newId);
        const checkbox = node.querySelector('.message-checkbox');
        if (checkbox) {
            checkbox.setAttribute('data-message-id', newId);
        }
    }
    if (selectedMessageIds.has(oldId)) {
        selectedMessageIds.delete(oldId);
        selectedMessageIds.add(newId);
    }
    updateSelectionActions();
}

window.deleteSelectedMessages = async function() {
    if (selectedMessageIds.size === 0) return;
    if (!currentChatId) {
        alert('No chat selected.');
        return;
    }

    const deleteEntireChat = confirm('Delete the entire chat instead of just selected messages?\n\nOK = delete entire chat\nCancel = delete only selected messages');
    if (deleteEntireChat) {
        await window.flaco.chats.clearMessages(currentChatId);
        chatMessages.innerHTML = '';
        await window.flaco.context.clearConversation();
        clearSelections();
        addMessage('assistant', 'Chat cleared', '✨ System');
        return;
    }

    const ids = Array.from(selectedMessageIds);
    const result = await window.flaco.chats.deleteMessages(ids, currentChatId);
    if (result.success) {
        ids.forEach((id) => {
            const node = document.querySelector(`.message[data-message-id="${id}"]`);
            if (node) node.remove();
        });
        clearSelections();
    } else {
        alert(result.error || 'Failed to delete selected messages');
    }
};

window.refreshFlacoContext = async function() {
    try {
        const result = await window.flaco.context.checkFlacoMd();

        if (result.exists) {
            const preview = result.content.substring(0, 150);
            addMessage('assistant', `✅ **flaco.md** found and will be loaded on your next message!\n\n**Preview:**\n${preview}${result.content.length > 150 ? '...' : ''}\n\n*Full context: ${result.content.length} characters*`, '🔄 System');
        } else {
            addMessage('assistant', `ℹ️ No **flaco.md** file found in the current directory.\n\nCreate a \`flaco.md\` file in your project directory to add persistent context to all conversations.\n\n**Tip:** See \`flaco.md.example\` for guidance.`, '🔄 System');
        }
    } catch (error) {
        console.error('Refresh flaco context error:', error);
        addMessage('assistant', `⚠️ Error checking flaco.md: ${error.message}`, '🔄 System');
    }
};

// ===========================================
// CHAT FUNCTIONALITY
// ===========================================

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Enter sends, Cmd/Ctrl+Enter inserts newline
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        if (e.metaKey || e.ctrlKey) {
            // Cmd/Ctrl+Enter: insert newline at cursor
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            const value = this.value;
            this.value = value.substring(0, start) + '\n' + value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;

            // Trigger auto-resize
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        } else if (!e.shiftKey) {
            // Plain Enter: send message
            e.preventDefault();
            sendMessage();
        }
    }
});

// Send button click
sendButton.addEventListener('click', sendMessage);

// Token and cost estimate
messageInput.addEventListener('input', updateTokenEstimate);

async function updateTokenEstimate() {
    const text = messageInput.value.trim();
    const tokenEstimateDiv = document.getElementById('tokenEstimate');

    if (!text) {
        tokenEstimateDiv.style.display = 'none';
        return;
    }

    // Rough token estimation: ~4 characters per token (common heuristic)
    const estimatedTokens = Math.ceil(text.length / 4);

    // Update display
    const tokenCountSpan = tokenEstimateDiv.querySelector('.token-count');
    const costEstimateSpan = tokenEstimateDiv.querySelector('.cost-estimate');

    tokenCountSpan.textContent = `~${estimatedTokens.toLocaleString()} tokens`;
    costEstimateSpan.textContent = 'Free (Local model)';

    tokenEstimateDiv.style.display = 'flex';
}

// Quick action commands
window.runCommand = function(command) {
    messageInput.value = command;
    sendMessage();
};

async function handleSlashCommand(command) {
    const cmd = command.toLowerCase();

    if (cmd === '/init') {
        // Create flaco.md file
        addMessage('user', '/init');

        try {
            const result = await window.flaco.context.createFlacoMd();

            if (result.success) {
                addMessage('assistant', `✅ **flaco.md** file created successfully!\n\n**Location:** \`${result.path}\`\n\n**What's next?**\n1. Edit the file to add your project context\n2. Click the 🔄 refresh button to preview it\n3. Your context will be loaded automatically on every message\n\n**Tip:** See \`flaco.md.example\` for ideas on what to include!`, '🎯 System');
            } else if (result.exists) {
                addMessage('assistant', `ℹ️ **flaco.md** already exists!\n\n**Location:** \`${result.path}\`\n\nClick the 🔄 refresh button to preview the current content, or edit the file directly.`, '🎯 System');
            } else {
                addMessage('assistant', `⚠️ Failed to create flaco.md: ${result.error}`, '🎯 System');
            }
        } catch (error) {
            console.error('Error creating flaco.md:', error);
            addMessage('assistant', `⚠️ Error: ${error.message}`, '🎯 System');
        }
    } else if (cmd === '/context') {
        // Show context information
        addMessage('user', '/context');

        try {
            const result = await window.flaco.context.getContextInfo();

            const messageCount = result.messageCount;
            const limit = result.limit;
            const percentage = Math.round((messageCount / limit) * 100);
            const remaining = limit - messageCount;

            let statusEmoji = '🟢';
            let status = 'Good';
            if (percentage > 80) {
                statusEmoji = '🔴';
                status = 'High - Consider starting new conversation';
            } else if (percentage > 60) {
                statusEmoji = '🟡';
                status = 'Moderate';
            }

            const bar = '█'.repeat(Math.floor(percentage / 5)) + '░'.repeat(20 - Math.floor(percentage / 5));

            addMessage('assistant', `${statusEmoji} **Conversation Context**\n\n**Messages:** ${messageCount} / ${limit}\n**Remaining:** ${remaining} messages\n**Usage:** ${percentage}%\n\n\`${bar}\`\n\n**Status:** ${status}\n\n**Tip:** Context is limited to the most recent ${limit} messages to prevent token overflow.`, '📊 System');
        } catch (error) {
            console.error('Error getting context info:', error);
            addMessage('assistant', `⚠️ Error: ${error.message}`, '📊 System');
        }
    } else if (cmd === '/clear') {
        // Clear chat messages
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        clearSelections();

        // Clear messages in chatManager
        if (currentChatId) {
            await window.flaco.chats.clearMessages(currentChatId);
        }

        // Clear AI conversation context
        await window.flaco.context.clearConversation();

        // Show confirmation
        addMessage('assistant', 'Chat and context cleared', '✨ System');
    } else if (cmd === '/costs') {
        // Cost transparency (local-first)
        const costMessage = '💰 **Cost overview**\n\nRunning on **local models (Ollama)** — API cost: **$0**. Performance depends on your hardware.\n\nFlaco runs locally and does not meter or store usage.';
        addMessage('assistant', costMessage, '💵 System');
    } else {
        // Unknown command
        addMessage('user', command);
        addMessage('assistant', `❓ Unknown command: **${command}**\n\n**Available commands:**\n- \`/init\` - Create flaco.md context file\n- \`/context\` - Show conversation context status\n- \`/clear\` - Clear the chat\n- \`/costs\` - Cost guidance for your current provider`, '🎯 System');
    }
}

// Rate limiting
const MAX_SENDS_PER_MINUTE = 20;
const rateLimitWindow = [];

// Reset rate limit on window focus (user returned after being away)
window.addEventListener('focus', () => {
    // Clear rate limit window when user returns
    rateLimitWindow.length = 0;
});

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Rate limit check
    const now = Date.now();
    const oneMinuteAgo = now - 60000;

    while (rateLimitWindow.length > 0 && rateLimitWindow[0] < oneMinuteAgo) {
        rateLimitWindow.shift();
    }

    if (rateLimitWindow.length >= MAX_SENDS_PER_MINUTE) {
        const oldestSend = rateLimitWindow[0];
        const waitTime = Math.ceil((oldestSend + 60000 - now) / 1000);

        alert(`⚠️ Rate Limit Exceeded\n\nYou've sent ${MAX_SENDS_PER_MINUTE} messages in the last minute.\n\nPlease wait ${waitTime} seconds before sending again.\n\nThis prevents accidental API spam and helps control costs.`);
        messageInput.value = message;
        return;
    }

    rateLimitWindow.push(now);

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';

    // Handle slash commands immediately
    if (message.startsWith('/')) {
        await handleSlashCommand(message);
        return;
    }

    sendQueue.push(message);
    processSendQueue();
}

async function processSendQueue() {
    if (isSending || sendQueue.length === 0) return;
    isSending = true;
    const message = sendQueue.shift();

    // Add user message to chat
    let userMessageId = addMessage('user', message);

    if (currentChatId) {
        const saved = await window.flaco.chats.addMessage('user', message, currentChatId);
        if (saved?.success && saved.message?.id) {
            updateMessageId(userMessageId, saved.message.id);
            userMessageId = saved.message.id;
        }
    }

    // Resolve current agent display before calling backend
    const agentDisplay = await getCurrentAgentDisplay();

    // Show thinking indicator
    const thinkingId = addThinking(agentDisplay);
    updateStatus('Thinking...', agentDisplay);

    try {
        const result = await window.flaco.sendMessage(message);

        removeThinking(thinkingId);
        updateStatus('Ready', agentDisplay);

        if (result.success) {
            const responseAgentDisplay = await getCurrentAgentDisplay();
            const assistantMessageId = addMessage('assistant', result.response, responseAgentDisplay, result.toolCalls);

            if (currentChatId) {
                const savedAssistant = await window.flaco.chats.addMessage('assistant', result.response, currentChatId);
                if (savedAssistant?.success && savedAssistant.message?.id) {
                    updateMessageId(assistantMessageId, savedAssistant.message.id);
                }
            }
        } else {
            if (result.error === 'RATE_LIMIT_EXCEEDED') {
                const rateLimitMessage = `⏱️ Slow down a bit.

- ${MAX_SENDS_PER_MINUTE} messages / minute max
- Wait ${result.waitTime} seconds, then try again
- Keeps local models calm and tidy`;
                addMessage('assistant', rateLimitMessage, '⚠️ Rate Limit');
                messageInput.value = message;
            } else {
                addMessage('assistant', `Error: ${result.error}\n\nPlease check your API key in Settings.`, '⚠️ Error');
            }
        }

    } catch (error) {
        removeThinking(thinkingId);
        updateStatus('Error');
        console.error('Send message error:', error);
        addMessage('assistant', `Sorry, I encountered an error: ${error.message}`, '⚠️ Error');
    } finally {
        isSending = false;
        if (sendQueue.length > 0) {
            processSendQueue();
        }
    }
}

function addMessage(role, content, agent = null, toolCalls = null, messageId = null) {
    // Remove welcome message if it exists
    const welcome = chatMessages.querySelector('.welcome-message');
    if (welcome) {
        welcome.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    // Generate unique message ID for selection
    const resolvedId = messageId || `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    messageDiv.setAttribute('data-message-id', resolvedId);

    // Extract icon and name separately to avoid double emoji
    const { icon, name: sender } = resolveAgentMeta(role, agent);

    // Build message HTML with checkbox
    let messageHTML = `
        <div class="message-select-checkbox">
            <input type="checkbox" class="message-checkbox" data-message-id="${resolvedId}">
        </div>
        <div class="message-header">
            <span class="message-icon">${icon}</span>
            <span class="message-sender">${sender}</span>
        </div>
    `;

    // Add tool calls if present
    if (toolCalls && toolCalls.length > 0) {
        messageHTML += '<div class="tool-calls-container">';
        toolCalls.forEach(toolCall => {
            messageHTML += createToolCallBlock(toolCall);
        });
        messageHTML += '</div>';
    }

    // Add message content
    messageHTML += `
        <div class="message-content">
            ${formatMessage(content)}
        </div>
    `;

    messageDiv.innerHTML = messageHTML;
    attachCopyHandlers(messageDiv);
    attachSelectionHandler(messageDiv, resolvedId);

    // Add event listeners for tool call expand/collapse
    if (toolCalls && toolCalls.length > 0) {
        const toolHeaders = messageDiv.querySelectorAll('.tool-call-header');
        toolHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const details = header.nextElementSibling;
                details.classList.toggle('collapsed');
                const expandIcon = header.querySelector('.tool-expand');
                expandIcon.textContent = details.classList.contains('collapsed') ? '▼' : '▲';
            });
        });
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return resolvedId;
}

function resolveAgentMeta(role, agentDisplay = null) {
    if (role === 'user') {
        return { icon: '👤', name: 'You' };
    }

    if (agentDisplay) {
        const parts = agentDisplay.trim().split(/\s+/);
        const icon = parts[0] || '🤖';
        const name = parts.slice(1).join(' ') || 'Assistant';
        return { icon, name };
    }

    return { icon: '🤖', name: 'Flaco' };
}

function createToolCallBlock(toolCall) {
    return `
        <div class="tool-call-block">
            <div class="tool-call-header">
                <span class="tool-icon">🔧</span>
                <span class="tool-name">${toolCall.name}</span>
                <span class="tool-expand">▼</span>
            </div>
            <div class="tool-call-details collapsed">
                <div class="tool-input">
                    <strong>Input:</strong>
                    <pre>${JSON.stringify(toolCall.input, null, 2)}</pre>
                </div>
            </div>
        </div>
    `;
}

function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function sanitizeHtmlOutput(html) {
    const template = document.createElement('template');
    template.innerHTML = html;

    const dangerousTags = ['script', 'style', 'iframe', 'object', 'embed', 'link', 'meta'];
    dangerousTags.forEach(tag => {
        template.content.querySelectorAll(tag).forEach(node => node.remove());
    });

    template.content.querySelectorAll('*').forEach(node => {
        [...node.attributes].forEach(attr => {
            const name = attr.name.toLowerCase();
            const value = attr.value || '';
            if (name.startsWith('on')) {
                node.removeAttribute(attr.name);
            }
            if ((name === 'href' || name === 'src') && value.trim().toLowerCase().startsWith('javascript:')) {
                node.removeAttribute(attr.name);
            }
        });
    });

    template.content.querySelectorAll('a').forEach(anchor => {
        anchor.setAttribute('rel', 'noopener noreferrer');
        anchor.setAttribute('target', '_blank');
    });

    return template.innerHTML;
}

function registerOverlayDismiss(modalId, closeFn) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeFn();
        }
    });
}

function formatMessage(content) {
    // Configure marked to use highlight.js
    marked.setOptions({
        highlight: function(code, lang) {
            if (lang && hljs.getLanguage(lang)) {
                try {
                    return hljs.highlight(code, { language: lang }).value;
                } catch (err) {
                    console.error('Highlight error:', err);
                }
            }
            return hljs.highlightAuto(code).value;
        },
        breaks: true,
        gfm: true
    });

    // Custom renderer to add copy buttons to code blocks
    const renderer = new marked.Renderer();
    const originalCodeRenderer = renderer.code.bind(renderer);

    renderer.code = function(code, language) {
        const highlighted = originalCodeRenderer(code, language);
        const escapedCode = encodeURIComponent(code);
        const lang = language || 'code';

        return `
            <div class="code-block">
                <div class="code-block-header">
                    <span class="code-lang">${lang}</span>
                    <button class="copy-button" data-code="${escapedCode}">Copy</button>
                </div>
                ${highlighted}
            </div>
        `;
    };

    marked.use({ renderer });

    // Render markdown with XSS protection
    try {
        const rendered = marked.parse(content);
        return sanitizeHtmlOutput(rendered);
    } catch (err) {
        console.error('Markdown parse error:', err);
        return escapeHtml(content).replace(/\n/g, '<br>');
    }
}

function attachCopyHandlers(container) {
    const buttons = container.querySelectorAll('.copy-button');
    buttons.forEach(button => {
        button.addEventListener('click', async () => {
            try {
                const code = decodeURIComponent(button.dataset.code || '');
                await navigator.clipboard.writeText(code);
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 1200);
            } catch (error) {
                console.error('Copy failed:', error);
                button.textContent = 'Copy failed';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 1200);
            }
        });
    });
}

let thinkingCounter = 0;

async function getCurrentAgentDisplay() {
    try {
        const currentAgentId = await window.flaco.agents.getCurrent();
        const agentsResult = await window.flaco.agents.getAll();
        const agents = agentsResult.success ? agentsResult.agents : [];
        const agent = agents.find(a => a.id === currentAgentId);
        lastAgentDisplay = agent ? `${agent.emoji} ${agent.name}` : '🤖 Flaco';
        return lastAgentDisplay;
    } catch (error) {
        console.error('Agent display lookup failed:', error);
        lastAgentDisplay = '🤖 Flaco';
        return lastAgentDisplay;
    }
}

function addThinking(agentDisplay = null) {
    const display = agentDisplay || lastAgentDisplay || '🤖 Flaco';
    const id = `thinking-${thinkingCounter++}`;
    const messages = [
        'Thinking…',
        'Sketching…',
        'Digging in…',
        'Crunching…',
        'Stitching…',
        'Reviewing…',
        'Checking…'
    ];
    const label = messages[Math.floor(Math.random() * messages.length)];
    const { icon, name } = resolveAgentMeta('assistant', display);
    const thinkingDiv = document.createElement('div');
    thinkingDiv.id = id;
    thinkingDiv.className = 'thinking';
    thinkingDiv.innerHTML = `
        <span>${icon}</span>
        <span class="thinking-label">${name} — ${label}</span>
        <div class="thinking-dots">
            <div class="thinking-dot"></div>
            <div class="thinking-dot"></div>
            <div class="thinking-dot"></div>
        </div>
    `;
    thinkingDiv.style.display = showThinkingIndicators ? 'flex' : 'none';
    chatMessages.appendChild(thinkingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeThinking(id) {
    const thinking = document.getElementById(id);
    if (thinking) {
        thinking.remove();
    }
}

function toggleThinkingVisibility() {
    document.querySelectorAll('.thinking').forEach(node => {
        node.style.display = showThinkingIndicators ? 'flex' : 'none';
    });
}

// Update status indicator
function updateStatus(status, agent = null) {
    const statusIndicator = document.getElementById('status-indicator');
    const agentDisplay = document.getElementById('current-agent-display');
    const agentIcon = document.getElementById('current-agent-icon');

    if (status && statusIndicator) {
        const statusSpan = statusIndicator.querySelector('span:last-child');
        if (statusSpan) {
            statusSpan.textContent = status;
        }
    }

    if (agent && (agentDisplay || agentIcon)) {
        const meta = resolveAgentMeta('assistant', agent);
        if (agentDisplay) agentDisplay.textContent = meta.name;
        if (agentIcon) agentIcon.textContent = meta.icon;
    }
}

// ===========================================
// DEVELOPER UTILITIES
// ===========================================

// Reset to first run experience (for testing or re-onboarding)
window.resetToFirstRun = async function() {
    if (confirm('This will reset the app to first run experience. You will need to re-enter your API keys. Continue?')) {
        await window.flaco.settings.resetFirstRun();
        alert('App reset! Please refresh the page to see the setup wizard.');
        location.reload();
    }
};

// ===========================================
// APP INITIALIZATION
// ===========================================

// Global keyboard shortcuts
window.addEventListener('keydown', (e) => {
    const isMod = e.metaKey || e.ctrlKey;

    // Cmd/Ctrl+K: New chat
    if (isMod && e.key === 'k') {
        e.preventDefault();
        createNewChat();
    }

    // Cmd/Ctrl+L: Clear chat
    else if (isMod && e.key === 'l') {
        e.preventDefault();
        handleSlashCommand('/clear');
    }

    // Cmd/Ctrl+,: Open settings
    else if (isMod && e.key === ',') {
        e.preventDefault();
        openSettings();
    }

    // Cmd/Ctrl+O: Toggle thinking indicator visibility
    else if (isMod && (e.key === 'o' || e.key === 'O')) {
        e.preventDefault();
        showThinkingIndicators = !showThinkingIndicators;
        toggleThinkingVisibility();
    }
});

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Flaco Desktop App Ready!');
    console.log('💡 Tip: Call resetToFirstRun() in console to reset to setup wizard');
    initialize();

    // Overlay click-to-dismiss for modals
    registerOverlayDismiss('settingsModal', closeSettings);
    registerOverlayDismiss('agentCreatorModal', closeAgentCreator);
    registerOverlayDismiss('setupWizard', hideSetupWizard);
});
