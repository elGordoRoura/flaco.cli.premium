import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

# Default template used when no FLACO.md template file is found on disk
DEFAULT_FLACO_TEMPLATE = """---
project: Your Project
version: 0.1.0
---

# Project Overview
- Purpose:
- Key components:

# Conventions
- Language/style:
- Testing:
- Deployment:

# Constraints
- Dependencies:
- Security considerations:
"""


class FlacoContextLoader:
    """Loads and manages FLACO.md context file for persistent project guidelines"""

    def __init__(self, search_path: Optional[str] = None):
        self.search_path = search_path or os.getcwd()
        self.context_file = self._find_context_file()
        self.context_data: Optional[Dict[str, Any]] = None

    def _find_context_file(self) -> Optional[str]:
        """Search for FLACO.md in current directory and parent directories"""
        current = Path(self.search_path).resolve()

        # Search up the directory tree
        for parent in [current] + list(current.parents):
            flaco_md = parent / "FLACO.md"
            if flaco_md.exists():
                return str(flaco_md)

        return None

    def load_context(self) -> Optional[str]:
        """Load the FLACO.md file and return its contents"""
        if not self.context_file:
            return None

        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter if it exists
            self._parse_frontmatter(content)

            return content

        except Exception as e:
            print(f"Warning: Error loading FLACO.md: {str(e)}")
            return None

    def _parse_frontmatter(self, content: str):
        """Parse YAML frontmatter from FLACO.md if present"""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    self.context_data = yaml.safe_load(parts[1])
                except yaml.YAMLError:
                    self.context_data = {}

    def get_system_prompt_addition(self) -> str:
        """Get the context to add to the system prompt"""
        context = self.load_context()
        if not context:
            return ""

        return f"""

# Project Context (from FLACO.md)

The following is the project-specific context loaded from FLACO.md in the repository.
This provides important guidelines, conventions, and information about this specific project.

{context}

---

Please follow all guidelines and conventions specified in the FLACO.md context above when working on this project.
"""

    def get_metadata(self) -> Dict[str, Any]:
        """Get parsed metadata from frontmatter"""
        if self.context_data is None:
            self.load_context()
        return self.context_data or {}

    def has_context(self) -> bool:
        """Check if FLACO.md exists"""
        return self.context_file is not None

    def get_context_path(self) -> Optional[str]:
        """Get the path to the FLACO.md file"""
        return self.context_file

    def create_context_file(
        self,
        target_dir: Optional[str] = None,
        template_path: Optional[str] = None,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """Create a FLACO.md file from a template or default content.

        Args:
            target_dir: Directory to place FLACO.md (defaults to search_path/cwd)
            template_path: Optional path to a template file
            overwrite: Allow overwriting an existing file

        Returns:
            Dict with success flag, exists flag, and file path
        """
        target_dir = Path(target_dir or self.search_path).resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        destination = target_dir / "FLACO.md"

        if destination.exists() and not overwrite:
            return {"success": False, "exists": True, "path": str(destination)}

        # Choose template: explicit path, repo docs template, or default fallback
        template_content: Optional[str] = None
        template_candidate = None

        if template_path:
            template_candidate = Path(template_path)
        else:
            repo_root = Path(__file__).resolve().parent.parent.parent
            repo_template = repo_root / "docs" / "FLACO.md.template"
            if repo_template.exists():
                template_candidate = repo_template

        if template_candidate and template_candidate.exists():
            template_content = template_candidate.read_text(encoding="utf-8")
        else:
            template_content = DEFAULT_FLACO_TEMPLATE

        destination.write_text(template_content, encoding="utf-8")
        self.context_file = str(destination)

        return {"success": True, "exists": False, "path": str(destination)}
