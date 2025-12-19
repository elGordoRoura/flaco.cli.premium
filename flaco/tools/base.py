from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class ToolStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PERMISSION_DENIED = "permission_denied"


@dataclass
class ToolResult:
    """Result from a tool execution"""
    status: ToolStatus
    output: str
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "output": self.output,
            "error": self.error,
            "metadata": self.metadata or {}
        }


class Tool(ABC):
    """Base class for all tools"""

    def __init__(self, name: str, description: str, requires_permission: bool = False):
        self.name = name
        self.description = description
        self.requires_permission = requires_permission

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool with given parameters"""
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Get the JSON schema for this tool (for function calling)"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters()
            }
        }

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get the parameters schema for this tool"""
        pass

    def validate_params(self, **kwargs) -> bool:
        """Validate parameters before execution"""
        return True
