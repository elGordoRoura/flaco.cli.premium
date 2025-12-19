#!/usr/bin/env python3
import warnings

# Suppress urllib3 OpenSSL warning for better UX
warnings.filterwarnings("ignore", message=".*urllib3 v2 only supports OpenSSL.*")

import click
import os
import sys
import signal
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.live import Live
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import time
import threading
import subprocess

from .agent import FlacoAgent
from .permissions import PermissionMode
from .context import FlacoContextLoader
from .commands.slash_commands import SlashCommandHandler
from .commands.quick_actions import QuickActionManager
from .config.user_config import UserConfig
from .utils.completers import FlacoCompleter, FlacoAutoSuggest
from .utils.update_checker import UpdateChecker
from . import __version__


console = Console()

# Global flag for interrupt handling
interrupt_requested = False

def signal_handler(sig, frame):
    """Handle interrupt signals"""
    global interrupt_requested
    interrupt_requested = True


def print_banner(theme_color: str):
    """Print the Flaco banner with Gemini-style ASCII art"""
    banner = """
  ███████╗██╗      █████╗  ██████╗ ██████╗
  ██╔════╝██║     ██╔══██╗██╔════╝██╔═══██╗
  █████╗  ██║     ███████║██║     ██║   ██║
  ██╔══╝  ██║     ██╔══██║██║     ██║   ██║
  ██║     ███████╗██║  ██║╚██████╗╚██████╔╝
  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝"""

    console.print(banner, style=f"bold {theme_color}", end="")
    console.print("  [dim]pro[/dim]")
    console.print("\n⚡ Local AI Coding Assistant")
    console.print("   Powered by Ollama")
    console.print("   Made by Roura.io\n")


def print_welcome(agent: FlacoAgent, theme_color: str):
    """Print welcome message with session information"""
    console.print("\n[bold green]Welcome to Flaco![/bold green]\n")

    # Check for updates and show banner if available
    has_update, latest_version, summary = UpdateChecker.check_for_updates(__version__)

    if has_update and latest_version:
        update_message = f"📦 Update available: v{__version__} → v{latest_version}"
        if summary:
            # Truncate summary if too long
            summary_text = summary[:60] + "..." if len(summary) > 60 else summary
            update_message += f"\n   {summary_text}"
        update_message += f"\n   Run: [bold cyan]pipx upgrade flaco-ai[/bold cyan]"

        console.print(Panel(
            update_message,
            border_style="yellow",
            padding=(0, 1)
        ))
        console.print()

    # Create session info box
    from rich.table import Table
    session_table = Table(show_header=False, box=None, padding=(0, 1))
    session_table.add_column(style="dim")
    session_table.add_column(style=theme_color)

    # Working directory
    import os
    cwd = os.getcwd()
    short_cwd = f".../{'/'.join(cwd.split('/')[-2:])}" if len(cwd) > 40 else cwd
    session_table.add_row("📁 Working Dir:", short_cwd)

    # FLACO.md context
    if agent.context_loader.has_context():
        context_path = agent.context_loader.get_context_path()
        session_table.add_row("📄 Context:", "✅ FLACO.md loaded")
    else:
        session_table.add_row("📄 Context:", "⚠️  No FLACO.md (use /init)")

    # Ollama connection (non-fatal check)
    if agent.llm.test_connection():
        session_table.add_row("🔗 Ollama:", f"✅ Connected ({agent.llm.base_url})")
        session_table.add_row("🤖 Model:", agent.llm.model)
    else:
        session_table.add_row("🔗 Ollama:", f"⚠️  Not connected ({agent.llm.base_url})")
        session_table.add_row("💡 Tip:", "Run 'ollama serve' to start Ollama")

    # Permission mode
    session_table.add_row("🔐 Permissions:", agent.permission_manager.mode.value)

    # Version and update check (reuse result from banner check)
    if has_update and latest_version:
        version_display = f"v{__version__} → v{latest_version} available"
        session_table.add_row("📦 Version:", version_display)
        session_table.add_row("⬆️  Update:", "pipx upgrade flaco-ai")
    else:
        session_table.add_row("📦 Version:", f"v{__version__} (latest)")

    # Print session info box
    session_panel = Panel(
        session_table,
        title=f"[bold {theme_color}]Session Info[/bold {theme_color}]",
        border_style=theme_color,
        padding=(0, 1)
    )
    console.print(session_panel)

    console.print("\n[dim]Type your message, '/' for commands, or '#' for quick actions.[/dim]")
    console.print("[dim]💡 Tip: Type '/' or '#' alone and press Enter to see all available options.[/dim]")
    console.print("[dim]💡 For multiline: Press Enter twice to submit. Paste works automatically.[/dim]")
    console.print("[dim]Press ESC or Ctrl+C to interrupt thinking. Ctrl+D to exit.[/dim]\n")


def display_metrics(metrics: dict, theme_color: str):
    """Display response metrics in a compact format"""
    time_str = f"{metrics['time_taken']:.2f}s"
    tokens_str = f"{metrics.get('tokens', 0):,}" if metrics.get('tokens', 0) > 0 else "N/A"
    agent_str = f"{metrics.get('agent_emoji', '🦙')} {metrics.get('agent', 'Flaco')}"

    # Check if this was a swarm task
    if metrics.get('swarm') and metrics.get('swarm_task'):
        swarm_task = metrics['swarm_task']
        agent_types = swarm_task.get('required_agents', [])
        console.print(f"[bold {theme_color}]🌟 Agent Swarm Activated![/bold {theme_color}]")
        console.print(f"[dim]Complexity: {swarm_task.get('complexity', 'unknown')} | {swarm_task.get('reasoning', '')}[/dim]")

    metrics_text = (
        f"[dim]"
        f"{agent_str} • "
        f"⏱️  {time_str} • "
        f"🎫 {tokens_str} tokens • "
        f"🔄 {metrics.get('llm_calls', 1)} calls"
        f"[/dim]"
    )
    console.print(metrics_text)


@click.command()
@click.option(
    '--model', '-m',
    default=None,
    help='Ollama model to use (default: from config or qwen2.5-coder:7b)'
)
@click.option(
    '--ollama-url', '-u',
    default=None,
    help='Ollama server URL (default: from config or http://localhost:11434)'
)
@click.option(
    '--headless', '-p',
    is_flag=True,
    help='Run in headless mode (non-interactive, for automation)'
)
@click.option(
    '--auto-approve', '-y',
    is_flag=True,
    help='Auto-approve all tool executions (use with caution!)'
)
@click.option(
    '--prompt',
    help='Single prompt to execute in headless mode'
)
@click.option(
    '--working-dir', '-d',
    help='Set working directory'
)
def main(model, ollama_url, headless, auto_approve, prompt, working_dir):
    """Flaco AI - Local AI Coding Assistant powered by Ollama"""

    # Register signal handler for graceful interrupts
    signal.signal(signal.SIGINT, signal_handler)

    # Change working directory if specified
    if working_dir:
        if os.path.isdir(working_dir):
            os.chdir(working_dir)
        else:
            console.print(f"[red]Error: Working directory not found: {working_dir}[/red]")
            sys.exit(1)

    # Check for first run BEFORE initializing anything
    user_config = UserConfig()
    is_first_run = user_config.is_first_run()

    # If first run, show banner and run setup FIRST
    if is_first_run and not headless:
        theme_color = user_config.theme_color
        print_banner(theme_color)
        console.print(f"\n[bold {theme_color}]👋 Welcome to Flaco![/bold {theme_color}]")
        console.print("[dim]It looks like this is your first time running Flaco.[/dim]")
        console.print("[dim]Let's get you set up with a quick wizard...[/dim]\n")

        # Create temporary agent just for setup command
        temp_agent = FlacoAgent(
            ollama_url=ollama_url or "http://localhost:11434",
            model=model or "qwen2.5-coder:7b",
            permission_mode=PermissionMode.INTERACTIVE
        )
        temp_slash_handler = SlashCommandHandler(temp_agent)

        # Run setup wizard
        temp_slash_handler.handle_command("/setup")

        console.print("\n[green]Setup complete! You can now start using Flaco.[/green]")
        console.print("[dim]Press Enter to continue...[/dim]")
        input()

        # Reload config after setup
        user_config = UserConfig()

    # Get configured values (use CLI args if provided, otherwise use config)
    configured_url = ollama_url or user_config.ollama_url
    configured_model = model or user_config.ollama_model
    theme_color = user_config.theme_color

    # Determine permission mode
    if headless:
        permission_mode = PermissionMode.HEADLESS
    elif auto_approve:
        permission_mode = PermissionMode.AUTO_APPROVE
    else:
        permission_mode = PermissionMode.INTERACTIVE

    # Initialize agent with configured values
    agent = FlacoAgent(
        ollama_url=configured_url,
        model=configured_model,
        permission_mode=permission_mode
    )

    # Initialize slash command handler and quick actions
    slash_handler = SlashCommandHandler(agent)
    quick_actions = QuickActionManager()

    # Headless mode - single prompt execution
    if headless and prompt:
        response, metrics = agent.chat(prompt)
        console.print(Markdown(response))
        console.print()
        display_metrics(metrics, theme_color)
        return

    # Interactive mode - print banner if not first run (already printed above)
    if not is_first_run:
        print_banner(theme_color)

    print_welcome(agent, theme_color)

    # Set up prompt session with history and autocomplete
    history_file = os.path.expanduser("~/.flaco_history")
    completer = FlacoCompleter(slash_handler, quick_actions)
    auto_suggest = FlacoAutoSuggest(slash_handler, quick_actions)

    # More subtle autocomplete (Claude-style)
    from prompt_toolkit.key_binding import KeyBindings

    # Custom key bindings for better multiline support
    bindings = KeyBindings()

    @bindings.add('enter')
    def _(event):
        """Submit on Enter for single line, or Enter twice for multiline"""
        buffer = event.current_buffer
        # If buffer is empty or doesn't contain newlines, submit immediately
        if not buffer.text or '\n' not in buffer.text:
            buffer.validate_and_handle()
        else:
            # Multi-line: check if cursor is at end and previous char is newline
            # This means they pressed Enter on an empty line - submit
            if buffer.cursor_position == len(buffer.text) and buffer.text.endswith('\n'):
                buffer.validate_and_handle()
            else:
                # Add newline for multi-line input
                buffer.insert_text('\n')

    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=auto_suggest,  # Use custom inline suggestions
        completer=completer,
        complete_while_typing=False,  # Only show on Tab (cleaner)
        complete_in_thread=True,  # Don't block UI
        key_bindings=bindings,
        multiline=True  # Enable multiline for paste detection
    )

    # Main conversation loop
    try:
        while True:
            try:
                # Get user input with command hints
                # Show available commands hint for / and #
                prompt_text = "\n> You: "

                user_input = session.prompt(prompt_text)

                if not user_input.strip():
                    continue

                # Natural exit on "bye"
                if user_input.strip().lower() == 'bye':
                    console.print(f"\n[{theme_color}]Goodbye! 👋[/{theme_color}]")
                    break

                # Show available commands when starting with / or #
                if user_input == '/' or (user_input.startswith('/') and len(user_input) == 1):
                    # Show all slash commands
                    console.print("\n[cyan]Available slash commands:[/cyan]")
                    commands_list = sorted(slash_handler.commands.keys())
                    for i in range(0, len(commands_list), 4):
                        row = commands_list[i:i+4]
                        console.print("  " + "  ".join(f"/{cmd:15}" for cmd in row))
                    console.print("\n[dim]Type to filter, or /help for details[/dim]\n")
                    continue

                if user_input == '#':
                    # Show all quick actions
                    console.print("\n[cyan]Available quick actions:[/cyan]")
                    for action in quick_actions.list_actions():
                        console.print(f"  [cyan]#{action.name:20}[/cyan] [dim]{action.description}[/dim]")
                    console.print("\n[dim]Type # followed by action name[/dim]\n")
                    continue

                # Show filtered quick actions as user types
                if user_input.startswith('#') and len(user_input) > 1:
                    partial = user_input[1:].lower().replace(' ', '')
                    matches = [a for a in quick_actions.list_actions()
                              if a.name.lower().replace(' ', '').startswith(partial)]
                    if matches and len(matches) < len(quick_actions.list_actions()):
                        console.print(f"\n[dim]Matching quick actions for '{user_input}':[/dim]")
                        for action in matches:
                            console.print(f"  [cyan]#{action.name:20}[/cyan] [dim]{action.description}[/dim]")
                        console.print(f"\n[dim]Press Enter to see matches, or complete the name to execute[/dim]\n")
                        continue

                # Detect large paste (>15 lines)
                lines = user_input.split('\n')
                if len(lines) > 15:
                    # Show paste summary
                    console.print(f"\n[cyan]📋 Large paste detected:[/cyan] {len(lines)} lines")

                    # Show preview of first and last few lines
                    preview_lines = 3
                    console.print("[dim]Preview (first 3 lines):[/dim]")
                    for i, line in enumerate(lines[:preview_lines]):
                        preview = line[:80] + "..." if len(line) > 80 else line
                        console.print(f"[dim]  {i+1} | {preview}[/dim]")

                    if len(lines) > preview_lines * 2:
                        console.print(f"[dim]  ... ({len(lines) - preview_lines * 2} more lines) ...[/dim]")

                    console.print("[dim]Preview (last 3 lines):[/dim]")
                    for i, line in enumerate(lines[-preview_lines:]):
                        line_num = len(lines) - preview_lines + i + 1
                        preview = line[:80] + "..." if len(line) > 80 else line
                        console.print(f"[dim]  {line_num} | {preview}[/dim]")

                    console.print(f"\n[green]Processing {len(lines)} lines...[/green]\n")

                # Check for quick actions (#commands)
                if user_input.startswith('#'):
                    action_name = user_input[1:].strip()
                    # Try exact match first, then case-insensitive
                    action = quick_actions.get_action(action_name)
                    if not action:
                        # Try case-insensitive match
                        for a in quick_actions.list_actions():
                            if a.name.lower().replace(' ', '') == action_name.lower().replace(' ', ''):
                                action = a
                                break

                    if action:
                        console.print(f"[cyan]🚀 Running quick action:[/cyan] {action.name}")
                        console.print(f"[dim]{action.description}[/dim]\n")

                        for cmd in action.commands:
                            if cmd.startswith('/'):
                                # It's a slash command
                                console.print(f"[dim]→ {cmd}[/dim]")
                                slash_handler.handle_command(cmd)
                            else:
                                # It's a bash command - execute it directly
                                console.print(f"[dim]→ {cmd}[/dim]")
                                try:
                                    result = subprocess.run(
                                        cmd,
                                        shell=True,
                                        capture_output=True,
                                        text=True,
                                        timeout=30
                                    )
                                    if result.stdout:
                                        console.print(result.stdout)
                                    if result.stderr:
                                        console.print(f"[yellow]{result.stderr}[/yellow]")
                                    if result.returncode != 0:
                                        console.print(f"[red]Command failed with exit code {result.returncode}[/red]")
                                except subprocess.TimeoutExpired:
                                    console.print("[red]Command timed out[/red]")
                                except Exception as e:
                                    console.print(f"[red]Error: {str(e)}[/red]")

                        console.print("[green]✅ Quick action completed![/green]")
                    else:
                        console.print(f"[red]Unknown quick action:[/red] #{action_name}")
                        console.print("\n[yellow]Available quick actions:[/yellow]")
                        for qa in quick_actions.list_actions():
                            console.print(f"  #{qa.name} - {qa.description}")
                    continue

                # Check for slash commands
                if user_input.startswith('/'):
                    slash_handler.handle_command(user_input)
                    continue

                # Check for image attachment syntax: @image:/path/to/image.png message
                if user_input.startswith('@image:'):
                    parts = user_input.split(' ', 1)
                    image_path = parts[0].replace('@image:', '')
                    message = parts[1] if len(parts) > 1 else "What's in this image?"

                    console.print("\n[cyan]🤖 Flaco:[/cyan]")

                    # Show thinking animation for image processing
                    with console.status("⚡ Analyzing image...", spinner="dots") as status:
                        response = agent.chat_with_image(message, image_path)

                    console.print(Markdown(response))
                    continue

                # Check for swarm first
                swarm_task = agent.agent_swarm.analyze_task(user_input)

                if swarm_task:
                    # Show swarm collaboration
                    swarm_agents = agent.agent_swarm.get_swarm_agents(swarm_task)
                    agent_emojis = ' '.join([a.emoji for a in swarm_agents])
                    # Include agent name in status text for single-line display
                    status_text = f"{agent_emojis} Flaco: Team collaboration in progress..."
                else:
                    # Route to get the agent first
                    selected_agent = agent.agent_router.route(user_input)
                    thinking_message = selected_agent.get_random_thinking_message()

                    # Include agent name and thinking message in status text for single-line display
                    status_text = f"{selected_agent.emoji} {selected_agent.name}: {thinking_message}..."

                # Reset interrupt flag
                global interrupt_requested
                interrupt_requested = False

                interrupted = False
                response = None
                metrics = None

                def run_chat():
                    nonlocal response, metrics, interrupted
                    global interrupt_requested
                    try:
                        # Check if interrupted before starting
                        if interrupt_requested:
                            interrupted = True
                            return
                        response, metrics = agent.chat(user_input)
                    except (KeyboardInterrupt, Exception) as e:
                        if isinstance(e, KeyboardInterrupt) or interrupt_requested:
                            interrupted = True
                        else:
                            raise

                # Run chat in a thread so we can handle interrupts
                chat_thread = threading.Thread(target=run_chat)
                chat_thread.daemon = True

                try:
                    chat_thread.start()

                    # Poll for completion or interrupt (check every 0.1s)
                    import sys
                    import select
                    import termios
                    import tty
                    from rich.live import Live

                    # Save terminal settings
                    old_settings = None
                    try:
                        old_settings = termios.tcgetattr(sys.stdin)
                        tty.setcbreak(sys.stdin.fileno())
                    except:
                        pass  # Not a TTY, skip ESC handling

                    # Create animated spinner with agent name and status
                    spinner = Spinner("dots", text=status_text, style="bold cyan")

                    with Live(spinner, console=console, refresh_per_second=10, transient=True) as live:
                        while chat_thread.is_alive():
                            # Check for interrupt flag
                            if interrupt_requested:
                                interrupted = True
                                break

                            # Check for ESC key (non-blocking)
                            if old_settings and sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                                char = sys.stdin.read(1)
                                if char == '\x1b':  # ESC key
                                    interrupt_requested = True
                                    interrupted = True
                                    break

                            chat_thread.join(timeout=0.1)

                    # Restore terminal settings
                    if old_settings:
                        try:
                            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        except:
                            pass

                    # Wait a bit for thread to finish
                    chat_thread.join(timeout=0.5)

                    if interrupted or interrupt_requested:
                        console.print("\n[yellow]⚠️  Interrupted! You can rephrase or try again.[/yellow]")
                        # Reset flag for next prompt
                        interrupt_requested = False
                        continue

                    if response:
                        # Clear the agent name line
                        import sys
                        sys.stdout.write('\033[F\033[K')
                        sys.stdout.flush()

                        console.print(Markdown(response))
                        display_metrics(metrics, theme_color)
                except KeyboardInterrupt:
                    interrupt_requested = True
                    console.print("\n[yellow]⚠️  Interrupted! You can rephrase or try again.[/yellow]")
                    continue

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted. Use /exit or Ctrl+D to quit.[/yellow]")
                continue
            except EOFError:
                console.print(f"\n\n[{theme_color}]Goodbye! 👋[/{theme_color}]")
                break

    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
