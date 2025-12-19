"""Auto-completion for Flaco commands"""

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.document import Document
from typing import Iterable, Optional


class FlacoCompleter(Completer):
    """Custom completer for Flaco slash commands and quick actions"""

    def __init__(self, slash_handler, quick_actions):
        self.slash_handler = slash_handler
        self.quick_actions = quick_actions

    def get_completions(self, document, complete_event):
        """Generate completions based on current input"""
        text = document.text_before_cursor
        completions = []

        # Slash command completions
        if text.startswith('/'):
            command_part = text[1:].lower()
            for cmd_name in sorted(self.slash_handler.commands.keys()):
                if cmd_name.startswith(command_part):
                    completions.append(Completion(
                        cmd_name,
                        start_position=-len(command_part),
                        display=f"/{cmd_name}",
                        display_meta=self._get_command_description(cmd_name)
                    ))

        # Quick action completions
        elif text.startswith('#'):
            action_part = text[1:].lower()
            for action in self.quick_actions.list_actions():
                if action.name.lower().startswith(action_part):
                    completions.append(Completion(
                        action.name,
                        start_position=-len(action_part),
                        display=f"#{action.name}",
                        display_meta=action.description
                    ))

        # Return completions
        for completion in completions:
            yield completion

    def _get_command_description(self, cmd_name):
        """Get description for a command"""
        descriptions = {
            "help": "Show all commands",
            "setup": "Interactive setup wizard",
            "exit": "Exit Flaco",
            "quit": "Exit Flaco",
            "clear": "Clear screen",
            "reset": "Reset conversation",
            "status": "Show current status",
            "init": "Create FLACO.md",
            "context": "Show context",
            "costs": "Show cost info",
            "model": "Change model",
            "models": "List models",
            "history": "Show history",
            "permissions": "Change permissions",
            "todos": "Show todos",
            "scan": "Scan project",
            "project": "Manage projects",
            "git": "Git operations",
            "stats": "Show stats",
            "recap": "Activity recap",
            "review": "Code review mode",
            "refresh": "Refresh context",
            "agent": "Manage agents",
            "actions": "Show quick actions",
            "reset-config": "Reset config"
        }
        return descriptions.get(cmd_name, "")


class FlacoAutoSuggest(AutoSuggest):
    """Custom auto-suggest for inline command completion"""

    def __init__(self, slash_handler, quick_actions):
        self.slash_handler = slash_handler
        self.quick_actions = quick_actions

    def get_suggestion(self, buffer: "Buffer", document: Document) -> Optional[Suggestion]:
        """Return inline suggestion based on current input"""
        text = document.text.lower()

        # Slash command suggestions
        if text.startswith('/') and len(text) > 1:
            command_part = text[1:]
            # Find first matching command
            for cmd_name in sorted(self.slash_handler.commands.keys()):
                if cmd_name.startswith(command_part) and cmd_name != command_part:
                    # Return the remaining part to complete
                    suggestion = cmd_name[len(command_part):]
                    return Suggestion(suggestion)

        # Quick action suggestions
        elif text.startswith('#') and len(text) > 1:
            action_part = text[1:].lower().replace(' ', '')
            # Find first matching action
            for action in self.quick_actions.list_actions():
                action_normalized = action.name.lower().replace(' ', '')
                if action_normalized.startswith(action_part) and action_normalized != action_part:
                    # Calculate the remaining part
                    # Need to match case and spacing from original
                    typed_len = len(text) - 1  # Exclude the #
                    suggestion = action.name[typed_len:]
                    return Suggestion(suggestion)

        return None
