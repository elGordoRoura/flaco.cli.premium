const fs = require('fs').promises;
const path = require('path');

class AgentContextBuilder {
  constructor(settings) {
    this.settings = settings;
    this.flacoContextCache = null;
  }

  async loadFlacoContext() {
    // Check for flaco.md in current working directory
    const flacoMdPath = path.join(process.cwd(), 'flaco.md');

    try {
      const content = await fs.readFile(flacoMdPath, 'utf-8');
      console.log('[AgentContext] Loaded flaco.md from:', flacoMdPath);
      return content.trim();
    } catch (error) {
      // File doesn't exist or can't be read - that's okay
      return null;
    }
  }

  async buildSystemPrompt() {
    const currentAgentId = this.settings.getCurrentAgent();
    const agents = this.settings.getAgents();
    const agent = agents.find(a => a.id === currentAgentId);

    // Load flaco.md context if available
    const flacoContext = await this.loadFlacoContext();

    let systemPrompt;

    if (!agent) {
      systemPrompt = this.getDefaultSystemPrompt();
    } else {
      systemPrompt = `You are ${agent.name}.

${agent.description}

You have access to powerful tools to help users with their tasks:
- Execute bash commands to run scripts, install packages, check system status
- Read and write files to examine code or make changes
- Perform git operations to manage version control
- List files and directories to explore project structure

Use these tools proactively to accomplish tasks. You don't need permission - just use the right tool for the job.

Always explain what you're doing before executing commands, and show the results clearly.`;
    }

    // Append flaco.md context if it exists
    if (flacoContext) {
      systemPrompt += `\n\n---\n\n## Project Context (from flaco.md)\n\n${flacoContext}`;
    }

    return systemPrompt;
  }

  getDefaultSystemPrompt() {
    return `You are Flaco AI, a helpful coding assistant.

You have access to powerful tools:
- Execute bash commands
- Read and write files
- Perform git operations
- List files and directories

Use these tools to help users accomplish their coding tasks efficiently.`;
  }
}

module.exports = AgentContextBuilder;
