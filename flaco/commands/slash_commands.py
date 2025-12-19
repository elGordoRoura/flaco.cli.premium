import os
import json
from pathlib import Path
from typing import Dict, Callable, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from ..permissions import PermissionMode
from ..agents.custom_agents import CustomAgentManager
from .quick_actions import QuickActionManager
from ..config.user_config import UserConfig
from ..utils.snippets import snippet_library, SnippetCategory


class SlashCommandHandler:
    """Handles slash commands for Flaco"""

    def __init__(self, agent):
        self.agent = agent
        self.console = Console()
        self.agent_manager = CustomAgentManager()
        self.quick_actions = QuickActionManager()

        # Initialize theme_color with safe fallback
        try:
            user_config = UserConfig()
            self.theme_color = user_config.theme_color
        except:
            self.theme_color = "cyan"  # Safe default

        self.commands: Dict[str, Callable] = {
            "help": self.cmd_help,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
            "clear": self.cmd_clear,
            "reset": self.cmd_reset,
            "status": self.cmd_status,
            "init": self.cmd_init,
            "context": self.cmd_context,
            "costs": self.cmd_costs,
            "model": self.cmd_model,
            "models": self.cmd_models,
            "history": self.cmd_history,
            "permissions": self.cmd_permissions,
            "todos": self.cmd_todos,
            "scan": self.cmd_scan,
            "project": self.cmd_project,
            "git": self.cmd_git,
            "stats": self.cmd_stats,
            "recap": self.cmd_recap,
            "review": self.cmd_review,
            "refresh": self.cmd_refresh,
            "agent": self.cmd_agent,
            "actions": self.cmd_actions,
            "setup": self.cmd_setup,
            "reset-config": self.cmd_reset_config,
            "snippet": self.cmd_snippet,
            "snippets": self.cmd_snippet,
            "check-update": self.cmd_check_update,
            "run-update": self.cmd_run_update,
        }

        # Load custom commands from .flaco/commands/ if they exist
        self._load_custom_commands()

    def handle_command(self, command_str: str):
        """Handle a slash command"""
        parts = command_str[1:].split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if command in self.commands:
            self.commands[command](args)
        else:
            self.console.print(f"[red]Unknown command: /{command}[/red]")
            self.console.print("[yellow]Type /help to see available commands[/yellow]")

    def _load_custom_commands(self):
        """Load custom slash commands from .flaco/commands/"""
        commands_dir = Path.cwd() / ".flaco" / "commands"
        if commands_dir.exists():
            for cmd_file in commands_dir.glob("*.md"):
                cmd_name = cmd_file.stem
                self.commands[cmd_name] = lambda args, f=cmd_file: self._execute_custom_command(f, args)

    def _execute_custom_command(self, file_path: Path, args: str):
        """Execute a custom command from markdown file"""
        with open(file_path, 'r') as f:
            prompt = f.read()

        # Replace {args} placeholder if present
        if "{args}" in prompt:
            prompt = prompt.replace("{args}", args)
        elif args:
            prompt = f"{prompt}\n\n{args}"

        # Execute through agent
        self.console.print(f"\n[cyan]Executing custom command: {file_path.stem}[/cyan]")
        response, metrics = self.agent.chat(prompt)
        self.console.print(Markdown(response))

    # Built-in commands

    def cmd_help(self, args: str):
        """Show help information"""
        table = Table(title="Available Commands", show_header=True)
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")

        commands_help = [
            ("/help", "Show this help message"),
            ("/setup", "🎯 Interactive setup wizard (recommended for first-time users)"),
            ("/exit, /quit", "Exit Flaco"),
            ("/clear", "Clear chat context and screen"),
            ("/reset", "Reset conversation history"),
            ("/status", "Show current status and statistics"),
            ("/init", "Create a CLAUDE.md codebase guide (and optional FLACO.md)"),
            ("/install-github-app", "Scaffold a Claude GitHub Actions workflow"),
            ("/context [summary]", "Show context status (and file contents unless 'summary')"),
            ("/costs", "Cost guidance for your current provider"),
            ("/model [name]", "Change the current model"),
            ("/models [number|name]", "List and switch between Ollama models"),
            ("/history", "Show conversation history"),
            ("/permissions [mode]", "Change permission mode (interactive/auto/headless)"),
            ("/todos", "Show current todo list"),
            ("/scan", "🌟 Scan project and show intelligence insights"),
            ("/project [action]", "🚀 Manage projects (list/create/switch/info)"),
            ("/git [action]", "🔄 Git operations (status/commit/push/history)"),
            ("/stats [period]", "📊 Show contribution stats (day/week/month/year)"),
            ("/recap [period]", "📈 Generate activity recap (day/week/month/year)"),
            ("/review <path>", "🔍 Comprehensive code review of a directory"),
            ("/refresh", "🔄 Check FLACO.md status"),
            ("/agent [action]", "🤖 Manage custom agents (create/list/switch/edit/delete/current)"),
            ("/actions", "⚡ Show available quick actions (#commands)"),
            ("/snippet [name|search|category]", "📋 Browse and insert code snippets"),
            ("/reset-config", "🔄 Reset configuration to defaults"),
            ("/check-update", "📦 Check for Flaco updates"),
            ("/run-update", "⬆️  Auto-update Flaco to latest version"),
            ("/install-github-app", "Set up Claude GitHub Actions workflow"),
        ]

        for cmd, desc in commands_help:
            table.add_row(cmd, desc)

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n[dim]Custom commands can be added in .flaco/commands/[/dim]")
        self.console.print("[cyan]💡 Tip:[/cyan] Type [bold]#[/bold] for quick actions (e.g., #Quick commit, #Fresh start)\n")

    def cmd_exit(self, args: str):
        """Exit Flaco"""
        self.console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
        exit(0)

    def cmd_clear(self, args: str):
        """Clear the screen"""
        self.agent.reset_conversation()
        os.system('clear' if os.name != 'nt' else 'cls')
        self.console.print("[green]✅ Chat context cleared[/green]")

    def cmd_reset(self, args: str):
        """Reset conversation history"""
        self.agent.reset_conversation()
        self.console.print("[green]✅ Conversation history reset[/green]")

    def cmd_status(self, args: str):
        """Show current status"""
        status_info = f"""
**Ollama Server:** {self.agent.llm.base_url}
**Model:** {self.agent.llm.model}
**Permission Mode:** {self.agent.permission_manager.mode.value}
**Conversation:** {self.agent.get_conversation_summary()}
**FLACO.md:** {'✅ Loaded' if self.agent.context_loader.has_context() else '❌ Not found'}
**Working Directory:** {os.getcwd()}
"""
        self.console.print(Panel(Markdown(status_info), title="Status", border_style="cyan"))

    def cmd_context(self, args: str):
        """Show FLACO.md context"""
        context_info = self.agent.get_context_info()
        usage_bar = self._build_usage_bar(context_info["percentage"])

        status_md = f"""**Messages:** {context_info['message_count']} / {context_info['limit']}  
**Remaining:** {context_info['remaining']}  
**Usage:** {context_info['percentage']}%  
`{usage_bar}`

**FLACO.md:** {"✅ " + context_info["context_path"] if context_info["has_context"] else "❌ Not found"}
"""
        self.console.print(Panel(Markdown(status_md), title="Conversation Context", border_style="cyan"))

        show_summary_only = args.strip().lower() == "summary"
        if context_info["has_context"] and not show_summary_only:
            context = self.agent.context_loader.load_context()
            if context:
                self.console.print(Panel(
                    Markdown(context),
                    title=f"FLACO.md ({context_info['context_path']})",
                    border_style="green"
                ))
        elif not context_info["has_context"]:
            self.console.print("[yellow]No FLACO.md found. Use /init --flaco to create one in this directory.[/yellow]")

    def cmd_init(self, args: str):
        """Create CLAUDE.md (and optionally FLACO.md) in the current directory"""
        force = "--force" in args
        include_flaco = "--flaco" in args
        cwd = Path(os.getcwd())

        claude_path = cwd / "CLAUDE.md"
        claude_template = self._load_template("CLAUDE.md.template", self._default_claude_template())

        if claude_path.exists() and not force:
            self.console.print(f"[yellow]ℹ️ CLAUDE.md already exists at {claude_path}[/yellow]")
            self.console.print("[dim]Re-run with --force to overwrite.[/dim]")
        else:
            claude_path.write_text(claude_template, encoding="utf-8")
            self.console.print(f"[green]✅ Created CLAUDE.md at {claude_path}[/green]")

        if include_flaco:
            template_path = None
            repo_template = Path(os.getcwd()) / "docs" / "FLACO.md.template"
            if repo_template.exists():
                template_path = str(repo_template)

            result = self.agent.create_context_file(
                target_dir=os.getcwd(),
                template_path=template_path,
                overwrite=force
            )

            if result.get("exists") and not force:
                self.console.print(f"[yellow]ℹ️ FLACO.md already exists at {result['path']}[/yellow]")
            elif result.get("success"):
                self.console.print(f"[green]✅ Created FLACO.md at {result['path']}[/green]")

    def cmd_install_github_app(self, args: str):
        """Scaffold a Claude GitHub Actions workflow"""
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)
        workflow_path = workflows_dir / "claude-github-app.yml"

        if workflow_path.exists() and "--force" not in args:
            self.console.print(f"[yellow]ℹ️ Workflow already exists at {workflow_path}[/yellow]")
            self.console.print("[dim]Re-run with --force to overwrite.[/dim]")
            return

        workflow_content = self._claude_workflow_template()
        workflow_path.write_text(workflow_content, encoding="utf-8")
        self.console.print(f"[green]✅ Added Claude GitHub Actions workflow at {workflow_path}[/green]")
        self.console.print("[dim]Set secrets CLAUDE_API_KEY and optional CLAUDE_MODEL in repo settings before enabling.[/dim]")

    def cmd_costs(self, args: str):
        """Show cost guidance"""
        cost_message = (
            "💰 **Cost overview**\n\n"
            "Running on local models (Ollama) — API cost: **$0**. "
            "Performance depends on your hardware.\n\n"
            "Flaco keeps work local by default; no usage metering."
        )
        self.console.print(Markdown(cost_message))

    def cmd_model(self, args: str):
        """Change the current model"""
        if not args:
            self.console.print(f"[cyan]Current model:[/cyan] {self.agent.llm.model}")
            return

        self.agent.llm.model = args.strip()
        self.console.print(f"[green]✅ Model changed to:[/green] {args.strip()}")

    def cmd_models(self, args: str):
        """List available models and optionally switch"""
        try:
            models = self.agent.llm.list_models()
            if not models:
                self.console.print("[yellow]No models found[/yellow]")
                return

            # If user provided a model name or number, switch to it
            if args.strip():
                model_arg = args.strip()

                # Check if it's a number (index)
                if model_arg.isdigit():
                    idx = int(model_arg) - 1
                    if 0 <= idx < len(models):
                        selected_model = models[idx].get("name")
                        self.agent.llm.model = selected_model
                        self.console.print(f"[green]✅ Switched to:[/green] {selected_model}")
                        return
                    else:
                        self.console.print(f"[red]Invalid model number. Choose 1-{len(models)}[/red]")
                        return
                else:
                    # Try to find by name
                    matching_model = next((m for m in models if m.get("name") == model_arg), None)
                    if matching_model:
                        self.agent.llm.model = model_arg
                        self.console.print(f"[green]✅ Switched to:[/green] {model_arg}")
                        return
                    else:
                        self.console.print(f"[red]Model not found: {model_arg}[/red]")
                        self.console.print("[dim]Run /models without arguments to see available models[/dim]")
                        return

            # Display models table with current model highlighted
            current_model = self.agent.llm.model

            table = Table(title="Available Ollama Models", show_header=True)
            table.add_column("#", style="dim", width=4)
            table.add_column("Name", style="cyan")
            table.add_column("Size", style="white")
            table.add_column("Modified", style="dim")
            table.add_column("Active", style="green", justify="center")

            for idx, model in enumerate(models, 1):
                name = model.get("name", "unknown")
                size = self._format_size(model.get("size", 0))
                modified = model.get("modified_at", "unknown")[:10]
                is_active = "✓" if name == current_model else ""
                table.add_row(str(idx), name, size, modified, is_active)

            self.console.print("\n")
            self.console.print(table)
            self.console.print("\n[dim]Usage: /models <number|name> to switch models[/dim]")
            self.console.print(f"[dim]Current model: [cyan]{current_model}[/cyan][/dim]\n")

        except Exception as e:
            self.console.print(f"[red]Error listing models: {str(e)}[/red]")

    def cmd_history(self, args: str):
        """Show conversation history"""
        if not self.agent.messages:
            self.console.print("[yellow]No conversation history[/yellow]")
            return

        for i, msg in enumerate(self.agent.messages, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            if role == "user":
                self.console.print(f"\n[bold cyan]User (#{i}):[/bold cyan]")
            elif role == "assistant":
                self.console.print(f"\n[bold green]Assistant (#{i}):[/bold green]")
            elif role == "tool":
                self.console.print(f"\n[bold yellow]Tool Result (#{i}):[/bold yellow]")

            if content:
                # Truncate long messages
                display_content = content[:500] + "..." if len(content) > 500 else content
                self.console.print(display_content)

    def cmd_permissions(self, args: str):
        """Change permission mode"""
        if not args:
            self.console.print(f"[cyan]Current permission mode:[/cyan] {self.agent.permission_manager.mode.value}")
            self.console.print("\n[dim]Available modes: interactive, auto, headless[/dim]")
            return

        mode_map = {
            "interactive": PermissionMode.INTERACTIVE,
            "auto": PermissionMode.AUTO_APPROVE,
            "headless": PermissionMode.HEADLESS
        }

        mode_str = args.strip().lower()
        if mode_str in mode_map:
            self.agent.set_permission_mode(mode_map[mode_str])
            self.console.print(f"[green]✅ Permission mode changed to:[/green] {mode_str}")
        else:
            self.console.print(f"[red]Invalid mode: {mode_str}[/red]")
            self.console.print("[yellow]Available modes: interactive, auto, headless[/yellow]")

    def cmd_todos(self, args: str):
        """Show current todo list"""
        todo_file = os.path.join(os.getcwd(), ".flaco_todos.json")
        if not os.path.exists(todo_file):
            self.console.print("[yellow]No active todo list[/yellow]")
            return

        with open(todo_file, 'r') as f:
            todos = json.load(f)

        if not todos:
            self.console.print("[yellow]Todo list is empty[/yellow]")
            return

        table = Table(title="Current Tasks", show_header=True)
        table.add_column("#", style="dim")
        table.add_column("Status", style="white")
        table.add_column("Task", style="cyan")

        status_icons = {
            "pending": "⏳",
            "in_progress": "🔄",
            "completed": "✅"
        }

        for i, todo in enumerate(todos, 1):
            icon = status_icons.get(todo["status"], "❓")
            table.add_row(str(i), icon, todo["content"])

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

    def cmd_scan(self, args: str):
        """Scan project and show intelligence insights"""
        from ..intelligence import ProjectScanner

        self.console.print("\n[cyan]🔍 Scanning project...[/cyan]\n")

        scanner = ProjectScanner()
        try:
            insight = scanner.scan()

            # Health score with color
            health_color = "green" if insight.health_score >= 80 else "yellow" if insight.health_score >= 60 else "red"

            # Create summary
            summary = f"""
## 📊 Project Intelligence Report

**Type:** {insight.project_type.value.upper()}
**Framework:** {insight.framework or 'None detected'}
**Languages:** {', '.join(insight.languages)}
**Health Score:** [{health_color}]{insight.health_score:.0f}/100[/{health_color}]

### 📈 Statistics
- **Files:** {insight.file_count:,} code files
- **Lines:** {insight.total_lines:,} lines of code
- **Dependencies:** {len(insight.dependencies)} packages

### 🔧 Configuration
- **Entry Points:** {', '.join(insight.entry_points) if insight.entry_points else 'Not detected'}
- **Test Framework:** {insight.test_framework or '❌ None'}
- **CI/CD:** {'✅ Configured' if insight.has_ci else '❌ Not configured'}
- **Docker:** {'✅ Yes' if insight.has_docker else '❌ No'}
- **Tests:** {'✅ Yes' if insight.has_tests else '❌ No tests found'}

### 💡 Suggestions
"""
            if insight.suggestions:
                for suggestion in insight.suggestions:
                    summary += f"- {suggestion}\n"
            else:
                summary += "- ✨ Project looks great! No suggestions at this time.\n"

            self.console.print(Panel(
                Markdown(summary),
                title="🌟 Project Intelligence",
                border_style="cyan"
            ))

        except Exception as e:
            self.console.print(f"[red]Error scanning project: {str(e)}[/red]")

    def cmd_project(self, args: str):
        """Manage projects"""
        from ..projects import ProjectManager

        pm = ProjectManager()

        if not args or args == "list":
            projects = pm.list_projects()

            if not projects:
                self.console.print("[yellow]No projects yet. Create one with: /project create <name>[/yellow]")
                return

            table = Table(title="Flaco Projects", show_header=True)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="white")
            table.add_column("Path", style="dim")
            table.add_column("Last Accessed", style="green")

            for proj in projects:
                current_marker = "→ " if pm.current_project and pm.current_project.name == proj.name else ""
                last_accessed = proj.last_accessed.split('T')[0] if proj.last_accessed else "N/A"
                table.add_row(
                    current_marker + proj.name,
                    proj.project_type,
                    proj.path[:40] + "..." if len(proj.path) > 40 else proj.path,
                    last_accessed
                )

            self.console.print("\n")
            self.console.print(table)
            self.console.print("\n[dim]Commands: /project create/switch/info/delete[/dim]\n")

        elif args.startswith("create"):
            parts = args.split(maxsplit=1)
            if len(parts) < 2:
                self.console.print("[red]Usage: /project create <name>[/red]")
                return

            name = parts[1]
            path = os.path.join(os.getcwd(), name)

            try:
                project = pm.create_project(name, path)
                self.console.print(f"[green]✅ Created project: {name}[/green]")
                self.console.print(f"[dim]Path: {path}[/dim]")
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

        elif args.startswith("switch"):
            parts = args.split(maxsplit=1)
            if len(parts) < 2:
                self.console.print("[red]Usage: /project switch <name>[/red]")
                return

            name = parts[1]
            try:
                project = pm.switch_project(name)
                self.console.print(f"[green]✅ Switched to project: {name}[/green]")
                self.console.print(f"[dim]Path: {project.path}[/dim]")
            except Exception as e:
                self.console.print(f"[red]Error: {str(e)}[/red]")

        elif args.startswith("info"):
            if not pm.current_project:
                self.console.print("[yellow]No active project[/yellow]")
                return

            proj = pm.current_project
            stats = pm.get_project_stats(proj.name)

            info = f"""
**Name:** {proj.name}
**Type:** {proj.project_type}
**Description:** {proj.description or 'No description'}
**Path:** {proj.path}

**Statistics:**
- Files: {stats['files']:,}
- Directories: {stats['directories']:,}
- Size: {stats['size_mb']} MB

**Settings:**
- Git Enabled: {'✅' if proj.git_enabled else '❌'}
- Auto Commit: {'✅' if proj.auto_commit else '❌'}

**Created:** {proj.created_at.split('T')[0]}
**Last Accessed:** {proj.last_accessed.split('T')[0]}
"""
            self.console.print(Panel(Markdown(info), title=f"📁 {proj.name}", border_style="cyan"))

        else:
            self.console.print("[yellow]Available actions: list, create, switch, info[/yellow]")

    def cmd_git(self, args: str):
        """Git operations"""
        from ..projects import GitAutoVersioning

        git = GitAutoVersioning()

        if not git.is_git_repo():
            self.console.print("[yellow]Not a git repository. Initialize with: git init[/yellow]")
            return

        if not args or args == "status":
            changes = git.get_changes()
            stats = git.get_repo_stats()

            self.console.print(f"\n[cyan]📊 Git Status[/cyan]")
            self.console.print(f"Branch: [green]{stats['branch']}[/green]")
            self.console.print(f"Total Commits: {stats['total_commits']}")
            self.console.print(f"Uncommitted Changes: {stats['uncommitted_changes']}")

            if changes:
                self.console.print("\n[yellow]Changes:[/yellow]")
                for change in changes[:10]:
                    icon = "+" if change.change_type == "added" else "~" if change.change_type == "modified" else "-"
                    self.console.print(f"  {icon} {change.file_path}")

                if len(changes) > 10:
                    self.console.print(f"  ... and {len(changes) - 10} more")

        elif args.startswith("commit"):
            parts = args.split(maxsplit=1)
            message = parts[1] if len(parts) > 1 else None

            success, msg = git.auto_commit(message)
            if success:
                self.console.print(f"[green]✅ {msg}[/green]")
            else:
                self.console.print(f"[red]❌ {msg}[/red]")

        elif args == "push":
            success, msg = git.auto_push()
            if success:
                self.console.print(f"[green]✅ {msg}[/green]")
            else:
                self.console.print(f"[red]❌ {msg}[/red]")

        elif args == "history":
            commits = git.get_commit_history(limit=10)

            if not commits:
                self.console.print("[yellow]No commits yet[/yellow]")
                return

            table = Table(title="Recent Commits", show_header=True)
            table.add_column("Hash", style="cyan")
            table.add_column("Message", style="white")
            table.add_column("Author", style="green")
            table.add_column("Date", style="dim")

            for commit in commits:
                table.add_row(commit.hash, commit.message[:50], commit.author, commit.date)

            self.console.print("\n")
            self.console.print(table)
            self.console.print("\n")

        else:
            self.console.print("[yellow]Available actions: status, commit, push, history[/yellow]")

    def cmd_stats(self, args: str):
        """Show contribution statistics"""
        from ..analytics import ContributionTracker

        tracker = ContributionTracker()
        period = args.strip() if args else "week"

        if period not in ["day", "week", "month", "year"]:
            self.console.print("[red]Invalid period. Use: day, week, month, or year[/red]")
            return

        stats = tracker.get_stats(period)

        period_name = {
            "day": "Today",
            "week": "This Week",
            "month": "This Month",
            "year": "This Year"
        }.get(period)

        info = f"""
## 📊 {period_name}'s Statistics

**Total Activities:** {stats.total_activities:,}

**Breakdown:**
- 💬 Chat Messages: {stats.chat_messages:,}
- 📝 Files Created: {stats.files_created:,}
- ✏️  Files Modified: {stats.files_modified:,}
- 🔄 Git Commits: {stats.git_commits:,}
- 🔧 Tool Executions: {stats.tool_executions:,}
- 🌟 Agent Swarms: {stats.agent_swarms:,}
"""

        if stats.streak_days > 0 and period == "day":
            info += f"\n**🔥 Current Streak:** {stats.streak_days} days!"

        if stats.total_tokens > 0:
            info += f"\n**🎫 Tokens Used:** {stats.total_tokens:,}"

        if stats.projects_worked_on:
            info += f"\n\n**📁 Active Projects:** {', '.join(stats.projects_worked_on)}"

        self.console.print(Panel(Markdown(info), title="Statistics", border_style="cyan"))

    def cmd_recap(self, args: str):
        """Generate activity recap"""
        from ..analytics import ContributionTracker

        tracker = ContributionTracker()
        period = args.strip() if args else "week"

        if period not in ["day", "week", "month", "year"]:
            self.console.print("[red]Invalid period. Use: day, week, month, or year[/red]")
            return

        # Show contribution graph for year
        if period == "year":
            self.console.print("\n[cyan]" + tracker.generate_contribution_graph() + "[/cyan]\n")

        # Show recap
        recap = tracker.generate_recap(period)
        self.console.print(Panel(Markdown(recap), title="Activity Recap", border_style="cyan"))

    def _build_usage_bar(self, percentage: int) -> str:
        """Return a simple usage bar for context stats."""
        capped = max(0, min(percentage, 100))
        filled_blocks = int((capped / 100) * 20)
        return "█" * filled_blocks + "░" * (20 - filled_blocks)

    def _load_template(self, filename: str, default: str) -> str:
        """Load a template from docs if present, else return default."""
        repo_root = Path(__file__).resolve().parents[2]
        template_path = repo_root / "docs" / filename
        if template_path.exists():
            try:
                return template_path.read_text(encoding="utf-8")
            except Exception:
                return default
        return default

    def _default_claude_template(self) -> str:
        """Fallback CLAUDE.md template."""
        return """# CLAUDE.md

This file guides Claude (and other agents) when working on this codebase.

## Project Overview
- App: Flaco AI (CLI + macOS desktop)
- Focus: Local-first AI coding assistant powered by Ollama
- Key tech: Python CLI (`flaco/`), Electron UI (`flaco-macos/`)

## How to Run
- CLI: `flaco` (after `pip install -e .` in venv)
- Desktop: `cd flaco-macos && npm install && npm start`

## Build & Test
- CLI tests: `pytest`
- Desktop tests: `npm test`
- Desktop build: `npm run build:quiet`

## Conventions
- Python: PEP 8, 4-space indent, type hints where useful
- JS: CommonJS modules, camelCase, renderer-safe code stays in `preload.js`
- Docs: keep customer-facing guides in `docs/guides/`; owner/internal in `docs/internal/`

## Context Files
- `FLACO.md` for project-specific context (optional)
- `CLAUDE.md` (this file) for repo-wide guidance
"""

    def _claude_workflow_template(self) -> str:
        """GitHub Actions workflow scaffold for Claude GitHub App."""
        return """name: Claude GitHub App

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Claude Review (placeholder)
        run: |
          echo "Configure Claude GitHub App here."
          echo "Set secrets CLAUDE_API_KEY and optional CLAUDE_MODEL."
          echo "Replace this step with the official Claude GitHub App action once available."
"""

    def _format_size(self, size_bytes: int) -> str:
        """Format bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def cmd_review(self, args: str):
        """Perform comprehensive code review of a directory"""
        from pathlib import Path
        from rich.prompt import Prompt, Confirm
        from rich.table import Table

        # Interactive prompt if no args provided
        if not args:
            self.console.print(f"\n[{self.theme_color}]🔍 Code Review[/{self.theme_color}]\n")
            self.console.print("[dim]Enter the path to the directory you want to review[/dim]")
            self.console.print("[dim]Example: /Users/me/project or ~/Documents/my-code[/dim]\n")

            path_input = Prompt.ask("📁 Path to review", default=".")
            if not path_input:
                self.console.print("[yellow]⚠️  Review cancelled[/yellow]\n")
                return
            args = path_input

        # Validate path
        review_path = Path(args.strip()).expanduser().resolve()
        if not review_path.exists():
            self.console.print(f"[red]❌ Error: Path does not exist: {review_path}[/red]\n")
            return

        if not review_path.is_dir():
            self.console.print(f"[red]❌ Error: Path must be a directory: {review_path}[/red]\n")
            return

        # Step 1: Find Python files using agent's Glob tool
        self.console.print(f"\n[cyan]📂 Finding Python files in {review_path}...[/cyan]")
        glob_result = self.agent.tools["Glob"].execute(pattern="**/*.py", path=str(review_path))

        if glob_result.status.value != "success":
            self.console.print(f"[red]❌ Failed to find files: {glob_result.error}[/red]\n")
            return

        # Parse file paths
        all_files = [line.strip() for line in glob_result.output.strip().split('\n') if line.strip()]

        if not all_files:
            self.console.print("[yellow]⚠️  No Python files found in the specified path[/yellow]\n")
            return

        # Track reviewed files across iterations
        reviewed_files = []

        # Main review loop - allows continuing with more files
        while True:
            # Get remaining files
            remaining_files = [f for f in all_files if f not in reviewed_files]

            if not remaining_files:
                self.console.print(f"\n[green]✅ All files have been reviewed![/green]\n")
                break

            # Display file selection
            self.console.print(f"\n[{self.theme_color}]📂 Found {len(remaining_files)} file(s) to review[/{self.theme_color}]")

            if len(reviewed_files) > 0:
                self.console.print(f"[dim]({len(reviewed_files)} already reviewed)[/dim]")

            self.console.print()

            # Show files in a table
            table = Table(show_header=True, box=None, padding=(0, 1))
            table.add_column("#", style="dim", width=4)
            table.add_column("File", style="cyan")
            table.add_column("Lines", style="dim", justify="right", width=8)

            file_info = []
            for idx, file_path in enumerate(remaining_files, 1):
                # Count lines
                try:
                    read_result = self.agent.tools["Read"].execute(file_path=file_path)
                    line_count = len(read_result.output.split('\n')) if read_result.status.value == "success" else 0
                except:
                    line_count = 0

                file_info.append({
                    "path": file_path,
                    "lines": line_count
                })

                # Shorten path for display
                display_path = Path(file_path).name
                if len(str(Path(file_path).parent)) > 40:
                    parent_parts = str(Path(file_path).parent).split('/')
                    display_path = f".../{'/'.join(parent_parts[-2:])}/{display_path}"
                else:
                    display_path = str(Path(file_path).relative_to(review_path))

                table.add_row(str(idx), display_path, f"{line_count:,}")

            self.console.print(table)

            # Get user selection
            self.console.print(f"\n[dim]Selection format:[/dim]")
            self.console.print(f"[dim]  • Individual: 1,3,5[/dim]")
            self.console.print(f"[dim]  • Range: 1-10[/dim]")
            self.console.print(f"[dim]  • All: all[/dim]")
            self.console.print(f"[dim]  • Default: Press Enter for first 10[/dim]\n")

            selection = Prompt.ask(
                "Select files to review",
                default="1-10" if len(remaining_files) >= 10 else f"1-{len(remaining_files)}"
            )

            # Parse selection
            selected_indices = self._parse_file_selection(selection, len(remaining_files))

            if not selected_indices:
                self.console.print("[yellow]⚠️  No files selected[/yellow]\n")
                break

            files_to_review = [file_info[i-1] for i in selected_indices]
            total_lines = sum(f['lines'] for f in files_to_review)

            self.console.print(f"\n[green]✅ Selected {len(files_to_review)} file(s) ({total_lines:,} lines total)[/green]\n")

            # Step 2: Read selected files
            self.console.print("[cyan]📖 Reading files...[/cyan]")
            file_contents = []

            for file_item in files_to_review:
                file_path = file_item['path']
                try:
                    read_result = self.agent.tools["Read"].execute(file_path=file_path)
                    if read_result.status.value == "success":
                        file_contents.append({
                            "path": file_path,
                            "content": read_result.output
                        })
                        self.console.print(f"[dim]  ✓ {Path(file_path).name}[/dim]")
                        reviewed_files.append(file_path)  # Track as reviewed
                except Exception as e:
                    self.console.print(f"[yellow]  ⚠️  Skipped {file_path}: {str(e)}[/yellow]")

            if not file_contents:
                self.console.print("[red]❌ Failed to read any files[/red]\n")
                break

            self.console.print(f"[green]✅ Read {len(file_contents)} file(s) successfully[/green]\n")

            # Step 3: Perform code review using the agent
            self.console.print("[cyan]🔍 Analyzing code quality, bugs, security, performance...[/cyan]\n")

            # Build comprehensive review prompt
            review_prompt = f"""I need you to perform a comprehensive code review of the following Python files from: {review_path}

Please analyze these {len(file_contents)} files and provide a detailed review covering:
1. **Code Quality**: Maintainability, readability, code smells
2. **Bugs & Issues**: Logic errors, edge cases, potential runtime errors
3. **Security**: Vulnerabilities, OWASP concerns, input validation
4. **Performance**: Inefficiencies, optimization opportunities
5. **Best Practices**: Design patterns, Pythonic code, conventions

For each issue found, provide:
- File path and line number
- Specific code example
- Explanation of the issue
- Recommended fix with code snippet

Files to review:
"""

            for fc in file_contents:
                review_prompt += f"\n### File: {fc['path']}\n```python\n{fc['content']}\n```\n"

            # Execute review through agent
            from rich.spinner import Spinner
            from rich.live import Live

            spinner = Spinner("dots", text="Jony - Code Reviewer: Scrutinizing the details...", style=f"bold {self.theme_color}")

            with Live(spinner, console=self.console, refresh_per_second=10, transient=True) as live:
                response, metrics = self.agent.chat(review_prompt)

            # Display review results
            self.console.print("\n")
            self.console.print(Panel(
                Markdown(response),
                title=f"🔍 Code Review Results",
                border_style=self.theme_color,
                padding=(1, 2)
            ))

            # Display metrics
            self.console.print(f"\n[dim]📊 Review completed in {metrics.get('total_time', 0):.2f}s | "
                              f"Tokens: {metrics.get('total_tokens', 0)} | "
                              f"Files analyzed: {len(file_contents)}[/dim]\n")

            # Check if there are more files to review
            remaining_count = len([f for f in all_files if f not in reviewed_files])

            if remaining_count > 0:
                self.console.print(f"[{self.theme_color}]📂 {remaining_count} file(s) remaining[/{self.theme_color}]")
                continue_review = Confirm.ask("Continue reviewing?", default=True)

                if not continue_review:
                    self.console.print(f"\n[green]✅ Review session complete! Reviewed {len(reviewed_files)} file(s)[/green]\n")
                    break
            else:
                self.console.print(f"\n[green]✅ All files reviewed![/green]\n")
                break

    def _parse_file_selection(self, selection: str, max_files: int) -> list:
        """Parse file selection input (e.g., '1,3,5-10,15' or 'all')"""
        selection = selection.strip().lower()

        if selection == 'all':
            return list(range(1, max_files + 1))

        selected = set()
        parts = selection.split(',')

        for part in parts:
            part = part.strip()
            if '-' in part:
                # Handle range (e.g., '1-10')
                try:
                    start, end = part.split('-')
                    start, end = int(start.strip()), int(end.strip())
                    selected.update(range(start, min(end + 1, max_files + 1)))
                except:
                    continue
            else:
                # Handle individual number
                try:
                    num = int(part)
                    if 1 <= num <= max_files:
                        selected.add(num)
                except:
                    continue

        return sorted(list(selected))

    def cmd_refresh(self, args: str):
        """Check flaco.md status - matches desktop refresh button"""
        if self.agent.context_loader.has_context():
            content = self.agent.context_loader.load_context()
            preview = content[:150]
            if len(content) > 150:
                preview += "..."

            info = f"""✅ **FLACO.md** found and loaded!

**Preview:**
{preview}

**Full context:** {len(content)} characters
**Path:** {self.agent.context_loader.get_context_path()}

The context will be included in all your messages."""

            self.console.print(Panel(Markdown(info), title="🔄 FLACO.md Status", border_style="green"))
        else:
            info = """ℹ️  No **FLACO.md** file found in the current directory.

Create a `FLACO.md` file in your project directory to add persistent context to all conversations.

**Tip:** Run `/init` to create a template FLACO.md file."""

            self.console.print(Panel(Markdown(info), title="🔄 FLACO.md Status", border_style="yellow"))

    def cmd_check_update(self, args: str):
        """Check for Flaco updates"""
        from ..utils.update_checker import UpdateChecker
        from .. import __version__

        self.console.print(f"\n[{self.theme_color}]📦 Checking for updates...[/{self.theme_color}]\n")

        # Force a fresh check by clearing cache
        if UpdateChecker.CACHE_FILE.exists():
            UpdateChecker.CACHE_FILE.unlink()

        has_update, latest_version, summary = UpdateChecker.check_for_updates(__version__)

        if has_update and latest_version:
            # Update available
            message = f"""📦 **Update Available!**

**Current version:** v{__version__}
**Latest version:** v{latest_version}

**What's new:**
{summary if summary else "Bug fixes and improvements"}

**To update:**
```bash
pipx upgrade flaco-ai
```

After updating, restart Flaco to use the new version."""

            self.console.print(Panel(
                Markdown(message),
                title="⬆️  Update Available",
                border_style="yellow",
                padding=(1, 2)
            ))
        else:
            # Already on latest
            message = f"""✅ **You're up to date!**

**Current version:** v{__version__}

You're running the latest version of Flaco."""

            self.console.print(Panel(
                Markdown(message),
                title="📦 Update Check",
                border_style="green",
                padding=(1, 2)
            ))

        self.console.print()

    def cmd_run_update(self, args: str):
        """Automatically update Flaco to the latest version"""
        from ..utils.update_checker import UpdateChecker
        from .. import __version__
        import subprocess

        self.console.print(f"\n[{self.theme_color}]⬆️  Auto-Update[/{self.theme_color}]\n")

        # Check for updates
        self.console.print("[dim]Checking for updates...[/dim]")

        # Force fresh check
        if UpdateChecker.CACHE_FILE.exists():
            UpdateChecker.CACHE_FILE.unlink()

        has_update, latest_version, summary = UpdateChecker.check_for_updates(__version__)

        if not has_update:
            self.console.print(f"\n[green]✅ You're already on the latest version (v{__version__})[/green]\n")
            return

        # Show what will be updated
        self.console.print(f"\n[yellow]📦 Update available: v{__version__} → v{latest_version}[/yellow]")
        if summary:
            self.console.print(f"[dim]{summary}[/dim]\n")

        # Confirm with user
        from rich.prompt import Confirm
        if not Confirm.ask("Proceed with update?", default=True):
            self.console.print("[yellow]⚠️  Update cancelled[/yellow]\n")
            return

        # Run the update
        self.console.print(f"\n[{self.theme_color}]Running: pipx upgrade flaco-ai[/{self.theme_color}]\n")

        try:
            # Run pipx upgrade
            result = subprocess.run(
                ["pipx", "upgrade", "flaco-ai"],
                capture_output=True,
                text=True,
                timeout=120
            )

            # Show output
            if result.stdout:
                self.console.print(result.stdout)

            if result.returncode == 0:
                self.console.print(f"\n[green]✅ Successfully updated to v{latest_version}![/green]")
                self.console.print(f"[yellow]⚠️  Please restart Flaco to use the new version[/yellow]")
                self.console.print(f"[dim]Tip: Type /exit or /quit to close, then run flaco.cli again[/dim]\n")
            else:
                self.console.print(f"\n[red]❌ Update failed[/red]")
                if result.stderr:
                    self.console.print(f"[red]{result.stderr}[/red]")
                self.console.print(f"\n[yellow]Try running manually: pipx upgrade flaco-ai[/yellow]\n")

        except subprocess.TimeoutExpired:
            self.console.print(f"\n[red]❌ Update timed out[/red]")
            self.console.print(f"[yellow]Try running manually: pipx upgrade flaco-ai[/yellow]\n")
        except FileNotFoundError:
            self.console.print(f"\n[red]❌ pipx not found[/red]")
            self.console.print(f"[yellow]Please install pipx first: https://pipx.pypa.io/[/yellow]\n")
        except Exception as e:
            self.console.print(f"\n[red]❌ Update failed: {str(e)}[/red]")
            self.console.print(f"[yellow]Try running manually: pipx upgrade flaco-ai[/yellow]\n")

    def cmd_agent(self, args: str):
        """Manage custom AI agents - matches desktop functionality"""
        parts = args.split(maxsplit=1) if args else []
        action = parts[0].lower() if parts else "list"
        action_args = parts[1] if len(parts) > 1 else ""

        if action == "create":
            agent = self.agent_manager.create_agent_interactive()
            self.console.print(f"\n[green]✓ Created agent: {agent.emoji} {agent.name}[/green]")
            self.console.print(f"[dim]ID: {agent.id}[/dim]\n")

        elif action == "list":
            self.agent_manager.list_agents(show_table=True)

        elif action == "switch":
            if not action_args:
                self.console.print("[red]Usage: /agent switch <name or id>[/red]")
                return

            agent = self.agent_manager.set_current_agent(action_args)
            if agent:
                self.console.print(f"\n[green]✓ Switched to {agent.emoji} {agent.name}[/green]")
                self.console.print(f"[dim]{agent.description}[/dim]\n")
            else:
                self.console.print(f"[red]Agent not found: {action_args}[/red]")
                self.console.print("[yellow]Run /agent list to see available agents[/yellow]")

        elif action == "current":
            current = self.agent_manager.get_current_agent()
            if current:
                info = f"""**{current.emoji} {current.name}**

{current.description}

**Type:** {'Default' if current.is_default else 'Custom'}
**ID:** {current.id}"""
                self.console.print(Panel(Markdown(info), title="Current Agent", border_style="cyan"))
            else:
                self.console.print("[yellow]No agent currently selected[/yellow]")
                self.console.print("[dim]Run /agent switch <name> to select an agent[/dim]")

        elif action == "edit":
            if not action_args:
                self.console.print("[red]Usage: /agent edit <id>[/red]")
                return

            agent = self.agent_manager.get_agent(action_args)
            if not agent:
                self.console.print(f"[red]Agent not found: {action_args}[/red]")
                return

            if agent.is_default:
                self.console.print("[red]Cannot edit default agents[/red]")
                return

            self.console.print(f"\n[cyan]Editing: {agent.emoji} {agent.name}[/cyan]")
            self.console.print("[dim]Leave blank to keep current value[/dim]\n")

            new_emoji = Prompt.ask("Emoji", default=agent.emoji)
            new_name = Prompt.ask("Name", default=agent.name)
            new_desc = Prompt.ask("Description", default=agent.description)

            updated = self.agent_manager.update_agent(
                agent.id,
                emoji=new_emoji if new_emoji != agent.emoji else None,
                name=new_name if new_name != agent.name else None,
                description=new_desc if new_desc != agent.description else None
            )

            if updated:
                self.console.print(f"\n[green]✓ Updated {updated.emoji} {updated.name}[/green]")
            else:
                self.console.print("[red]Failed to update agent[/red]")

        elif action == "delete":
            if not action_args:
                self.console.print("[red]Usage: /agent delete <id>[/red]")
                return

            agent = self.agent_manager.get_agent(action_args)
            if not agent:
                self.console.print(f"[red]Agent not found: {action_args}[/red]")
                return

            if agent.is_default:
                self.console.print("[red]Cannot delete default agents[/red]")
                return

            if Confirm.ask(f"Delete {agent.emoji} {agent.name}?", default=False):
                if self.agent_manager.delete_agent(agent.id):
                    self.console.print(f"[green]✓ Deleted {agent.emoji} {agent.name}[/green]")
                else:
                    self.console.print("[red]Failed to delete agent[/red]")
            else:
                self.console.print("[yellow]Cancelled[/yellow]")

        else:
            help_text = """**Agent Commands:**

• `/agent create` - Create a new custom agent interactively
• `/agent list` - Show all agents (default + custom)
• `/agent switch <name>` - Switch to a different agent
• `/agent current` - Show currently active agent
• `/agent edit <id>` - Edit a custom agent
• `/agent delete <id>` - Delete a custom agent

**Examples:**
```
/agent create
/agent switch "Python Expert"
/agent switch default_python
/agent current
/agent edit agent_abc123
/agent delete agent_abc123
```"""
            self.console.print(Panel(Markdown(help_text), title="🤖 Agent Management", border_style="cyan"))

    def cmd_actions(self, args: str):
        """Show available quick actions (#commands)"""
        table = Table(title="⚡ Quick Actions", show_header=True)
        table.add_column("Quick Action", style="cyan")
        table.add_column("Description", style="white")

        for action in self.quick_actions.list_actions():
            table.add_row(f"#{action.name}", action.description)

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n[dim]Type # followed by the action name to run it (e.g., #Quick commit)[/dim]")
        self.console.print("[dim]Quick actions are multi-step workflows that combine multiple commands.[/dim]\n")

    def cmd_setup(self, args: str):
        """Interactive setup wizard for Flaco"""
        self.console.print("\n")
        self.console.print("╔═══════════════════════════════════════╗", style=f"bold {self.theme_color}")
        self.console.print("║                                       ║", style=f"bold {self.theme_color}")
        self.console.print("║       🦙 FLACO SETUP WIZARD           ║", style=f"bold {self.theme_color}")
        self.console.print("║                                       ║", style=f"bold {self.theme_color}")
        self.console.print("╚═══════════════════════════════════════╝", style=f"bold {self.theme_color}")
        self.console.print("\n")

        # Load or create user config
        user_config = UserConfig()

        # Step 1: Configure Ollama connection
        self.console.print("[bold]Step 1:[/bold] Configure Ollama connection")
        self.console.print(f"[dim]Current: {user_config.ollama_url}[/dim]")

        ollama_input = Prompt.ask(
            "Enter Ollama host:port (http:// will be added automatically)",
            default=user_config.ollama_url.replace("http://", "").replace("https://", "")
        )
        user_config.ollama_url = ollama_input
        user_config.save()

        # Update agent's Ollama URL
        self.agent.llm.base_url = user_config.ollama_url

        # Step 2: Check Ollama connection and select model
        self.console.print("\n[bold]Step 2:[/bold] Testing Ollama connection...")
        if not self.agent.llm.test_connection():
            self.console.print(f"[red]❌ Cannot connect to Ollama at {self.agent.llm.base_url}[/red]")
            self.console.print("[yellow]Please ensure Ollama is running and try again.[/yellow]")
            return

        self.console.print(f"[green]✅ Connected to Ollama[/green] at {self.agent.llm.base_url}")

        # Fetch available models
        try:
            models = self.agent.llm.list_models()
            if models:
                self.console.print(f"\n[bold]Found {len(models)} models:[/bold]")

                # Display models
                for i, model in enumerate(models, 1):
                    name = model.get("name", "unknown")
                    size = self._format_size(model.get("size", 0))
                    marker = "[cyan]✓[/cyan]" if name == user_config.ollama_model else " "
                    self.console.print(f"  {i}. {marker} {name} ({size})")

                # Let user select
                model_choice = Prompt.ask(
                    f"\nSelect model (1-{len(models)} or enter name)",
                    default=user_config.ollama_model
                )

                # Handle numeric choice
                if model_choice.isdigit() and 1 <= int(model_choice) <= len(models):
                    selected_model = models[int(model_choice) - 1].get("name")
                else:
                    selected_model = model_choice

                user_config.ollama_model = selected_model
                user_config.save()
                self.agent.llm.model = selected_model
                self.console.print(f"[green]✅ Model set to:[/green] {selected_model}")
            else:
                self.console.print("[yellow]No models found. Using default.[/yellow]")
        except Exception as e:
            self.console.print(f"[yellow]Could not fetch models: {str(e)}[/yellow]")
            self.console.print(f"[dim]Using current model: {self.agent.llm.model}[/dim]")

        # Step 3: Choose theme color
        self.console.print("\n[bold]Step 3:[/bold] Choose your theme color")
        self.console.print(f"[dim]Current: {user_config.theme_color}[/dim]")

        color_options = [
            ("cyan", "Cyan (Default) - Cool and professional"),
            ("green", "Green - Fresh and vibrant"),
            ("blue", "Blue - Calm and trustworthy"),
            ("magenta", "Magenta - Bold and creative"),
            ("yellow", "Yellow - Bright and energetic"),
            ("white", "White - Clean and minimal")
        ]

        self.console.print("\n[bold]Available colors:[/bold]")
        for i, (color, desc) in enumerate(color_options, 1):
            sample = f"[{color}]●[/{color}]"
            self.console.print(f"  {i}. {sample} {desc}")

        color_choice = Prompt.ask(
            "\nEnter color name or number",
            default="cyan",
            choices=["cyan", "green", "blue", "magenta", "yellow", "white", "1", "2", "3", "4", "5", "6"]
        )

        # Map number to color
        color_map = {"1": "cyan", "2": "green", "3": "blue", "4": "magenta", "5": "yellow", "6": "white"}
        selected_color = color_map.get(color_choice, color_choice)

        user_config.theme_color = selected_color
        user_config.save()
        self.console.print(f"[{selected_color}]✅ Theme color set to {selected_color}![/{selected_color}]")

        # Step 4: Check for FLACO.md
        self.console.print("\n[bold]Step 4:[/bold] Checking for FLACO.md context file...")
        if self.agent.context_loader.has_context():
            context_path = self.agent.context_loader.get_context_path()
            self.console.print(f"[green]✅ Found FLACO.md[/green] at {context_path}")
        else:
            self.console.print("[yellow]ℹ️  No FLACO.md found[/yellow]")
            if Confirm.ask("Would you like to create one now?", default=True):
                result = self.agent.create_context_file(
                    target_dir=os.getcwd(),
                    template_path=None,
                    overwrite=False
                )
                if result.get("success"):
                    self.console.print(f"[green]✅ Created FLACO.md at {result['path']}[/green]")

        # Step 5: Create .flaco directory structure
        self.console.print("\n[bold]Step 5:[/bold] Setting up .flaco directory...")
        flaco_dir = Path.cwd() / ".flaco"
        commands_dir = flaco_dir / "commands"

        if not flaco_dir.exists():
            flaco_dir.mkdir(exist_ok=True)
            commands_dir.mkdir(exist_ok=True)
            self.console.print(f"[green]✅ Created .flaco directory structure[/green]")
        else:
            self.console.print(f"[green]✅ .flaco directory already exists[/green]")

        # Step 6: Permission mode recommendation
        self.console.print("\n[bold]Step 6:[/bold] Current permission mode")
        self.console.print(f"[cyan]Mode:[/cyan] {self.agent.permission_manager.mode.value}")
        self.console.print("[dim]Use /permissions to change mode (interactive/auto/headless)[/dim]")

        # Step 7: Show quick start guide
        self.console.print("\n[bold]Step 7:[/bold] Quick start tips")
        tips = Panel(Markdown("""
**You're all set! Here's what you can do:**

• Type **/** to see all slash commands
• Type **#** to use quick actions (e.g., `#Quick commit`)
• Type **/actions** to see all available quick actions
• Type **/help** for comprehensive help
• Create custom commands in `.flaco/commands/*.md`
• Press **Ctrl+C** to interrupt or exit

**Try these to get started:**
- `/scan` - Scan your project
- `/git status` - Check git status
- `#Status check` - Quick project overview
- Just chat naturally and ask for help!
        """), title="🚀 Ready to Go!", border_style="green")
        self.console.print(tips)

        # Mark setup as completed
        user_config.set("setup_completed", True)
        user_config.save()

        self.console.print("\n[green]✨ Setup complete! Happy coding with Flaco![/green]\n")

    def cmd_reset_config(self, args: str):
        """Reset Flaco configuration to defaults"""
        if Confirm.ask("[yellow]⚠️  Reset all Flaco settings to defaults?[/yellow]", default=False):
            user_config = UserConfig()
            user_config.reset()
            self.console.print("[green]✅ Configuration reset successfully![/green]")
            self.console.print("[dim]Run /setup to configure Flaco again.[/dim]")
        else:
            self.console.print("[dim]Reset cancelled.[/dim]")

    def cmd_snippet(self, args: str):
        """
        Browse and insert code snippets.

        Usage:
          /snippet                 - List all snippets
          /snippet <name>          - Insert a specific snippet
          /snippet search <query>  - Search snippets
          /snippet <category>      - List snippets in category
        """
        if not args:
            # List all snippets
            self._list_all_snippets()
        elif args.startswith("search "):
            # Search snippets
            query = args[7:].strip()
            self._search_snippets(query)
        elif args in [cat.value for cat in SnippetCategory]:
            # List category
            self._list_category_snippets(args)
        else:
            # Insert specific snippet
            self._insert_snippet(args)

    def _list_all_snippets(self):
        """List all available snippets"""
        table = Table(title="📋 Available Code Snippets", show_header=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Category", style="yellow")
        table.add_column("Description", style="white")

        snippets = snippet_library.snippets.values()
        for snippet in sorted(snippets, key=lambda s: (s.category.value, s.name)):
            table.add_row(
                snippet.name,
                snippet.category.value,
                snippet.description[:60] + "..." if len(snippet.description) > 60 else snippet.description
            )

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n[dim]💡 Usage: /snippet <name> to insert a snippet[/dim]")
        self.console.print("[dim]💡 Search: /snippet search <query>[/dim]")
        self.console.print("[dim]💡 Filter: /snippet <category> (e.g., /snippet python)[/dim]\n")

    def _search_snippets(self, query: str):
        """Search snippets by query"""
        results = snippet_library.search_snippets(query=query)

        if not results:
            self.console.print(f"[yellow]No snippets found matching '{query}'[/yellow]")
            return

        table = Table(title=f"🔍 Search Results for '{query}'", show_header=True)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Category", style="yellow")
        table.add_column("Description", style="white")

        for snippet in sorted(results, key=lambda s: s.name):
            table.add_row(
                snippet.name,
                snippet.category.value,
                snippet.description[:60] + "..." if len(snippet.description) > 60 else snippet.description
            )

        self.console.print("\n")
        self.console.print(table)
        self.console.print(f"\n[dim]💡 Found {len(results)} snippet(s)[/dim]\n")

    def _list_category_snippets(self, category_name: str):
        """List snippets in a specific category"""
        try:
            category = SnippetCategory(category_name)
            results = snippet_library.search_snippets(category=category)

            if not results:
                self.console.print(f"[yellow]No snippets in category '{category_name}'[/yellow]")
                return

            table = Table(title=f"📋 {category_name.capitalize()} Snippets", show_header=True)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")

            for snippet in sorted(results, key=lambda s: s.name):
                table.add_row(snippet.name, snippet.description)

            self.console.print("\n")
            self.console.print(table)
            self.console.print(f"\n[dim]💡 Found {len(results)} snippet(s)[/dim]\n")

        except ValueError:
            self.console.print(f"[red]Unknown category: {category_name}[/red]")
            self.console.print(f"[dim]Available categories: {', '.join([cat.value for cat in SnippetCategory])}[/dim]")

    def _insert_snippet(self, name: str):
        """Insert a specific snippet"""
        snippet = snippet_library.get_snippet(name)

        if not snippet:
            self.console.print(f"[red]Snippet '{name}' not found[/red]")
            self.console.print("[dim]Use /snippet to list all available snippets[/dim]")
            return

        # Show snippet details
        panel = Panel(
            Markdown(f"**Category:** {snippet.category.value}\n\n**Description:** {snippet.description}"),
            title=f"📋 {snippet.name}",
            border_style="cyan"
        )
        self.console.print("\n")
        self.console.print(panel)

        # Collect variable values if snippet has variables
        variables = {}
        if snippet.variables:
            self.console.print("\n[bold]Customize snippet variables:[/bold]")
            for var_name, default_value in snippet.variables.items():
                value = Prompt.ask(
                    f"  {var_name}",
                    default=default_value
                )
                variables[var_name] = value

        # Render snippet
        code = snippet_library.render_snippet(name, variables if variables else None)

        # Display the code
        self.console.print("\n[bold]Generated code:[/bold]")
        self.console.print(Panel(
            code,
            border_style="green",
            title=f"✨ {name}"
        ))

        # Ask if user wants to save to file
        if Confirm.ask("\n[cyan]Save to file?[/cyan]", default=False):
            filename = Prompt.ask("Filename", default=f"{name}.{snippet.language}")
            try:
                with open(filename, 'w') as f:
                    f.write(code)
                self.console.print(f"[green]✅ Saved to {filename}[/green]")
            except Exception as e:
                self.console.print(f"[red]❌ Error saving file: {str(e)}[/red]")

        self.console.print()
