"""MongoDB manager for Flaco AI data persistence."""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import logging

logger = logging.getLogger(__name__)


class MongoDBManager:
    """Manages MongoDB connections and operations for Flaco AI."""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize MongoDB manager.

        Args:
            connection_string: MongoDB connection URI (defaults to env var)
        """
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        self.client: Optional[MongoClient] = None
        self.db = None
        self.connected = False

        if self.connection_string:
            self.connect()

    def connect(self) -> bool:
        """
        Connect to MongoDB.

        Returns:
            bool: True if connection successful
        """
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')

            # Get database name from connection string or use default
            self.db = self.client['flaco_ai']
            self.connected = True
            logger.info("✅ Connected to MongoDB")
            return True

        except (ConnectionFailure, OperationFailure) as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("Disconnected from MongoDB")

    # ==================== Conversation Memory ====================

    def save_conversation(self, session_id: str, messages: List[Dict[str, Any]]) -> bool:
        """
        Save conversation messages to MongoDB.

        Args:
            session_id: Unique session identifier
            messages: List of conversation messages

        Returns:
            bool: True if saved successfully
        """
        if not self.connected:
            return False

        try:
            collection = self.db['conversations']
            collection.update_one(
                {'session_id': session_id},
                {
                    '$set': {
                        'messages': messages,
                        'updated_at': datetime.utcnow()
                    },
                    '$setOnInsert': {
                        'created_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")
            return False

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Load conversation messages from MongoDB.

        Args:
            session_id: Unique session identifier

        Returns:
            List of conversation messages
        """
        if not self.connected:
            return []

        try:
            collection = self.db['conversations']
            doc = collection.find_one({'session_id': session_id})
            return doc['messages'] if doc else []
        except Exception as e:
            logger.error(f"Failed to load conversation: {e}")
            return []

    def clear_conversation(self, session_id: str) -> bool:
        """Delete conversation history."""
        if not self.connected:
            return False

        try:
            collection = self.db['conversations']
            collection.delete_one({'session_id': session_id})
            return True
        except Exception as e:
            logger.error(f"Failed to clear conversation: {e}")
            return False

    # ==================== Project Context ====================

    def save_project_context(self, project_name: str, context: Dict[str, Any]) -> bool:
        """Save project context and metadata."""
        if not self.connected:
            return False

        try:
            collection = self.db['projects']
            collection.update_one(
                {'name': project_name},
                {
                    '$set': {
                        'context': context,
                        'updated_at': datetime.utcnow()
                    },
                    '$setOnInsert': {
                        'created_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save project context: {e}")
            return False

    def load_project_context(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Load project context."""
        if not self.connected:
            return None

        try:
            collection = self.db['projects']
            doc = collection.find_one({'name': project_name})
            return doc['context'] if doc else None
        except Exception as e:
            logger.error(f"Failed to load project context: {e}")
            return None

    # ==================== Analytics & Contributions ====================

    def save_activity(self, activity_data: Dict[str, Any]) -> bool:
        """Save user activity for analytics."""
        if not self.connected:
            return False

        try:
            collection = self.db['activities']
            activity_data['timestamp'] = datetime.utcnow()
            collection.insert_one(activity_data)
            return True
        except Exception as e:
            logger.error(f"Failed to save activity: {e}")
            return False

    def get_activities(self,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      activity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get activities with optional filters."""
        if not self.connected:
            return []

        try:
            collection = self.db['activities']
            query = {}

            if start_date or end_date:
                query['timestamp'] = {}
                if start_date:
                    query['timestamp']['$gte'] = start_date
                if end_date:
                    query['timestamp']['$lte'] = end_date

            if activity_type:
                query['type'] = activity_type

            return list(collection.find(query).sort('timestamp', -1))
        except Exception as e:
            logger.error(f"Failed to get activities: {e}")
            return []

    # ==================== Agent State ====================

    def save_agent_state(self, agent_name: str, state: Dict[str, Any]) -> bool:
        """Save agent state for persistence."""
        if not self.connected:
            return False

        try:
            collection = self.db['agent_states']
            collection.update_one(
                {'agent': agent_name},
                {
                    '$set': {
                        'state': state,
                        'updated_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save agent state: {e}")
            return False

    def load_agent_state(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Load agent state."""
        if not self.connected:
            return None

        try:
            collection = self.db['agent_states']
            doc = collection.find_one({'agent': agent_name})
            return doc['state'] if doc else None
        except Exception as e:
            logger.error(f"Failed to load agent state: {e}")
            return None

    # ==================== Utilities ====================

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        if not self.connected:
            return {'connected': False}

        try:
            return {
                'connected': True,
                'conversations': self.db['conversations'].count_documents({}),
                'projects': self.db['projects'].count_documents({}),
                'activities': self.db['activities'].count_documents({}),
                'agent_states': self.db['agent_states'].count_documents({})
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {'connected': True, 'error': str(e)}
