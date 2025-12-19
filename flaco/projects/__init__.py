"""Project management and workspace organization"""

from .project_manager import ProjectManager, Project
from .git_auto import GitAutoVersioning

__all__ = ['ProjectManager', 'Project', 'GitAutoVersioning']
