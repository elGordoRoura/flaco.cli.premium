import json
import os
import re
import time
import uuid
from typing import List, Dict, Any, Optional, Tuple
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .llm import OllamaClient
from .tools import (
    ReadTool, WriteTool, EditTool, GlobTool, GrepTool,
    BashTool, GitTool, TodoTool, ToolResult, ToolStatus
)
from .permissions import PermissionManager, PermissionMode
from .context import FlacoContextLoader
from .agents import AgentRouter, SpecializedAgent
from .agents.custom_agents import CustomAgentManager
from .intelligence import AgentSwarm, SwarmTask
from .analytics import ContributionTracker
from .analytics.contributions import ActivityType
from .storage import LocalStorageManager


class FlacoAgent:
    """Main agent that orchestrates LLM interactions and tool execution"""

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "qwen2.5-coder:7b",
        permission_mode: PermissionMode = PermissionMode.INTERACTIVE,
        session_id: Optional[str] = None
    ):
        self.console = Console()
        self.llm = OllamaClient(base_url=ollama_url, model=model)
        self.permission_manager = PermissionManager(mode=permission_mode)
        self.context_loader = FlacoContextLoader()
        self.agent_router = AgentRouter()
        self.agent_swarm = AgentSwarm(self.agent_router)
        self.activity_tracker = ContributionTracker()
        self.custom_agent_manager = CustomAgentManager()
        self.current_agent: Optional[SpecializedAgent] = None
        self.current_swarm: Optional[SwarmTask] = None

        # Initialize tools
        self.tools = {
            "Read": ReadTool(),
            "Write": WriteTool(),
            "Edit": EditTool(),
            "Glob": GlobTool(),
            "Grep": GrepTool(),
            "Bash": BashTool(),
            "Git": GitTool(),
            "TodoWrite": TodoTool(),
        }

        # Local storage integration
        self.storage = LocalStorageManager()
        self.session_id = session_id or str(uuid.uuid4())

        # Conversation history
        self.messages: List[Dict[str, Any]] = []
        self.context_limit = int(os.getenv("FLACO_CONTEXT_LIMIT", "120"))
        self.base_system_prompt = self._build_base_system_prompt()

        # Load previous conversation if exists
        self._load_conversation()

    def _build_base_system_prompt(self) -> str:
        """Build the base system prompt with Flaco context"""
        base_prompt = """You are Flaco, a powerful AI coding assistant running locally via Ollama.

You help developers with software engineering tasks including:
- Writing, editing, and debugging code
- Understanding codebases and explaining code
- Running commands and analyzing outputs
- Managing git repositories
- Refactoring and optimizing code
- Creating documentation

You have access to powerful tools for file operations, command execution, and more.

# CRITICAL: CODE REVIEW BEHAVIOR

⚠️ WHEN THE USER ASKS YOU TO REVIEW, ANALYZE, EVALUATE, OR EXAMINE CODE:

YOU MUST:
1. Use the Read tool to examine ACTUAL file contents
2. Read the CODE inside the files, not just list filenames
3. Analyze the actual code logic, functions, and implementation
4. Provide specific feedback with code examples and line numbers from what you READ

YOU MUST NEVER:
- Use ONLY Glob or Grep to list files without reading them
- Provide a review based only on filenames or directory structure
- Give generic feedback without reading the actual code

THE USER WANTS YOU TO READ AND DEEPLY ANALYZE THE CODE ITSELF.
File listings are NOT code reviews. You must READ the files with the Read tool.

# IMPORTANT: Tool Execution

You MUST execute tools to complete tasks. When you need to use a tool:
1. Use the tool calling functionality provided by the API
2. ALTERNATIVELY: Output JSON in the format: {"name": "ToolName", "arguments": {arg1: val1, arg2: val2}}
3. DO NOT just describe what you would do - actually execute the tools
4. DO NOT output step-by-step plans without executing them
5. After using tools, you will see their results and can proceed with the next steps

# Tool Usage Guidelines

- Always use the appropriate tool for each task
- Execute tools immediately, don't just plan
- Request permission before making destructive changes
- Provide brief explanations of what you're doing
- Use TodoWrite to track multi-step tasks
- Read files before editing them
- Be precise and careful with file modifications

# Code Review Requirements (Detailed)

When performing code reviews, your analysis should include:
1. Code quality - smells, anti-patterns, readability
2. Bugs and logic errors - edge cases, potential runtime errors
3. Security - vulnerabilities, input validation, authentication
4. Performance - inefficient algorithms, unnecessary operations
5. Best practices - language idioms, framework conventions
6. Architecture - design patterns, separation of concerns
7. Error handling - try/catch, null checks, validation
8. Documentation - missing or unclear comments

Always:
- Reference specific line numbers from files you READ
- Quote actual code snippets from the files
- Prioritize findings by severity (critical, important, minor)
- Suggest concrete improvements with code examples

# Best Practices

- Follow existing code style and conventions
- Write clear, maintainable code
- Add comments only where necessary
- Test changes when possible
- Use git for version control

# Communication Style

- Be concise and direct
- Use markdown formatting for readability
- Explain your reasoning when helpful
- Ask questions if requirements are unclear
- EXECUTE tools to complete tasks, don't just describe them
"""

        # Add FLACO.md context if available
        flaco_context = self.context_loader.get_system_prompt_addition()
        if flaco_context:
            base_prompt += flaco_context

        return base_prompt

    def _build_system_prompt(self, agent: SpecializedAgent) -> str:
        """Build the full system prompt with agent specialization"""
        full_prompt = self.base_system_prompt

        # Add specialized agent prompt
        full_prompt += agent.get_system_prompt_addition()

        return full_prompt

    def _extract_json_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON tool calls from text response (fallback for models without native function calling)"""
        tool_calls = []

        # Pattern to match JSON objects that look like tool calls
        # Matches: {"name": "ToolName", "arguments": {...}}
        pattern = r'\{[^{}]*"name"\s*:\s*"([^"]+)"[^{}]*"arguments"\s*:\s*\{[^}]*\}[^}]*\}'

        # Find all potential JSON objects in the text
        json_objects = re.findall(r'\{(?:[^{}]|\{[^{}]*\})*\}', text)

        for json_str in json_objects:
            try:
                obj = json.loads(json_str)
                # Check if this looks like a tool call
                if "name" in obj and "arguments" in obj:
                    # Convert to Ollama tool call format
                    tool_call = {
                        "id": f"call_{len(tool_calls)}",
                        "function": {
                            "name": obj["name"],
                            "arguments": json.dumps(obj["arguments"]) if isinstance(obj["arguments"], dict) else obj["arguments"]
                        }
                    }
                    tool_calls.append(tool_call)
            except json.JSONDecodeError:
                continue

        return tool_calls

    def chat(self, user_message: str) -> Tuple[str, Dict[str, Any]]:
        """Process a user message and return the response with metrics"""
        start_time = time.time()

        # Check if a custom agent is selected (takes precedence over routing)
        custom_agent = self.custom_agent_manager.get_current_agent()
        if custom_agent:
            # Create a SpecializedAgent wrapper for the custom agent
            self.current_agent = SpecializedAgent(
                name=custom_agent.name,
                emoji=custom_agent.emoji,
                specialization=custom_agent.description,
                keywords=[],  # Custom agents don't need keyword routing
                priority=10  # High priority
            )
        else:
            # Check if this requires agent swarm collaboration
            self.current_swarm = self.agent_swarm.analyze_task(user_message)

            # Route to appropriate specialized agent
            if self.current_swarm:
                # Use primary agent from swarm
                self.current_agent = self.agent_router.get_agent(self.current_swarm.primary_agent)
            else:
                self.current_agent = self.agent_router.route(user_message)

        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        self._save_conversation()

        # Main conversation loop - handle tool calls
        max_iterations = 10
        iteration = 0
        total_tokens = 0
        llm_calls = 0

        while iteration < max_iterations:
            iteration += 1

            # Get LLM response with tools
            response = self._call_llm()
            llm_calls += 1

            # Track token usage if available
            if "eval_count" in response:
                total_tokens += response.get("eval_count", 0)
                total_tokens += response.get("prompt_eval_count", 0)

            # Check if there are tool calls
            if "tool_calls" in response.get("message", {}):
                tool_calls = response["message"]["tool_calls"]
                self._handle_tool_calls(tool_calls)
            else:
                # No more tool calls, check if JSON tool calls are in the text (fallback)
                assistant_message = response["message"]["content"]
                extracted_tool_calls = self._extract_json_tool_calls(assistant_message)

                if extracted_tool_calls:
                    # Found JSON tool calls in text, execute them
                    # Add the message to history first to avoid re-extracting
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    self._save_conversation()
                    self._handle_tool_calls(extracted_tool_calls)
                else:
                    # No tool calls at all, return the response
                    self.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    self._save_conversation()

                    # Calculate metrics
                    end_time = time.time()
                    metrics = {
                        "agent": self.current_agent.name,
                        "agent_emoji": self.current_agent.emoji,
                        "time_taken": end_time - start_time,
                        "tokens": total_tokens,
                        "llm_calls": llm_calls,
                        "iterations": iteration,
                        "swarm": self.current_swarm is not None,
                        "swarm_task": self.current_swarm.__dict__ if self.current_swarm else None
                    }

                    # Log activity
                    self.activity_tracker.log_activity(
                        ActivityType.CHAT_MESSAGE,
                        {"agent": self.current_agent.name, "tokens": total_tokens}
                    )

                    if self.current_swarm:
                        self.activity_tracker.log_activity(
                            ActivityType.AGENT_SWARM,
                            {"complexity": self.current_swarm.complexity.value}
                        )

                    return assistant_message, metrics

        end_time = time.time()
        metrics = {
            "agent": self.current_agent.name if self.current_agent else "Unknown",
            "agent_emoji": self.current_agent.emoji if self.current_agent else "⚡",
            "time_taken": end_time - start_time,
            "tokens": total_tokens,
            "llm_calls": llm_calls,
            "iterations": iteration,
            "swarm": self.current_swarm is not None,
            "swarm_task": self.current_swarm.__dict__ if self.current_swarm else None
        }

        return "Maximum iteration limit reached. Please try breaking down your request.", metrics

    def _call_llm(self) -> Dict[str, Any]:
        """Call the LLM with current messages and tool schemas"""

        # Prepare messages with specialized agent's system prompt
        agent_prompt = self._build_system_prompt(self.current_agent) if self.current_agent else self.base_system_prompt
        context_messages = self.messages[-self.context_limit:] if self.context_limit > 0 else self.messages

        # Filter out tool-related messages when tools are disabled
        # This prevents 400 errors from Ollama when tool messages exist in history
        cleaned_messages = []
        for msg in context_messages:
            # Skip messages with tool role or tool_calls field
            if msg.get("role") == "tool" or "tool_calls" in msg:
                continue
            cleaned_messages.append(msg)

        messages = [{"role": "system", "content": agent_prompt}] + cleaned_messages

        # Get tool schemas
        tool_schemas = [tool.get_schema() for tool in self.tools.values()]

        # Call Ollama with tools (will use native function calling if model supports it)
        response = self.llm.chat(
            messages=messages,
            tools=tool_schemas,
            temperature=0.7
        )

        return response

    def _handle_tool_calls(self, tool_calls: List[Dict[str, Any]]):
        """Execute tool calls and add results to conversation"""

        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])

            # Execute the tool
            result = self._execute_tool(function_name, arguments)

            # Add tool call and result to messages
            self.messages.append({
                "role": "assistant",
                "tool_calls": [tool_call]
            })

            self.messages.append({
                "role": "tool",
                "content": json.dumps(result.to_dict()),
                "tool_call_id": tool_call.get("id", "")
            })
            # Save after tool results
            self._save_conversation()

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> ToolResult:
        """Execute a tool with permission checking"""

        if tool_name not in self.tools:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Unknown tool: {tool_name}"
            )

        tool = self.tools[tool_name]

        # Check permissions
        if tool.requires_permission:
            action_desc = self._format_tool_action(tool_name, arguments)
            if not self.permission_manager.request_permission(tool_name, action_desc, arguments):
                return ToolResult(
                    status=ToolStatus.PERMISSION_DENIED,
                    output="",
                    error="Permission denied by user"
                )

        # Execute the tool
        try:
            result = tool.execute(**arguments)

            # Display result to user
            self._display_tool_result(tool_name, result)

            return result

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error executing {tool_name}: {str(e)}"
            )

    def _format_tool_action(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Format a tool action for permission display"""
        if tool_name == "Write":
            return f"Write to file: {arguments.get('file_path', 'unknown')}"
        elif tool_name == "Edit":
            return f"Edit file: {arguments.get('file_path', 'unknown')}"
        elif tool_name == "Bash":
            return f"Execute command: {arguments.get('command', 'unknown')}"
        elif tool_name == "Git":
            return f"Git {arguments.get('operation', 'unknown')}"
        else:
            return f"Execute {tool_name}"

    def _display_tool_result(self, tool_name: str, result: ToolResult):
        """Display tool execution result to user"""
        if result.status == ToolStatus.SUCCESS:
            icon = "✅"
            color = "green"
        elif result.status == ToolStatus.ERROR:
            icon = "❌"
            color = "red"
        else:
            icon = "⚠️"
            color = "yellow"

        self.console.print(f"\n{icon} [{color}]{tool_name}[/{color}]")

        if result.output:
            # Truncate very long outputs for display
            display_output = result.output
            if len(display_output) > 1000:
                display_output = display_output[:1000] + "\n... [truncated]"
            self.console.print(Panel(display_output, border_style=color))

        if result.error:
            self.console.print(f"[red]Error: {result.error}[/red]")

    def chat_with_image(self, message: str, image_path: str) -> str:
        """Process a message with an image attachment"""
        try:
            # Use LLM's image support
            response = self.llm.chat_with_image(
                message=message,
                image_path=image_path,
                system=self.system_prompt
            )

            assistant_message = response["message"]["content"]
            self.messages.append({"role": "user", "content": f"{message} [image: {image_path}]"})
            self.messages.append({"role": "assistant", "content": assistant_message})

            return assistant_message

        except Exception as e:
            return f"Error processing image: {str(e)}"

    def reset_conversation(self):
        """Clear conversation history"""
        self.messages = []
        # Clear from local storage
        if self.storage.connected:
            self.storage.clear_conversation(self.session_id)

    def get_conversation_summary(self) -> str:
        """Get a summary of the conversation"""
        return f"Messages: {len(self.messages)}"

    def get_context_info(self) -> Dict[str, Any]:
        """Return context usage and file info for status displays."""
        count = len(self.messages)
        limit = self.context_limit if self.context_limit > 0 else count
        used = min(count, limit) if limit else count
        percentage = int((used / limit) * 100) if limit else 0

        return {
            "has_context": self.context_loader.has_context(),
            "context_path": self.context_loader.get_context_path(),
            "message_count": count,
            "limit": limit,
            "remaining": max(limit - used, 0),
            "percentage": min(percentage, 100)
        }

    def create_context_file(self, target_dir: Optional[str] = None, overwrite: bool = False) -> Dict[str, Any]:
        """Create FLACO.md in the target directory using available templates."""
        return self.context_loader.create_context_file(target_dir=target_dir, overwrite=overwrite)

    def set_permission_mode(self, mode: PermissionMode):
        """Change permission mode"""
        self.permission_manager.set_mode(mode)

    def _load_conversation(self):
        """Load conversation history from local storage"""
        if self.storage.connected:
            messages = self.storage.load_conversation(self.session_id)
            if messages:
                self.messages = messages
                self.console.print(f"[dim]💾 Loaded {len(messages)} messages from previous session[/dim]")

    def _save_conversation(self):
        """Save conversation history to local storage"""
        if self.storage.connected:
            self.storage.save_conversation(self.session_id, self.messages)
