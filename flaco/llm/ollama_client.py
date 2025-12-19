import json
import requests
from typing import List, Dict, Any, Optional, Generator
import base64
from pathlib import Path
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class OllamaClient:
    """
    Client for interacting with Ollama API with function calling support.

    Features:
    - Connection pooling for improved performance
    - Automatic retry with exponential backoff
    - Streaming and non-streaming chat support
    - Function calling (tool use) support
    - Conversation history management

    Performance:
    Uses connection pooling to reuse HTTP connections across requests,
    reducing latency and improving throughput.
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5-coder:7b"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.conversation_history: List[Dict[str, Any]] = []

        # Create session with connection pooling
        self.session = requests.Session()

        # Configure retry strategy for connection pooling
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,  # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )

        # Mount adapter with connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,  # Number of connection pools to cache
            pool_maxsize=20  # Maximum number of connections to save in the pool
        )

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def __del__(self):
        """Cleanup: close the session when the client is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """Send a chat request to Ollama with retry logic"""

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature,
            }
        }

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        if tools:
            payload["tools"] = tools

        last_error = None
        for attempt in range(max_retries):
            try:
                # Use session for connection pooling
                response = self.session.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=120  # Reduced from 300s to 120s
                )
                response.raise_for_status()

                if stream:
                    return self._handle_stream(response)
                else:
                    return response.json()

            except requests.exceptions.ConnectionError as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(
                        f"Failed to connect to Ollama at {self.base_url} after {max_retries} attempts.\n"
                        f"Please ensure Ollama is running:\n"
                        f"  - Run 'ollama serve' in a terminal\n"
                        f"  - Or check if Ollama is running on a different port\n"
                        f"  - Use --ollama-url flag to specify custom URL"
                    )
            except requests.exceptions.Timeout as e:
                last_error = e
                raise Exception(
                    f"Request to Ollama timed out after 120 seconds.\n"
                    f"The model '{self.model}' might be too large or slow.\n"
                    f"Try using a smaller model with the --model flag."
                )
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    raise Exception(
                        f"Model '{self.model}' not found on Ollama server.\n"
                        f"Available models can be listed with: ollama list\n"
                        f"Pull the model with: ollama pull {self.model}"
                    )
                else:
                    raise Exception(f"Ollama API error: {str(e)}")
            except requests.exceptions.RequestException as e:
                last_error = e
                raise Exception(f"Error communicating with Ollama: {str(e)}")

        # Should not reach here, but just in case
        raise Exception(f"Failed after {max_retries} retries: {last_error}")

    def _handle_stream(self, response) -> Generator[Dict[str, Any], None, None]:
        """Handle streaming responses from Ollama"""
        for line in response.iter_lines():
            if line:
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate a completion from a prompt"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
            }
        }

        if system:
            payload["system"] = system

        try:
            # Use session for connection pooling
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error communicating with Ollama: {str(e)}")

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models"""
        try:
            # Use session for connection pooling
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error listing models: {str(e)}")

    def encode_image(self, image_path: str) -> str:
        """Encode an image to base64 for multimodal support"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def chat_with_image(
        self,
        message: str,
        image_path: str,
        system: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a chat message with an image attachment"""

        image_data = self.encode_image(image_path)

        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        messages.append({
            "role": "user",
            "content": message,
            "images": [image_data]
        })

        return self.chat(messages)

    def test_connection(self) -> bool:
        """Test if Ollama server is accessible"""
        try:
            # Use session for connection pooling
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
