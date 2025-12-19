"""
Model Context Protocol (MCP) Client

This module provides integration with MCP servers to extend Flaco's capabilities.
MCP is a protocol for connecting AI assistants to external data sources and tools.
"""

import json
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path


class MCPClient:
    """Client for Model Context Protocol servers"""

    def __init__(self):
        self.servers: Dict[str, Dict[str, Any]] = {}
        self.load_server_config()

    def load_server_config(self):
        """Load MCP server configuration from .flaco/mcp.json"""
        config_path = Path.cwd() / ".flaco" / "mcp.json"

        if not config_path.exists():
            return

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.servers = config.get("mcpServers", {})
        except Exception as e:
            print(f"Warning: Error loading MCP config: {str(e)}")

    def get_available_servers(self) -> List[str]:
        """Get list of configured MCP servers"""
        return list(self.servers.keys())

    def call_server(
        self,
        server_name: str,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Call an MCP server method

        Args:
            server_name: Name of the MCP server
            method: Method to call
            params: Parameters for the method

        Returns:
            Response from the server
        """
        if server_name not in self.servers:
            raise ValueError(f"Unknown MCP server: {server_name}")

        server_config = self.servers[server_name]
        command = server_config.get("command")
        args = server_config.get("args", [])

        if not command:
            raise ValueError(f"No command configured for server: {server_name}")

        # Build the request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }

        try:
            # Execute the server command
            process = subprocess.Popen(
                [command] + args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Send request and get response
            stdout, stderr = process.communicate(
                input=json.dumps(request),
                timeout=30
            )

            if stderr:
                print(f"MCP Server stderr: {stderr}")

            # Parse response
            response = json.loads(stdout)
            return response

        except subprocess.TimeoutExpired:
            raise Exception(f"MCP server {server_name} timed out")
        except Exception as e:
            raise Exception(f"Error calling MCP server: {str(e)}")

    def list_tools(self, server_name: str) -> List[Dict[str, Any]]:
        """List available tools from an MCP server"""
        try:
            response = self.call_server(server_name, "tools/list")
            return response.get("result", {}).get("tools", [])
        except Exception as e:
            print(f"Error listing tools from {server_name}: {str(e)}")
            return []

    def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Any:
        """Call a tool on an MCP server"""
        params = {
            "name": tool_name,
            "arguments": arguments
        }

        response = self.call_server(server_name, "tools/call", params)
        return response.get("result")


# Example MCP configuration format:
# .flaco/mcp.json
"""
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token"
      }
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"]
    }
  }
}
"""
