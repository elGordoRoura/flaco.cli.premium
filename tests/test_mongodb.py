#!/usr/bin/env python3
"""Test MongoDB connection for Flaco AI."""

import os
from dotenv import load_dotenv
from flaco.database import MongoDBManager

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB connection and basic operations."""
    print("🔍 Testing MongoDB connection...\n")

    # Initialize MongoDB manager
    db = MongoDBManager()

    if not db.connected:
        print("❌ Failed to connect to MongoDB")
        print(f"Connection string: {os.getenv('MONGODB_URI', 'Not set')}")
        return False

    print("✅ Connected to MongoDB successfully!\n")

    # Test saving a conversation
    print("📝 Testing conversation save...")
    test_messages = [
        {"role": "user", "content": "Hello, Flaco!"},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

    success = db.save_conversation("test_session", test_messages)
    if success:
        print("✅ Conversation saved successfully")
    else:
        print("❌ Failed to save conversation")
        return False

    # Test loading a conversation
    print("\n📥 Testing conversation load...")
    loaded_messages = db.load_conversation("test_session")
    if loaded_messages == test_messages:
        print("✅ Conversation loaded successfully")
        print(f"   Loaded {len(loaded_messages)} messages")
    else:
        print("❌ Failed to load conversation correctly")
        return False

    # Test database stats
    print("\n📊 Database Statistics:")
    stats = db.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # Cleanup test data
    print("\n🧹 Cleaning up test data...")
    db.clear_conversation("test_session")
    print("✅ Test data cleaned up")

    # Disconnect
    db.disconnect()
    print("\n✅ All tests passed! MongoDB integration is working correctly.")
    return True

if __name__ == "__main__":
    test_mongodb_connection()
