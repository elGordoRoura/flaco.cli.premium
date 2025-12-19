"""
Quick Actions System for Flaco
Provides hashtag (#) shortcuts for common workflows
"""

from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class QuickAction:
    """Represents a quick action that can be triggered with #"""
    name: str
    description: str
    commands: List[str]


class QuickActionManager:
    """Manages quick actions (#commands)"""

    def __init__(self):
        self.actions: List[QuickAction] = self._default_actions()

    def _default_actions(self) -> List[QuickAction]:
        """Default quick actions available to all users"""
        return [
            QuickAction(
                name="Quick commit",
                description="Stage, commit, and push changes",
                commands=[
                    "/git status",
                    "git add .",
                    "git commit -m 'Update'",
                    "git push"
                ]
            ),
            QuickAction(
                name="Fresh start",
                description="Clear context and start new conversation",
                commands=["/clear"]
            ),
            QuickAction(
                name="Code review",
                description="Review recent changes",
                commands=[
                    "git diff --stat",
                    "git diff"
                ]
            ),
            QuickAction(
                name="Test and build",
                description="Run tests and build project",
                commands=[
                    "npm test",
                    "npm run build"
                ]
            ),
            QuickAction(
                name="Status check",
                description="Check project status",
                commands=[
                    "/status",
                    "/git status",
                    "/todos"
                ]
            ),
            QuickAction(
                name="Project scan",
                description="Scan project and show insights",
                commands=["/scan"]
            )
        ]

    def get_action(self, name: str) -> Optional[QuickAction]:
        """Get a quick action by name (case-insensitive)"""
        name_lower = name.lower()
        for action in self.actions:
            if action.name.lower() == name_lower:
                return action
        return None

    def list_actions(self) -> List[QuickAction]:
        """Get all available quick actions"""
        return self.actions

    def add_custom_action(self, name: str, description: str, commands: List[str]) -> QuickAction:
        """Add a custom quick action"""
        action = QuickAction(name=name, description=description, commands=commands)
        self.actions.append(action)
        return action

    def remove_action(self, name: str) -> bool:
        """Remove a quick action by name"""
        name_lower = name.lower()
        for i, action in enumerate(self.actions):
            if action.name.lower() == name_lower:
                del self.actions[i]
                return True
        return False

    def get_suggestions(self, partial: str) -> List[QuickAction]:
        """Get action suggestions based on partial name"""
        partial_lower = partial.lower()
        return [
            action for action in self.actions
            if partial_lower in action.name.lower()
        ]
