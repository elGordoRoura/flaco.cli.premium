"""Update checker for Flaco CLI"""
import json
import time
from pathlib import Path
from typing import Optional, Tuple
import requests


class UpdateChecker:
    """Check for Flaco updates from GitHub releases"""

    GITHUB_API_URL = "https://api.github.com/repos/RouraIO/flaco.cli/releases/latest"
    CACHE_FILE = Path.home() / ".flaco" / "update_check.json"
    CACHE_DURATION = 86400  # 24 hours in seconds

    @classmethod
    def check_for_updates(cls, current_version: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Check if a newer version is available

        Returns:
            (has_update, latest_version, release_notes)
        """
        # Check cache first
        cached_result = cls._get_cached_result()
        if cached_result:
            return cached_result

        # Fetch latest release from GitHub
        try:
            response = requests.get(cls.GITHUB_API_URL, timeout=3)
            response.raise_for_status()

            data = response.json()
            latest_version = data.get("tag_name", "").lstrip("v")
            release_notes = data.get("body", "")

            # Extract first line of release notes as summary
            summary = release_notes.split('\n')[0] if release_notes else ""

            # Compare versions
            has_update = cls._is_newer_version(latest_version, current_version)

            # Cache the result
            result = (has_update, latest_version, summary)
            cls._cache_result(result)

            return result

        except Exception as e:
            # Silently fail - don't interrupt user experience
            return (False, None, None)

    @classmethod
    def _is_newer_version(cls, latest: str, current: str) -> bool:
        """Compare version strings (e.g., '0.3.0' vs '0.2.9')"""
        try:
            # Strip any whitespace
            latest = latest.strip()
            current = current.strip()

            # If versions are exactly the same, no update needed
            if latest == current:
                return False

            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]

            # Pad to same length
            while len(latest_parts) < len(current_parts):
                latest_parts.append(0)
            while len(current_parts) < len(latest_parts):
                current_parts.append(0)

            return latest_parts > current_parts
        except:
            return False

    @classmethod
    def _get_cached_result(cls) -> Optional[Tuple[bool, Optional[str], Optional[str]]]:
        """Get cached update check result if still valid"""
        if not cls.CACHE_FILE.exists():
            return None

        try:
            with open(cls.CACHE_FILE, 'r') as f:
                cache = json.load(f)

            # Check if cache is still valid
            if time.time() - cache.get('timestamp', 0) < cls.CACHE_DURATION:
                return (
                    cache.get('has_update', False),
                    cache.get('latest_version'),
                    cache.get('summary')
                )
        except:
            pass

        return None

    @classmethod
    def _cache_result(cls, result: Tuple[bool, Optional[str], Optional[str]]):
        """Cache the update check result"""
        try:
            cls.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

            cache = {
                'timestamp': time.time(),
                'has_update': result[0],
                'latest_version': result[1],
                'summary': result[2]
            }

            with open(cls.CACHE_FILE, 'w') as f:
                json.dump(cache, f)
        except:
            pass  # Silently fail if can't cache
