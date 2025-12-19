"""Smart auto-git versioning with intelligent commits"""

import subprocess
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class GitChange:
    """Represents a git change"""
    file_path: str
    change_type: str  # 'added', 'modified', 'deleted'
    lines_added: int = 0
    lines_deleted: int = 0


@dataclass
class GitCommit:
    """Represents a git commit"""
    hash: str
    message: str
    author: str
    date: str
    files_changed: int


class GitAutoVersioning:
    """Smart automatic git versioning system"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.auto_commit_enabled = False
        self.auto_push_enabled = False
        self.commit_prefix = "🤖 Flaco:"

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    def init_repo(self) -> bool:
        """Initialize a new git repository"""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )

            # Create initial .gitignore
            gitignore_path = self.repo_path / ".gitignore"
            if not gitignore_path.exists():
                gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Node
node_modules/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Flaco
.flaco_todos.json
.flaco_history
"""
                with open(gitignore_path, 'w') as f:
                    f.write(gitignore_content)

            return True
        except Exception as e:
            print(f"Error initializing git repo: {e}")
            return False

    def get_changes(self) -> List[GitChange]:
        """Get current uncommitted changes"""
        if not self.is_git_repo():
            return []

        changes = []

        try:
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                status = line[:2]
                file_path = line[3:].strip()

                if status.strip() in ['A', '??']:
                    change_type = 'added'
                elif status.strip() == 'M':
                    change_type = 'modified'
                elif status.strip() == 'D':
                    change_type = 'deleted'
                else:
                    change_type = 'modified'

                changes.append(GitChange(
                    file_path=file_path,
                    change_type=change_type
                ))

        except Exception as e:
            print(f"Error getting git changes: {e}")

        return changes

    def analyze_changes(self, changes: List[GitChange]) -> Dict[str, any]:
        """Analyze changes to generate intelligent commit message"""
        if not changes:
            return {"summary": "No changes", "details": []}

        # Categorize changes
        added = [c for c in changes if c.change_type == 'added']
        modified = [c for c in changes if c.change_type == 'modified']
        deleted = [c for c in changes if c.change_type == 'deleted']

        # Detect patterns
        file_types = {}
        for change in changes:
            ext = Path(change.file_path).suffix or 'no_extension'
            file_types[ext] = file_types.get(ext, 0) + 1

        # Detect what was changed
        categories = {
            'config': ['.json', '.yaml', '.yml', '.toml', '.ini', '.env'],
            'python': ['.py'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx'],
            'styles': ['.css', '.scss', '.sass'],
            'docs': ['.md', '.txt', '.rst'],
            'test': ['test_', '_test', '.test.', '.spec.']
        }

        detected_categories = set()
        for change in changes:
            file_lower = change.file_path.lower()
            ext = Path(change.file_path).suffix

            for category, patterns in categories.items():
                if any(pattern in file_lower or pattern == ext for pattern in patterns):
                    detected_categories.add(category)

        # Generate summary
        parts = []
        if added:
            parts.append(f"add {len(added)} file(s)")
        if modified:
            parts.append(f"update {len(modified)} file(s)")
        if deleted:
            parts.append(f"remove {len(deleted)} file(s)")

        action_summary = ", ".join(parts)

        # Add category context
        if detected_categories:
            category_str = ", ".join(sorted(detected_categories))
            action_summary += f" ({category_str})"

        return {
            "summary": action_summary,
            "added": len(added),
            "modified": len(modified),
            "deleted": len(deleted),
            "categories": list(detected_categories),
            "details": [f"  - {c.change_type}: {c.file_path}" for c in changes[:10]]
        }

    def generate_commit_message(self, changes: List[GitChange], context: str = "") -> str:
        """Generate an intelligent commit message"""
        analysis = self.analyze_changes(changes)

        # Base message
        message = f"{self.commit_prefix} {analysis['summary']}"

        # Add context if provided
        if context:
            message += f"\n\n{context}"

        # Add file details for important changes
        if analysis['details'] and len(changes) <= 5:
            message += "\n\nChanges:\n" + "\n".join(analysis['details'])

        return message

    def auto_commit(self, message: str = None, add_all: bool = True) -> Tuple[bool, str]:
        """Automatically commit changes with smart message"""
        if not self.is_git_repo():
            return False, "Not a git repository"

        changes = self.get_changes()
        if not changes:
            return False, "No changes to commit"

        try:
            # Add files
            if add_all:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.repo_path,
                    capture_output=True,
                    check=True,
                    timeout=10
                )
            else:
                # Add only tracked files
                for change in changes:
                    subprocess.run(
                        ["git", "add", change.file_path],
                        cwd=self.repo_path,
                        capture_output=True,
                        timeout=10
                    )

            # Generate or use provided message
            if not message:
                message = self.generate_commit_message(changes)

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, f"Committed: {message.split(chr(10))[0]}"
            else:
                return False, f"Commit failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Git command timed out"
        except Exception as e:
            return False, f"Error during commit: {str(e)}"

    def auto_push(self, branch: str = None) -> Tuple[bool, str]:
        """Automatically push commits to remote"""
        if not self.is_git_repo():
            return False, "Not a git repository"

        try:
            # Get current branch if not specified
            if not branch:
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=self.repo_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                branch = result.stdout.strip()

            # Push
            result = subprocess.run(
                ["git", "push", "origin", branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return True, f"Pushed to {branch}"
            else:
                return False, f"Push failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Git push timed out"
        except Exception as e:
            return False, f"Error during push: {str(e)}"

    def get_commit_history(self, limit: int = 10) -> List[GitCommit]:
        """Get recent commit history"""
        if not self.is_git_repo():
            return []

        commits = []

        try:
            result = subprocess.run(
                ["git", "log", f"-{limit}", "--pretty=format:%H|%s|%an|%ar|%h", "--stat"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            for line in result.stdout.split('\n'):
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        commits.append(GitCommit(
                            hash=parts[0][:8],
                            message=parts[1],
                            author=parts[2],
                            date=parts[3],
                            files_changed=0
                        ))

        except Exception as e:
            print(f"Error getting commit history: {e}")

        return commits

    def rollback_to_commit(self, commit_hash: str, hard: bool = False) -> Tuple[bool, str]:
        """Rollback to a specific commit"""
        if not self.is_git_repo():
            return False, "Not a git repository"

        try:
            reset_type = "--hard" if hard else "--soft"

            result = subprocess.run(
                ["git", "reset", reset_type, commit_hash],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, f"Rolled back to {commit_hash}"
            else:
                return False, f"Rollback failed: {result.stderr}"

        except Exception as e:
            return False, f"Error during rollback: {str(e)}"

    def create_branch(self, branch_name: str, switch: bool = True) -> Tuple[bool, str]:
        """Create a new git branch"""
        if not self.is_git_repo():
            return False, "Not a git repository"

        try:
            # Create branch
            subprocess.run(
                ["git", "branch", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                check=True,
                timeout=5
            )

            # Switch to branch if requested
            if switch:
                subprocess.run(
                    ["git", "checkout", branch_name],
                    cwd=self.repo_path,
                    capture_output=True,
                    check=True,
                    timeout=5
                )

            return True, f"Created branch: {branch_name}"

        except Exception as e:
            return False, f"Error creating branch: {str(e)}"

    def get_current_branch(self) -> Optional[str]:
        """Get current git branch"""
        if not self.is_git_repo():
            return None

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception:
            return None

    def get_repo_stats(self) -> Dict[str, any]:
        """Get repository statistics"""
        if not self.is_git_repo():
            return {}

        stats = {
            "is_repo": True,
            "has_remote": False,
            "branch": self.get_current_branch(),
            "uncommitted_changes": len(self.get_changes()),
            "total_commits": 0
        }

        try:
            # Check for remote
            result = subprocess.run(
                ["git", "remote", "-v"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            stats["has_remote"] = bool(result.stdout.strip())

            # Count commits
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                stats["total_commits"] = int(result.stdout.strip())

        except Exception:
            pass

        return stats
