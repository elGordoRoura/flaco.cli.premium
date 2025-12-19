"""
Custom AI Agents Management for Flaco CLI
Matches the desktop app's custom agent functionality
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm


class CustomAgent:
    """Represents a custom AI agent"""

    def __init__(self, id: str, emoji: str, name: str, description: str,
                 created_at: str = None, is_default: bool = False):
        self.id = id
        self.emoji = emoji
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now().isoformat()
        self.is_default = is_default

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "emoji": self.emoji,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "is_default": self.is_default
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CustomAgent':
        return cls(
            id=data["id"],
            emoji=data["emoji"],
            name=data["name"],
            description=data["description"],
            created_at=data.get("created_at"),
            is_default=data.get("is_default", False)
        )


class CustomAgentManager:
    """Manages custom AI agents - matches the desktop AgentManager"""

    def __init__(self, storage_dir: str = "~/.flaco"):
        self.storage_dir = Path(storage_dir).expanduser()
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.agents_file = self.storage_dir / "agents.json"
        self.console = Console()

        # Default agents (match desktop defaults)
        self.default_agents = [
            CustomAgent(
                id="default_python",
                emoji="🐍",
                name="Python Expert",
                description="Python expert specializing in data science, pandas, numpy, and machine learning workflows",
                is_default=True
            ),
            CustomAgent(
                id="default_frontend",
                emoji="⚛️",
                name="Frontend Developer",
                description="Frontend specialist focused on React, TypeScript, and modern web development",
                is_default=True
            ),
            CustomAgent(
                id="default_devops",
                emoji="🔧",
                name="DevOps Engineer",
                description="DevOps expert for AWS, Docker, Kubernetes, and CI/CD pipelines",
                is_default=True
            ),
        ]

        # Load or initialize
        self._load_agents()

    def _load_agents(self):
        """Load agents from storage"""
        if self.agents_file.exists():
            with open(self.agents_file, 'r') as f:
                data = json.load(f)
                self.custom_agents = [CustomAgent.from_dict(a) for a in data.get("custom_agents", [])]
                self.current_agent_id = data.get("current_agent_id")
        else:
            self.custom_agents = []
            self.current_agent_id = None
            self._save_agents()

    def _save_agents(self):
        """Save agents to storage"""
        data = {
            "custom_agents": [a.to_dict() for a in self.custom_agents],
            "current_agent_id": self.current_agent_id
        }
        with open(self.agents_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all_agents(self) -> List[CustomAgent]:
        """Get all agents (default + custom)"""
        return self.default_agents + self.custom_agents

    def get_agent(self, agent_id: str) -> Optional[CustomAgent]:
        """Get agent by ID or name"""
        all_agents = self.get_all_agents()

        # Try exact ID match
        for agent in all_agents:
            if agent.id == agent_id:
                return agent

        # Try name match (case-insensitive)
        for agent in all_agents:
            if agent.name.lower() == agent_id.lower():
                return agent

        return None

    def get_current_agent(self) -> Optional[CustomAgent]:
        """Get the currently active agent"""
        if not self.current_agent_id:
            return None
        return self.get_agent(self.current_agent_id)

    def set_current_agent(self, agent_id: str) -> Optional[CustomAgent]:
        """Set the current active agent"""
        agent = self.get_agent(agent_id)
        if agent:
            self.current_agent_id = agent.id
            self._save_agents()
            return agent
        return None

    def create_agent(self, emoji: str, name: str, description: str) -> CustomAgent:
        """Create a new custom agent"""
        agent_id = f"agent_{uuid.uuid4().hex[:12]}"
        agent = CustomAgent(agent_id, emoji, name, description)
        self.custom_agents.append(agent)
        self._save_agents()
        return agent

    def update_agent(self, agent_id: str, emoji: str = None, name: str = None,
                     description: str = None) -> Optional[CustomAgent]:
        """Update an existing custom agent"""
        for agent in self.custom_agents:
            if agent.id == agent_id:
                if agent.is_default:
                    return None  # Can't edit default agents

                if emoji:
                    agent.emoji = emoji
                if name:
                    agent.name = name
                if description:
                    agent.description = description

                self._save_agents()
                return agent
        return None

    def delete_agent(self, agent_id: str) -> bool:
        """Delete a custom agent"""
        for i, agent in enumerate(self.custom_agents):
            if agent.id == agent_id:
                if agent.is_default:
                    return False  # Can't delete default agents

                self.custom_agents.pop(i)

                # If deleting current agent, clear selection
                if self.current_agent_id == agent_id:
                    self.current_agent_id = None

                self._save_agents()
                return True
        return False

    def list_agents(self, show_table: bool = True) -> List[CustomAgent]:
        """List all agents with optional table display"""
        agents = self.get_all_agents()

        if show_table:
            table = Table(title="Available Agents", show_header=True)
            table.add_column("Emoji", style="yellow", width=6)
            table.add_column("Name", style="cyan")
            table.add_column("Description", style="white")
            table.add_column("Type", style="magenta", width=8)
            table.add_column("Current", style="green", width=8)

            for agent in agents:
                is_current = "→" if agent.id == self.current_agent_id else ""
                agent_type = "Default" if agent.is_default else "Custom"

                # Truncate description if too long
                desc = agent.description
                if len(desc) > 60:
                    desc = desc[:57] + "..."

                table.add_row(
                    agent.emoji,
                    agent.name,
                    desc,
                    agent_type,
                    is_current
                )

            self.console.print(table)

        return agents

    def create_agent_interactive(self) -> CustomAgent:
        """Interactively create a new agent"""
        self.console.print("\n[cyan]Create New Agent[/cyan]")
        self.console.print("[yellow]Tip: Use emojis like 🚀 🐍 ⚛️ 🔧 🎨 📊[/yellow]\n")

        emoji = Prompt.ask("Emoji")
        name = Prompt.ask("Agent Name", default="My Agent")
        description = Prompt.ask(
            "Description (what this agent specializes in)",
            default="Expert in..."
        )

        agent = self.create_agent(emoji, name, description)

        self.console.print(f"\n[green]✓ Created agent: {agent.emoji} {agent.name}[/green]")

        # Offer to switch to new agent
        if Confirm.ask("Switch to this agent now?", default=True):
            self.set_current_agent(agent.id)
            self.console.print(f"[green]✓ Switched to {agent.emoji} {agent.name}[/green]")

        return agent
