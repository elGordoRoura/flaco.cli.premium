"""Advanced project management system"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class ProjectType(Enum):
    """Project template types"""
    CUSTOM = "custom"
    WEB_FULLSTACK = "web_fullstack"
    API_BACKEND = "api_backend"
    FRONTEND_REACT = "frontend_react"
    PYTHON_CLI = "python_cli"
    DATA_SCIENCE = "data_science"
    MICROSERVICE = "microservice"
    MOBILE_APP = "mobile_app"


@dataclass
class Project:
    """Represents a Flaco project workspace"""
    name: str
    path: str
    project_type: str
    description: str
    created_at: str
    last_accessed: str
    git_enabled: bool
    auto_commit: bool
    conversation_id: Optional[str] = None
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Create from dictionary"""
        return cls(**data)


class ProjectManager:
    """Manage multiple Flaco project workspaces"""

    def __init__(self, config_dir: str = "~/.flaco"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(exist_ok=True)
        self.projects_file = self.config_dir / "projects.json"
        self.current_project_file = self.config_dir / "current_project.txt"
        self.projects: Dict[str, Project] = {}
        self.current_project: Optional[Project] = None
        self._load_projects()

    def _load_projects(self):
        """Load projects from config file"""
        if self.projects_file.exists():
            try:
                with open(self.projects_file, 'r') as f:
                    data = json.load(f)
                    self.projects = {
                        name: Project.from_dict(proj)
                        for name, proj in data.items()
                    }
            except Exception as e:
                print(f"Warning: Could not load projects: {e}")

        # Load current project
        if self.current_project_file.exists():
            try:
                with open(self.current_project_file, 'r') as f:
                    current_name = f.read().strip()
                    if current_name in self.projects:
                        self.current_project = self.projects[current_name]
            except Exception:
                pass

    def _save_projects(self):
        """Save projects to config file"""
        try:
            with open(self.projects_file, 'w') as f:
                data = {name: proj.to_dict() for name, proj in self.projects.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving projects: {e}")

    def _save_current_project(self):
        """Save current project reference"""
        try:
            with open(self.current_project_file, 'w') as f:
                if self.current_project:
                    f.write(self.current_project.name)
        except Exception as e:
            print(f"Error saving current project: {e}")

    def create_project(
        self,
        name: str,
        path: str,
        project_type: str = "custom",
        description: str = "",
        git_enabled: bool = True,
        auto_commit: bool = True,
        tags: List[str] = None
    ) -> Project:
        """Create a new project"""
        if name in self.projects:
            raise ValueError(f"Project '{name}' already exists")

        path = str(Path(path).resolve())

        # Create project directory if it doesn't exist
        Path(path).mkdir(parents=True, exist_ok=True)

        # Create .flaco project directory
        project_flaco_dir = Path(path) / ".flaco"
        project_flaco_dir.mkdir(exist_ok=True)

        # Create project metadata file
        metadata_file = project_flaco_dir / "project.json"

        now = datetime.now().isoformat()
        project = Project(
            name=name,
            path=path,
            project_type=project_type,
            description=description,
            created_at=now,
            last_accessed=now,
            git_enabled=git_enabled,
            auto_commit=auto_commit,
            tags=tags or []
        )

        # Save project metadata in project directory
        with open(metadata_file, 'w') as f:
            json.dump(project.to_dict(), f, indent=2)

        self.projects[name] = project
        self._save_projects()

        return project

    def switch_project(self, name: str) -> Project:
        """Switch to a different project"""
        if name not in self.projects:
            raise ValueError(f"Project '{name}' not found")

        project = self.projects[name]
        project.last_accessed = datetime.now().isoformat()
        self.current_project = project

        # Change working directory
        os.chdir(project.path)

        self._save_projects()
        self._save_current_project()

        return project

    def list_projects(self) -> List[Project]:
        """List all projects"""
        return list(self.projects.values())

    def get_project(self, name: str) -> Optional[Project]:
        """Get a specific project"""
        return self.projects.get(name)

    def delete_project(self, name: str, delete_files: bool = False):
        """Delete a project (optionally delete files)"""
        if name not in self.projects:
            raise ValueError(f"Project '{name}' not found")

        project = self.projects[name]

        if delete_files:
            import shutil
            shutil.rmtree(project.path, ignore_errors=True)

        del self.projects[name]

        if self.current_project and self.current_project.name == name:
            self.current_project = None
            if self.current_project_file.exists():
                self.current_project_file.unlink()

        self._save_projects()

    def update_project(self, name: str, **kwargs):
        """Update project attributes"""
        if name not in self.projects:
            raise ValueError(f"Project '{name}' not found")

        project = self.projects[name]

        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)

        self._save_projects()

    def search_projects(self, query: str = None, tags: List[str] = None) -> List[Project]:
        """Search projects by name, description, or tags"""
        results = []

        for project in self.projects.values():
            match = True

            if query:
                query_lower = query.lower()
                if not (query_lower in project.name.lower() or
                       query_lower in project.description.lower()):
                    match = False

            if tags and match:
                if not any(tag in project.tags for tag in tags):
                    match = False

            if match:
                results.append(project)

        return results

    def get_project_stats(self, name: str) -> dict:
        """Get statistics for a project"""
        if name not in self.projects:
            raise ValueError(f"Project '{name}' not found")

        project = self.projects[name]
        path = Path(project.path)

        # Count files
        file_count = 0
        dir_count = 0
        total_size = 0

        try:
            for item in path.rglob("*"):
                if item.is_file():
                    file_count += 1
                    total_size += item.stat().st_size
                elif item.is_dir():
                    dir_count += 1
        except Exception:
            pass

        return {
            "name": project.name,
            "path": project.path,
            "files": file_count,
            "directories": dir_count,
            "size_bytes": total_size,
            "size_mb": round(total_size / (1024 * 1024), 2),
            "created": project.created_at,
            "last_accessed": project.last_accessed
        }

    def import_existing_project(self, path: str, name: str = None) -> Project:
        """Import an existing directory as a Flaco project"""
        path = str(Path(path).resolve())

        if not Path(path).exists():
            raise ValueError(f"Path does not exist: {path}")

        # Use directory name if no name provided
        if not name:
            name = Path(path).name

        # Auto-detect project type
        from ..intelligence import ProjectScanner
        scanner = ProjectScanner(path)
        insight = scanner.scan()

        project_type = insight.project_type.value
        description = f"Imported {insight.framework or project_type} project"

        # Check if git is already initialized
        git_enabled = (Path(path) / ".git").exists()

        return self.create_project(
            name=name,
            path=path,
            project_type=project_type,
            description=description,
            git_enabled=git_enabled,
            auto_commit=False  # Don't auto-commit on existing projects by default
        )

    def create_from_template(self, name: str, template: ProjectType, path: str = None) -> Project:
        """Create a project from a template"""
        if not path:
            path = str(Path.cwd() / name)

        templates = {
            ProjectType.WEB_FULLSTACK: {
                "type": "web_fullstack",
                "description": "Full-stack web application",
                "tags": ["web", "fullstack"]
            },
            ProjectType.API_BACKEND: {
                "type": "api_backend",
                "description": "REST API backend service",
                "tags": ["api", "backend"]
            },
            ProjectType.FRONTEND_REACT: {
                "type": "frontend_react",
                "description": "React frontend application",
                "tags": ["frontend", "react"]
            },
            ProjectType.PYTHON_CLI: {
                "type": "python_cli",
                "description": "Python CLI application",
                "tags": ["python", "cli"]
            },
            ProjectType.DATA_SCIENCE: {
                "type": "data_science",
                "description": "Data science / ML project",
                "tags": ["data", "ml"]
            },
            ProjectType.MICROSERVICE: {
                "type": "microservice",
                "description": "Microservice architecture",
                "tags": ["microservice", "api"]
            },
        }

        template_config = templates.get(template, {
            "type": "custom",
            "description": "Custom project",
            "tags": []
        })

        return self.create_project(
            name=name,
            path=path,
            project_type=template_config["type"],
            description=template_config["description"],
            tags=template_config["tags"]
        )
