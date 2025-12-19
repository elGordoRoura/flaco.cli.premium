"""GitHub-styled contribution tracking and analytics"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum


class ActivityType(Enum):
    """Types of activities to track"""
    CHAT_MESSAGE = "chat_message"
    FILE_CREATED = "file_created"
    FILE_MODIFIED = "file_modified"
    FILE_DELETED = "file_deleted"
    GIT_COMMIT = "git_commit"
    TOOL_EXECUTION = "tool_execution"
    PROJECT_CREATED = "project_created"
    AGENT_SWARM = "agent_swarm"


@dataclass
class Activity:
    """Represents a single activity"""
    type: str
    timestamp: str
    details: Dict[str, any]
    project: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        return cls(**data)


@dataclass
class ActivityStats:
    """Statistics for a time period"""
    period: str  # 'day', 'week', 'month', 'year'
    start_date: str
    end_date: str
    total_activities: int
    chat_messages: int
    files_created: int
    files_modified: int
    git_commits: int
    tool_executions: int
    agent_swarms: int
    most_active_day: Optional[str] = None
    streak_days: int = 0
    total_tokens: int = 0
    projects_worked_on: List[str] = None

    def __post_init__(self):
        if self.projects_worked_on is None:
            self.projects_worked_on = []


class ContributionTracker:
    """Track and analyze Flaco contributions"""

    def __init__(self, config_dir: str = "~/.flaco"):
        self.config_dir = Path(config_dir).expanduser()
        self.config_dir.mkdir(exist_ok=True)
        self.activities_file = self.config_dir / "activities.json"
        self.activities: List[Activity] = []
        self._load_activities()

    def _load_activities(self):
        """Load activities from file"""
        if self.activities_file.exists():
            try:
                with open(self.activities_file, 'r') as f:
                    data = json.load(f)
                    self.activities = [Activity.from_dict(a) for a in data]
            except Exception as e:
                print(f"Warning: Could not load activities: {e}")

    def _save_activities(self):
        """Save activities to file"""
        try:
            with open(self.activities_file, 'w') as f:
                data = [a.to_dict() for a in self.activities]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving activities: {e}")

    def log_activity(
        self,
        activity_type: ActivityType,
        details: Dict[str, any],
        project: Optional[str] = None
    ):
        """Log a new activity"""
        activity = Activity(
            type=activity_type.value,
            timestamp=datetime.now().isoformat(),
            details=details,
            project=project
        )

        self.activities.append(activity)

        # Keep only last 10,000 activities to prevent file from growing too large
        if len(self.activities) > 10000:
            self.activities = self.activities[-10000:]

        self._save_activities()

    def get_activities_for_date(self, date: datetime) -> List[Activity]:
        """Get activities for a specific date"""
        date_str = date.date().isoformat()
        return [
            a for a in self.activities
            if datetime.fromisoformat(a.timestamp).date().isoformat() == date_str
        ]

    def get_daily_count(self, date: datetime) -> int:
        """Get activity count for a specific day"""
        return len(self.get_activities_for_date(date))

    def get_contribution_map(self, days: int = 365) -> Dict[str, int]:
        """Get contribution map for last N days (GitHub-style)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        contribution_map = {}

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.date().isoformat()
            contribution_map[date_str] = 0
            current_date += timedelta(days=1)

        # Count activities per day
        for activity in self.activities:
            activity_date = datetime.fromisoformat(activity.timestamp).date().isoformat()
            if activity_date in contribution_map:
                contribution_map[activity_date] += 1

        return contribution_map

    def generate_contribution_graph(self, days: int = 365) -> str:
        """Generate ASCII contribution graph (GitHub-style)"""
        contribution_map = self.get_contribution_map(days)

        # Define intensity levels
        def get_symbol(count):
            if count == 0:
                return "·"
            elif count <= 2:
                return "▪"
            elif count <= 5:
                return "▪"
            elif count <= 10:
                return "◼"
            else:
                return "◼"

        # Group by weeks
        dates = sorted(contribution_map.keys())
        weeks = []
        current_week = []

        for date in dates:
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
            current_week.append((date, contribution_map[date]))

        if current_week:
            weeks.append(current_week)

        # Build graph
        lines = []
        lines.append("Contribution Activity (Last Year)")
        lines.append("")

        # Show by month
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for i in range(7):  # 7 days of week
            line = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i] + " "
            for week in weeks:
                if i < len(week):
                    count = week[i][1]
                    line += get_symbol(count) + " "
                else:
                    line += "  "
            lines.append(line)

        lines.append("")
        lines.append(f"Less · ▪ ▪ ◼ ◼ More")

        return "\n".join(lines)

    def calculate_streak(self) -> int:
        """Calculate current contribution streak"""
        if not self.activities:
            return 0

        contribution_map = self.get_contribution_map(days=365)
        dates = sorted(contribution_map.keys(), reverse=True)

        streak = 0
        today = datetime.now().date()

        for date_str in dates:
            date = datetime.fromisoformat(date_str).date()
            if (today - date).days == streak:
                if contribution_map[date_str] > 0:
                    streak += 1
                else:
                    break
            else:
                break

        return streak

    def get_stats(self, period: str = "day") -> ActivityStats:
        """Get statistics for a period"""
        now = datetime.now()

        if period == "day":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "week":
            start = now - timedelta(days=7)
            end = now
        elif period == "month":
            start = now - timedelta(days=30)
            end = now
        elif period == "year":
            start = now - timedelta(days=365)
            end = now
        else:
            raise ValueError(f"Invalid period: {period}")

        # Filter activities
        period_activities = [
            a for a in self.activities
            if start <= datetime.fromisoformat(a.timestamp) <= end
        ]

        # Count by type
        type_counts = defaultdict(int)
        for activity in period_activities:
            type_counts[activity.type] += 1

        # Get unique projects
        projects = list(set(a.project for a in period_activities if a.project))

        # Find most active day
        daily_counts = defaultdict(int)
        for activity in period_activities:
            day = datetime.fromisoformat(activity.timestamp).date().isoformat()
            daily_counts[day] += 1

        most_active_day = max(daily_counts.items(), key=lambda x: x[1])[0] if daily_counts else None

        # Calculate total tokens
        total_tokens = sum(
            a.details.get('tokens', 0)
            for a in period_activities
            if a.type == ActivityType.CHAT_MESSAGE.value
        )

        return ActivityStats(
            period=period,
            start_date=start.isoformat(),
            end_date=end.isoformat(),
            total_activities=len(period_activities),
            chat_messages=type_counts[ActivityType.CHAT_MESSAGE.value],
            files_created=type_counts[ActivityType.FILE_CREATED.value],
            files_modified=type_counts[ActivityType.FILE_MODIFIED.value],
            git_commits=type_counts[ActivityType.GIT_COMMIT.value],
            tool_executions=type_counts[ActivityType.TOOL_EXECUTION.value],
            agent_swarms=type_counts[ActivityType.AGENT_SWARM.value],
            most_active_day=most_active_day,
            streak_days=self.calculate_streak() if period == "day" else 0,
            total_tokens=total_tokens,
            projects_worked_on=projects
        )

    def generate_recap(self, period: str = "week") -> str:
        """Generate a recap report"""
        stats = self.get_stats(period)

        period_name = {
            "day": "Today",
            "week": "This Week",
            "month": "This Month",
            "year": "This Year"
        }.get(period, period)

        recap = f"""
# 📊 {period_name}'s Flaco Recap

## 🎯 Activity Summary
- **Total Activities**: {stats.total_activities:,}
- **Chat Messages**: {stats.chat_messages:,}
- **Files Created**: {stats.files_created:,}
- **Files Modified**: {stats.files_modified:,}
- **Git Commits**: {stats.git_commits:,}
- **Tool Executions**: {stats.tool_executions:,}
- **Agent Swarms**: {stats.agent_swarms:,}

## 🔥 Engagement
"""

        if stats.streak_days > 0 and period == "day":
            recap += f"- **Current Streak**: {stats.streak_days} days! 🔥\n"

        if stats.most_active_day:
            recap += f"- **Most Active Day**: {stats.most_active_day}\n"

        if stats.total_tokens > 0:
            recap += f"- **Tokens Used**: {stats.total_tokens:,}\n"

        if stats.projects_worked_on:
            recap += f"\n## 📁 Projects\n"
            for project in stats.projects_worked_on:
                recap += f"- {project}\n"

        # Add productivity message
        recap += "\n## 💪 Keep It Up!\n"

        if stats.total_activities == 0:
            recap += "No activity yet. Start coding to build your streak!"
        elif stats.total_activities < 10:
            recap += "Good start! Keep the momentum going."
        elif stats.total_activities < 50:
            recap += "You're on fire! Great productivity."
        else:
            recap += "Incredible work! You're a Flaco power user! 🚀"

        return recap

    def get_leaderboard_stats(self) -> Dict[str, any]:
        """Get stats for leaderboard/comparison"""
        year_stats = self.get_stats("year")

        return {
            "total_activities": year_stats.total_activities,
            "current_streak": self.calculate_streak(),
            "total_commits": year_stats.git_commits,
            "files_created": year_stats.files_created,
            "agent_swarms": year_stats.agent_swarms,
            "projects": len(year_stats.projects_worked_on)
        }
