import json
import os
from typing import Dict, Any, List
from .base import Tool, ToolResult, ToolStatus
from pathlib import Path


class TodoTool(Tool):
    """Manage todo list for task tracking"""

    def __init__(self):
        super().__init__(
            name="TodoWrite",
            description="Create and manage a task list to track progress on complex tasks",
            requires_permission=False
        )
        self.todo_file = os.path.join(os.getcwd(), ".flaco_todos.json")

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "todos": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The task description (imperative form)"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed"],
                                "description": "Current status of the task"
                            },
                            "activeForm": {
                                "type": "string",
                                "description": "Present continuous form (e.g., 'Running tests')"
                            }
                        },
                        "required": ["content", "status", "activeForm"]
                    },
                    "description": "The updated todo list"
                }
            },
            "required": ["todos"]
        }

    def execute(self, todos: List[Dict[str, str]]) -> ToolResult:
        try:
            # Validate that only one task is in_progress
            in_progress_count = sum(1 for todo in todos if todo["status"] == "in_progress")
            if in_progress_count != 1:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Exactly one task must be in_progress (found {in_progress_count})"
                )

            # Save todos to file
            with open(self.todo_file, 'w') as f:
                json.dump(todos, f, indent=2)

            # Format output
            output = self._format_todos(todos)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"total": len(todos), "completed": sum(1 for t in todos if t["status"] == "completed")}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error managing todos: {str(e)}"
            )

    def _format_todos(self, todos: List[Dict[str, str]]) -> str:
        """Format todos for display"""
        output = "Task List:\n"
        for i, todo in enumerate(todos, 1):
            status_icon = {
                "pending": "⏳",
                "in_progress": "🔄",
                "completed": "✅"
            }[todo["status"]]

            output += f"{i}. {status_icon} {todo['content']}\n"

        return output

    def get_todos(self) -> List[Dict[str, str]]:
        """Load current todos from file"""
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r') as f:
                return json.load(f)
        return []
