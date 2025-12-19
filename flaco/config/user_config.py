"""User configuration management for Flaco"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class UserConfig:
    """Manages user configuration for Flaco"""

    def __init__(self):
        self.config_dir = Path.home() / ".flaco"
        self.config_file = self.config_dir / "config.json"
        self._config: Dict[str, Any] = {}
        self._load_config()

    def is_first_run(self) -> bool:
        """Check if this is the first run (config file doesn't exist or setup not completed)"""
        return not self.config_file.exists() or not self._config.get("setup_completed", False)

    def _load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self._config = json.load(f)
            except Exception:
                self._config = {}
        else:
            self._config = self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "ollama_url": "http://localhost:11434",
            "ollama_model": "qwen2.5-coder:7b",
            "theme_color": "cyan",
            "permission_mode": "interactive",
            "setup_completed": False
        }

    def save(self):
        """Save configuration to file"""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self._config[key] = value

    @property
    def ollama_url(self) -> str:
        """Get Ollama URL"""
        return self._config.get("ollama_url", "http://localhost:11434")

    @ollama_url.setter
    def ollama_url(self, value: str):
        """Set Ollama URL (prepends http:// if not present)"""
        if not value.startswith(("http://", "https://")):
            value = f"http://{value}"
        self._config["ollama_url"] = value

    @property
    def ollama_model(self) -> str:
        """Get Ollama model"""
        return self._config.get("ollama_model", "qwen2.5-coder:7b")

    @ollama_model.setter
    def ollama_model(self, value: str):
        """Set Ollama model"""
        self._config["ollama_model"] = value

    @property
    def theme_color(self) -> str:
        """Get theme color"""
        return self._config.get("theme_color", "cyan")

    @theme_color.setter
    def theme_color(self, value: str):
        """Set theme color"""
        self._config["theme_color"] = value

    @property
    def permission_mode(self) -> str:
        """Get permission mode"""
        return self._config.get("permission_mode", "interactive")

    @permission_mode.setter
    def permission_mode(self, value: str):
        """Set permission mode"""
        self._config["permission_mode"] = value

    def reset(self):
        """Reset configuration to defaults"""
        self._config = self._default_config()
        if self.config_file.exists():
            self.config_file.unlink()
