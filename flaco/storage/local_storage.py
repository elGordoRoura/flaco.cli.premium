"""Local file-based storage for Flaco AI"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class LocalStorageManager:
    """Manages local file storage for conversations and data"""

    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize local storage manager

        Args:
            storage_dir: Directory to store data. Defaults to ~/.flaco/data
        """
        if storage_dir is None:
            storage_dir = os.path.expanduser('~/.flaco/data')

        self.storage_dir = Path(storage_dir)
        self.conversations_dir = self.storage_dir / 'conversations'
        self.projects_dir = self.storage_dir / 'projects'
        self.activities_dir = self.storage_dir / 'activities'

        # Create directories
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.activities_dir.mkdir(parents=True, exist_ok=True)

        self.connected = True

    def save_conversation(self, session_id: str, messages: List[Dict[str, Any]]) -> bool:
        """Save conversation to local file

        Args:
            session_id: Unique session identifier
            messages: List of message dictionaries

        Returns:
            True if successful
        """
        try:
            file_path = self.conversations_dir / f"{session_id}.json"
            data = {
                'session_id': session_id,
                'messages': messages,
                'updated_at': datetime.now().isoformat()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load conversation from local file

        Args:
            session_id: Unique session identifier

        Returns:
            List of messages or empty list if not found
        """
        try:
            file_path = self.conversations_dir / f"{session_id}.json"

            if not file_path.exists():
                return []

            with open(file_path, 'r') as f:
                data = json.load(f)

            return data.get('messages', [])
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return []

    def clear_conversation(self, session_id: str) -> bool:
        """Delete conversation file

        Args:
            session_id: Unique session identifier

        Returns:
            True if successful
        """
        try:
            file_path = self.conversations_dir / f"{session_id}.json"

            if file_path.exists():
                file_path.unlink()

            return True
        except Exception as e:
            print(f"Error clearing conversation: {e}")
            return False

    def list_conversations(self) -> List[Dict[str, Any]]:
        """List all saved conversations

        Returns:
            List of conversation metadata
        """
        try:
            conversations = []

            for file_path in self.conversations_dir.glob('*.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)

                    conversations.append({
                        'session_id': data['session_id'],
                        'updated_at': data.get('updated_at'),
                        'message_count': len(data.get('messages', []))
                    })
                except Exception:
                    continue

            # Sort by updated_at descending
            conversations.sort(key=lambda x: x.get('updated_at', ''), reverse=True)

            return conversations
        except Exception as e:
            print(f"Error listing conversations: {e}")
            return []

    def save_project_context(self, project_name: str, context: Dict[str, Any]) -> bool:
        """Save project context to local file

        Args:
            project_name: Name of the project
            context: Project context data

        Returns:
            True if successful
        """
        try:
            file_path = self.projects_dir / f"{project_name}.json"
            data = {
                'project_name': project_name,
                'context': context,
                'updated_at': datetime.now().isoformat()
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving project context: {e}")
            return False

    def load_project_context(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Load project context from local file

        Args:
            project_name: Name of the project

        Returns:
            Project context or None if not found
        """
        try:
            file_path = self.projects_dir / f"{project_name}.json"

            if not file_path.exists():
                return None

            with open(file_path, 'r') as f:
                data = json.load(f)

            return data.get('context')
        except Exception as e:
            print(f"Error loading project context: {e}")
            return None

    def save_activity(self, activity_data: Dict[str, Any]) -> bool:
        """Save activity/analytics data to local file

        Args:
            activity_data: Activity data to save

        Returns:
            True if successful
        """
        try:
            timestamp = datetime.now().isoformat()
            file_path = self.activities_dir / f"{timestamp.replace(':', '-')}.json"

            data = {
                'timestamp': timestamp,
                'activity': activity_data
            }

            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving activity: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics

        Returns:
            Dictionary with storage stats
        """
        try:
            conversation_count = len(list(self.conversations_dir.glob('*.json')))
            project_count = len(list(self.projects_dir.glob('*.json')))
            activity_count = len(list(self.activities_dir.glob('*.json')))

            return {
                'storage_type': 'Local File Storage',
                'storage_location': str(self.storage_dir),
                'conversations': conversation_count,
                'projects': project_count,
                'activities': activity_count,
                'connected': self.connected
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'storage_type': 'Local File Storage',
                'connected': False,
                'error': str(e)
            }

    def disconnect(self):
        """Cleanup (no-op for file storage)"""
        self.connected = False
