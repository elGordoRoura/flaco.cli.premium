"""
Code snippets library for quick code generation.

This module provides a comprehensive library of code snippets for various
programming languages and frameworks, making Flaco competitive with tools
like GitHub Copilot and Claude.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class SnippetCategory(Enum):
    """Categories for organizing code snippets"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    REACT = "react"
    FASTAPI = "fastapi"
    DJANGO = "django"
    SQL = "sql"
    DOCKER = "docker"
    GIT = "git"
    TESTING = "testing"
    ALGORITHMS = "algorithms"
    PATTERNS = "patterns"


@dataclass
class CodeSnippet:
    """Represents a reusable code snippet"""
    name: str
    description: str
    code: str
    language: str
    category: SnippetCategory
    tags: List[str]
    variables: Optional[Dict[str, str]] = None  # Variables to replace in template


class SnippetLibrary:
    """
    Manages a library of code snippets for quick access.

    Makes Flaco competitive by providing instant access to common patterns
    without needing to search documentation or Stack Overflow.
    """

    def __init__(self):
        self.snippets: Dict[str, CodeSnippet] = {}
        self._load_default_snippets()

    def _load_default_snippets(self):
        """Load default snippet library"""

        # Python snippets
        self.add_snippet(CodeSnippet(
            name="fastapi_endpoint",
            description="FastAPI REST endpoint with validation",
            code="""@app.{{method}}("/{{path}}")
async def {{function_name}}({{params}}):
    \"\"\"{{description}}\"\"\"
    try:
        # Your logic here
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))""",
            language="python",
            category=SnippetCategory.FASTAPI,
            tags=["api", "endpoint", "rest"],
            variables={"method": "post", "path": "items", "function_name": "create_item", "params": "item: Item", "description": "Create a new item"}
        ))

        self.add_snippet(CodeSnippet(
            name="async_retry",
            description="Async function with retry logic",
            code="""async def {{function_name}}({{params}}, max_retries: int = 3):
    \"\"\"{{description}}\"\"\"
    for attempt in range(max_retries):
        try:
            # Your async operation here
            result = await {{operation}}
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff""",
            language="python",
            category=SnippetCategory.PYTHON,
            tags=["async", "retry", "resilience"],
            variables={"function_name": "fetch_data", "params": "url: str", "description": "Fetch data with retry", "operation": "fetch(url)"}
        ))

        self.add_snippet(CodeSnippet(
            name="context_manager",
            description="Python context manager class",
            code="""class {{class_name}}:
    \"\"\"{{description}}\"\"\"

    def __init__(self, {{params}}):
        self.{{attribute}} = {{value}}

    def __enter__(self):
        # Setup logic
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup logic
        if exc_type is not None:
            # Handle exception
            return False
        return True""",
            language="python",
            category=SnippetCategory.PYTHON,
            tags=["context-manager", "resource-management"],
            variables={"class_name": "ResourceManager", "description": "Manage resource lifecycle", "params": "resource", "attribute": "resource", "value": "resource"}
        ))

        # React snippets
        self.add_snippet(CodeSnippet(
            name="react_component",
            description="React functional component with hooks",
            code="""import React, { useState, useEffect } from 'react';

interface {{ComponentName}}Props {
  {{propName}}: {{propType}};
}

const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({ {{propName}} }) => {
  const [{{stateName}}, set{{StateNameCapitalized}}] = useState<{{stateType}}>({{initialValue}});

  useEffect(() => {
    // Effect logic here
    return () => {
      // Cleanup logic here
    };
  }, [{{dependencies}}]);

  return (
    <div className="{{className}}">
      {/* Component JSX */}
    </div>
  );
};

export default {{ComponentName}};""",
            language="typescript",
            category=SnippetCategory.REACT,
            tags=["react", "component", "hooks"],
            variables={"ComponentName": "MyComponent", "propName": "data", "propType": "string", "stateName": "value", "StateNameCapitalized": "Value", "stateType": "string", "initialValue": "''", "dependencies": "propName", "className": "my-component"}
        ))

        self.add_snippet(CodeSnippet(
            name="react_custom_hook",
            description="Custom React hook",
            code="""import { useState, useEffect } from 'react';

interface Use{{HookName}}Options {
  {{optionName}}?: {{optionType}};
}

export const use{{HookName}} = ({{params}}: Use{{HookName}}Options = {}) => {
  const [{{stateName}}, set{{StateNameCapitalized}}] = useState<{{stateType}}>({{initialValue}});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    // Hook logic here
    setLoading(true);

    // Your async operation
    Promise.resolve()
      .then(result => {
        set{{StateNameCapitalized}}(result);
      })
      .catch(err => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [{{dependencies}}]);

  return { {{stateName}}, loading, error };
};""",
            language="typescript",
            category=SnippetCategory.REACT,
            tags=["react", "hook", "custom"],
            variables={"HookName": "FetchData", "optionName": "url", "optionType": "string", "params": "options", "stateName": "data", "StateNameCapitalized": "Data", "stateType": "any", "initialValue": "null", "dependencies": "options.url"}
        ))

        # Docker snippets
        self.add_snippet(CodeSnippet(
            name="dockerfile_python",
            description="Production-ready Python Dockerfile",
            code="""FROM python:{{python_version}}-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE {{port}}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD python -c "import requests; requests.get('http://localhost:{{port}}/health')"

# Run application
CMD ["python", "{{entrypoint}}"]""",
            language="dockerfile",
            category=SnippetCategory.DOCKER,
            tags=["docker", "python", "production"],
            variables={"python_version": "3.11", "port": "8000", "entrypoint": "main.py"}
        ))

        # Testing snippets
        self.add_snippet(CodeSnippet(
            name="pytest_fixture",
            description="Pytest fixture with cleanup",
            code="""import pytest

@pytest.fixture(scope="{{scope}}")
def {{fixture_name}}():
    \"\"\"{{description}}\"\"\"
    # Setup
    {{resource}} = {{setup_code}}

    yield {{resource}}

    # Teardown
    {{cleanup_code}}""",
            language="python",
            category=SnippetCategory.TESTING,
            tags=["pytest", "fixture", "testing"],
            variables={"scope": "function", "fixture_name": "database", "description": "Database fixture", "resource": "db", "setup_code": "create_database()", "cleanup_code": "db.close()"}
        ))

        self.add_snippet(CodeSnippet(
            name="mock_test",
            description="Unit test with mocking",
            code="""import pytest
from unittest.mock import Mock, patch, MagicMock

def test_{{function_name}}():
    \"\"\"Test {{description}}\"\"\"
    # Arrange
    {{mock_name}} = Mock()
    {{mock_name}}.{{method}}.return_value = {{return_value}}

    # Act
    result = {{function_under_test}}({{mock_name}})

    # Assert
    assert result == {{expected}}
    {{mock_name}}.{{method}}.assert_called_once_with({{expected_args}})""",
            language="python",
            category=SnippetCategory.TESTING,
            tags=["pytest", "mock", "unit-test"],
            variables={"function_name": "function_with_dependency", "description": "function behavior with mocked dependency", "mock_name": "mock_service", "method": "get_data", "return_value": "{'key': 'value'}", "function_under_test": "process_data", "expected": "expected_result", "expected_args": "arg1, arg2"}
        ))

        # Algorithm snippets
        self.add_snippet(CodeSnippet(
            name="binary_search",
            description="Binary search algorithm",
            code="""def binary_search(arr: List[{{type}}], target: {{type}}) -> int:
    \"\"\"
    Binary search algorithm - O(log n) time complexity.

    Args:
        arr: Sorted list to search in
        target: Value to find

    Returns:
        Index of target if found, -1 otherwise
    \"\"\"
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Not found""",
            language="python",
            category=SnippetCategory.ALGORITHMS,
            tags=["algorithm", "search", "binary-search"],
            variables={"type": "int"}
        ))

        # Git workflow snippets
        self.add_snippet(CodeSnippet(
            name="git_feature_workflow",
            description="Git feature branch workflow",
            code="""# Create and switch to feature branch
git checkout -b feature/{{feature_name}}

# Make your changes and commit
git add .
git commit -m "{{commit_message}}"

# Update with latest main
git fetch origin
git rebase origin/main

# Push feature branch
git push -u origin feature/{{feature_name}}

# Create pull request (GitHub CLI)
gh pr create --title "{{pr_title}}" --body "{{pr_description}}"

# After PR approved, merge and cleanup
git checkout main
git pull origin main
git branch -d feature/{{feature_name}}""",
            language="bash",
            category=SnippetCategory.GIT,
            tags=["git", "workflow", "feature-branch"],
            variables={"feature_name": "new-feature", "commit_message": "Add new feature", "pr_title": "Add new feature", "pr_description": "Implements new feature"}
        ))

    def add_snippet(self, snippet: CodeSnippet):
        """Add a snippet to the library"""
        self.snippets[snippet.name] = snippet

    def get_snippet(self, name: str) -> Optional[CodeSnippet]:
        """Get a snippet by name"""
        return self.snippets.get(name)

    def search_snippets(self, query: str = "", category: Optional[SnippetCategory] = None, tags: Optional[List[str]] = None) -> List[CodeSnippet]:
        """
        Search snippets by query, category, or tags.

        Args:
            query: Search term to match in name or description
            category: Filter by category
            tags: Filter by tags (match any)

        Returns:
            List of matching snippets
        """
        results = []
        query_lower = query.lower()

        for snippet in self.snippets.values():
            # Category filter
            if category and snippet.category != category:
                continue

            # Tags filter
            if tags and not any(tag in snippet.tags for tag in tags):
                continue

            # Query filter
            if query:
                if query_lower not in snippet.name.lower() and query_lower not in snippet.description.lower():
                    continue

            results.append(snippet)

        return results

    def list_categories(self) -> List[str]:
        """List all available categories"""
        return [cat.value for cat in SnippetCategory]

    def render_snippet(self, name: str, variables: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Render a snippet with variable substitution.

        Args:
            name: Snippet name
            variables: Dictionary of variables to substitute

        Returns:
            Rendered code with variables substituted, or None if snippet not found
        """
        snippet = self.get_snippet(name)
        if not snippet:
            return None

        code = snippet.code

        # Use provided variables or defaults
        vars_to_use = variables or snippet.variables or {}

        # Simple variable substitution
        for var_name, var_value in vars_to_use.items():
            placeholder = f"{{{{{var_name}}}}}"
            code = code.replace(placeholder, str(var_value))

        return code


# Global snippet library instance
snippet_library = SnippetLibrary()
