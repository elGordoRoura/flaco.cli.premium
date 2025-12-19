"""Tests for Ollama client"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from flaco.llm.ollama_client import OllamaClient


class TestOllamaClient(unittest.TestCase):
    """Test Ollama API client"""

    def setUp(self):
        """Set up test fixtures"""
        self.client = OllamaClient(base_url="http://localhost:11434", model="test-model")

    @patch('flaco.llm.ollama_client.requests.post')
    def test_chat_success(self, mock_post):
        """Test successful chat request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {"role": "assistant", "content": "Test response"}
        }
        mock_post.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]
        response = self.client.chat(messages)

        self.assertEqual(response["message"]["content"], "Test response")
        mock_post.assert_called_once()

    @patch('flaco.llm.ollama_client.requests.post')
    def test_chat_connection_error(self, mock_post):
        """Test connection error handling"""
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection refused")

        messages = [{"role": "user", "content": "Hello"}]

        with self.assertRaises(Exception) as context:
            self.client.chat(messages, max_retries=2)

        self.assertIn("Failed to connect to Ollama", str(context.exception))
        # Should retry 2 times
        self.assertEqual(mock_post.call_count, 2)

    @patch('flaco.llm.ollama_client.requests.post')
    def test_chat_timeout(self, mock_post):
        """Test timeout handling"""
        import requests
        mock_post.side_effect = requests.exceptions.Timeout("Timeout")

        messages = [{"role": "user", "content": "Hello"}]

        with self.assertRaises(Exception) as context:
            self.client.chat(messages, max_retries=1)

        self.assertIn("timed out", str(context.exception))

    @patch('flaco.llm.ollama_client.requests.post')
    def test_chat_model_not_found(self, mock_post):
        """Test 404 model not found"""
        import requests
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        messages = [{"role": "user", "content": "Hello"}]

        with self.assertRaises(Exception) as context:
            self.client.chat(messages, max_retries=1)

        self.assertIn("not found", str(context.exception))

    @patch('flaco.llm.ollama_client.requests.get')
    def test_connection_test_success(self, mock_get):
        """Test connection testing"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = self.client.test_connection()
        self.assertTrue(result)

    @patch('flaco.llm.ollama_client.requests.get')
    def test_connection_test_failure(self, mock_get):
        """Test connection failure"""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()

        result = self.client.test_connection()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
