"""Smart project detection and analysis system"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class ProjectType(Enum):
    """Detected project types"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    DJANGO = "django"
    FLASK = "flask"
    FASTAPI = "fastapi"
    NODEJS = "nodejs"
    RUST = "rust"
    GO = "go"
    JAVA = "java"
    UNKNOWN = "unknown"


@dataclass
class ProjectInsight:
    """Insights about a detected project"""
    project_type: ProjectType
    framework: Optional[str]
    languages: List[str]
    dependencies: Dict[str, str]
    entry_points: List[str]
    config_files: List[str]
    test_framework: Optional[str]
    has_ci: bool
    has_docker: bool
    has_tests: bool
    file_count: int
    total_lines: int
    suggestions: List[str]
    health_score: float  # 0-100


class ProjectScanner:
    """Automatically scan and understand project structure"""

    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.insight: Optional[ProjectInsight] = None

    def scan(self) -> ProjectInsight:
        """Perform a full project scan"""
        # Detect project type and framework
        project_type, framework = self._detect_project_type()

        # Scan for languages
        languages = self._detect_languages()

        # Parse dependencies
        dependencies = self._parse_dependencies(project_type)

        # Find entry points
        entry_points = self._find_entry_points(project_type)

        # Find config files
        config_files = self._find_config_files()

        # Detect testing framework
        test_framework = self._detect_test_framework(project_type)

        # Check for CI/CD
        has_ci = self._has_ci_cd()

        # Check for Docker
        has_docker = self._has_docker()

        # Check for tests
        has_tests = self._has_tests(project_type)

        # Count files and lines
        file_count, total_lines = self._count_code()

        # Generate suggestions
        suggestions = self._generate_suggestions(
            project_type, has_tests, has_ci, has_docker, test_framework
        )

        # Calculate health score
        health_score = self._calculate_health_score(
            has_tests, has_ci, has_docker, test_framework, len(config_files)
        )

        self.insight = ProjectInsight(
            project_type=project_type,
            framework=framework,
            languages=languages,
            dependencies=dependencies,
            entry_points=entry_points,
            config_files=config_files,
            test_framework=test_framework,
            has_ci=has_ci,
            has_docker=has_docker,
            has_tests=has_tests,
            file_count=file_count,
            total_lines=total_lines,
            suggestions=suggestions,
            health_score=health_score
        )

        return self.insight

    def _detect_project_type(self) -> tuple[ProjectType, Optional[str]]:
        """Detect the primary project type and framework"""
        # Check for Python frameworks
        if (self.root_path / "manage.py").exists():
            return ProjectType.DJANGO, "Django"

        if (self.root_path / "app.py").exists() or self._has_file_with_content("from flask import"):
            return ProjectType.FLASK, "Flask"

        if self._has_file_with_content("from fastapi import") or self._has_file_with_content("import fastapi"):
            return ProjectType.FASTAPI, "FastAPI"

        # Check for JavaScript/TypeScript frameworks
        package_json = self.root_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                    if 'react' in deps:
                        return ProjectType.REACT, "React"
                    if 'vue' in deps:
                        return ProjectType.VUE, "Vue"
                    if '@angular/core' in deps:
                        return ProjectType.ANGULAR, "Angular"
                    if 'next' in deps:
                        return ProjectType.REACT, "Next.js"

                    # Generic Node.js
                    return ProjectType.NODEJS, "Node.js"
            except:
                pass

        # Check for other languages
        if (self.root_path / "Cargo.toml").exists():
            return ProjectType.RUST, "Rust"

        if (self.root_path / "go.mod").exists():
            return ProjectType.GO, "Go"

        if (self.root_path / "pom.xml").exists() or (self.root_path / "build.gradle").exists():
            return ProjectType.JAVA, "Java"

        # Check for Python by requirements or setup.py
        if (self.root_path / "requirements.txt").exists() or (self.root_path / "setup.py").exists() or (self.root_path / "pyproject.toml").exists():
            return ProjectType.PYTHON, "Python"

        # Check for TypeScript
        if (self.root_path / "tsconfig.json").exists():
            return ProjectType.TYPESCRIPT, "TypeScript"

        return ProjectType.UNKNOWN, None

    def _detect_languages(self) -> List[str]:
        """Detect programming languages used"""
        languages = set()

        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React/JSX',
            '.tsx': 'TypeScript/React',
            '.rs': 'Rust',
            '.go': 'Go',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin'
        }

        for ext, lang in extensions.items():
            if self._has_files_with_extension(ext):
                languages.add(lang)

        return list(languages) if languages else ['Unknown']

    def _parse_dependencies(self, project_type: ProjectType) -> Dict[str, str]:
        """Parse project dependencies"""
        deps = {}

        if project_type in [ProjectType.PYTHON, ProjectType.DJANGO, ProjectType.FLASK, ProjectType.FASTAPI]:
            req_file = self.root_path / "requirements.txt"
            if req_file.exists():
                with open(req_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '==' in line:
                                name, version = line.split('==', 1)
                                deps[name.strip()] = version.strip()
                            else:
                                deps[line] = 'latest'

        elif project_type in [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT, ProjectType.REACT, ProjectType.VUE, ProjectType.ANGULAR, ProjectType.NODEJS]:
            package_json = self.root_path / "package.json"
            if package_json.exists():
                with open(package_json, 'r') as f:
                    pkg = json.load(f)
                    deps.update(pkg.get('dependencies', {}))

        return deps

    def _find_entry_points(self, project_type: ProjectType) -> List[str]:
        """Find main entry points of the application"""
        entry_points = []

        common_entry_files = [
            'main.py', 'app.py', 'server.py', 'manage.py',
            'index.js', 'index.ts', 'server.js', 'app.js',
            'main.rs', 'main.go', 'Main.java'
        ]

        for file in common_entry_files:
            if (self.root_path / file).exists():
                entry_points.append(file)

        return entry_points

    def _find_config_files(self) -> List[str]:
        """Find configuration files"""
        config_files = []

        common_configs = [
            '.env', '.env.example', 'config.py', 'settings.py',
            'package.json', 'tsconfig.json', 'webpack.config.js',
            'Dockerfile', 'docker-compose.yml', '.gitignore',
            'requirements.txt', 'pyproject.toml', 'setup.py',
            'Cargo.toml', 'go.mod', 'pom.xml'
        ]

        for config in common_configs:
            if (self.root_path / config).exists():
                config_files.append(config)

        return config_files

    def _detect_test_framework(self, project_type: ProjectType) -> Optional[str]:
        """Detect testing framework"""
        if project_type in [ProjectType.PYTHON, ProjectType.DJANGO, ProjectType.FLASK, ProjectType.FASTAPI]:
            if self._has_file_with_content("import pytest") or (self.root_path / "pytest.ini").exists():
                return "pytest"
            if self._has_file_with_content("import unittest"):
                return "unittest"

        elif project_type in [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT, ProjectType.REACT, ProjectType.VUE, ProjectType.NODEJS]:
            package_json = self.root_path / "package.json"
            if package_json.exists():
                with open(package_json, 'r') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                    if 'jest' in deps:
                        return "Jest"
                    if 'mocha' in deps:
                        return "Mocha"
                    if 'vitest' in deps:
                        return "Vitest"

        return None

    def _has_ci_cd(self) -> bool:
        """Check if CI/CD is configured"""
        ci_indicators = [
            '.github/workflows',
            '.gitlab-ci.yml',
            '.circleci',
            'Jenkinsfile',
            '.travis.yml',
            'azure-pipelines.yml'
        ]

        for indicator in ci_indicators:
            if (self.root_path / indicator).exists():
                return True

        return False

    def _has_docker(self) -> bool:
        """Check if Docker is configured"""
        return (self.root_path / "Dockerfile").exists() or (self.root_path / "docker-compose.yml").exists()

    def _has_tests(self, project_type: ProjectType) -> bool:
        """Check if project has tests"""
        test_indicators = ['tests/', 'test/', '__tests__/', 'spec/']

        for indicator in test_indicators:
            if (self.root_path / indicator).exists():
                return True

        # Check for test files
        if project_type in [ProjectType.PYTHON, ProjectType.DJANGO, ProjectType.FLASK, ProjectType.FASTAPI]:
            return self._has_files_matching("test_*.py") or self._has_files_matching("*_test.py")

        elif project_type in [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT, ProjectType.REACT, ProjectType.VUE, ProjectType.NODEJS]:
            return self._has_files_matching("*.test.js") or self._has_files_matching("*.spec.js")

        return False

    def _count_code(self) -> tuple[int, int]:
        """Count files and lines of code"""
        file_count = 0
        total_lines = 0

        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.rs', '.go', '.java', '.c', '.cpp'}

        try:
            for root, dirs, files in os.walk(self.root_path):
                # Skip common directories
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build', '.next'}]

                for file in files:
                    if any(file.endswith(ext) for ext in code_extensions):
                        file_count += 1
                        try:
                            with open(Path(root) / file, 'r', encoding='utf-8', errors='ignore') as f:
                                total_lines += sum(1 for _ in f)
                        except:
                            pass
        except:
            pass

        return file_count, total_lines

    def _generate_suggestions(self, project_type: ProjectType, has_tests: bool, has_ci: bool, has_docker: bool, test_framework: Optional[str]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        if not has_tests:
            if project_type in [ProjectType.PYTHON, ProjectType.DJANGO, ProjectType.FLASK, ProjectType.FASTAPI]:
                suggestions.append("📝 Add tests using pytest for better code reliability")
            elif project_type in [ProjectType.JAVASCRIPT, ProjectType.TYPESCRIPT, ProjectType.REACT, ProjectType.VUE]:
                suggestions.append("📝 Add tests using Jest or Vitest for better code quality")

        if not has_ci:
            suggestions.append("🔄 Set up CI/CD with GitHub Actions for automated testing")

        if not has_docker:
            suggestions.append("🐳 Add Docker configuration for consistent deployment")

        if not (self.root_path / ".gitignore").exists():
            suggestions.append("📁 Add .gitignore to exclude unnecessary files from version control")

        if not (self.root_path / "README.md").exists():
            suggestions.append("📖 Create a README.md to document your project")

        return suggestions

    def _calculate_health_score(self, has_tests: bool, has_ci: bool, has_docker: bool, test_framework: Optional[str], config_count: int) -> float:
        """Calculate project health score (0-100)"""
        score = 50.0  # Base score

        if has_tests:
            score += 20
        if test_framework:
            score += 10
        if has_ci:
            score += 10
        if has_docker:
            score += 5
        if config_count >= 3:
            score += 5

        return min(score, 100.0)

    def _has_files_with_extension(self, extension: str) -> bool:
        """Check if any files with extension exist"""
        try:
            for root, dirs, files in os.walk(self.root_path):
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '__pycache__'}]
                if any(f.endswith(extension) for f in files):
                    return True
        except:
            pass
        return False

    def _has_files_matching(self, pattern: str) -> bool:
        """Check if files matching pattern exist"""
        try:
            import fnmatch
            for root, dirs, files in os.walk(self.root_path):
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '__pycache__'}]
                if any(fnmatch.fnmatch(f, pattern) for f in files):
                    return True
        except:
            pass
        return False

    def _has_file_with_content(self, content: str) -> bool:
        """Check if any file contains specific content"""
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
        try:
            for root, dirs, files in os.walk(self.root_path):
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'venv', '__pycache__'}]
                for file in files:
                    if any(file.endswith(ext) for ext in code_extensions):
                        try:
                            with open(Path(root) / file, 'r', encoding='utf-8', errors='ignore') as f:
                                if content in f.read():
                                    return True
                        except:
                            pass
        except:
            pass
        return False
