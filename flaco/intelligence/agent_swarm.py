"""Agent Swarm - Multiple specialized agents collaborating on complex tasks"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
from ..agents import SpecializedAgent, AgentType


class TaskComplexity(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class SwarmTask:
    """A task that requires multiple agents"""
    description: str
    complexity: TaskComplexity
    required_agents: List[AgentType]
    primary_agent: AgentType
    reasoning: str


class AgentSwarm:
    """Coordinate multiple agents working together"""

    def __init__(self, agent_router):
        self.agent_router = agent_router

    def analyze_task(self, user_message: str) -> Optional[SwarmTask]:
        """Analyze if a task requires multiple agents"""
        message_lower = user_message.lower()

        # Complex multi-domain tasks
        swarm_indicators = {
            "full stack": ([AgentType.FRONTEND, AgentType.BACKEND, AgentType.DATABASE], AgentType.BACKEND),
            "deploy": ([AgentType.BACKEND, AgentType.DEVOPS], AgentType.DEVOPS),
            "secure api": ([AgentType.BACKEND, AgentType.SECURITY, AgentType.API], AgentType.SECURITY),
            "test coverage": ([AgentType.CODE_REVIEW, AgentType.BACKEND], AgentType.CODE_REVIEW),
            "authentication system": ([AgentType.BACKEND, AgentType.SECURITY, AgentType.DATABASE], AgentType.SECURITY),
            "user dashboard": ([AgentType.FRONTEND, AgentType.BACKEND, AgentType.DATABASE], AgentType.FRONTEND),
            "microservice": ([AgentType.BACKEND, AgentType.DEVOPS, AgentType.API], AgentType.BACKEND),
            "e-commerce": ([AgentType.FRONTEND, AgentType.BACKEND, AgentType.DATABASE, AgentType.SECURITY], AgentType.BACKEND),
            "crud application": ([AgentType.BACKEND, AgentType.DATABASE, AgentType.API], AgentType.BACKEND),
            "automation pipeline": ([AgentType.N8N, AgentType.DEVOPS, AgentType.API], AgentType.N8N),
        }

        for indicator, (agents, primary) in swarm_indicators.items():
            if indicator in message_lower:
                complexity = self._determine_complexity(len(agents))
                return SwarmTask(
                    description=user_message,
                    complexity=complexity,
                    required_agents=agents,
                    primary_agent=primary,
                    reasoning=f"Detected '{indicator}' which requires expertise from {len(agents)} different domains"
                )

        # Check for multiple domain keywords
        domains_detected = []

        if any(kw in message_lower for kw in ['frontend', 'ui', 'react', 'vue', 'interface']):
            domains_detected.append(AgentType.FRONTEND)

        if any(kw in message_lower for kw in ['backend', 'api', 'server', 'fastapi', 'django']):
            domains_detected.append(AgentType.BACKEND)

        if any(kw in message_lower for kw in ['database', 'sql', 'postgres', 'mongodb', 'query']):
            domains_detected.append(AgentType.DATABASE)

        if any(kw in message_lower for kw in ['deploy', 'docker', 'kubernetes', 'ci/cd']):
            domains_detected.append(AgentType.DEVOPS)

        if any(kw in message_lower for kw in ['security', 'secure', 'authentication', 'authorization']):
            domains_detected.append(AgentType.SECURITY)

        # If multiple domains detected, create a swarm
        if len(domains_detected) >= 2:
            complexity = self._determine_complexity(len(domains_detected))
            return SwarmTask(
                description=user_message,
                complexity=complexity,
                required_agents=domains_detected,
                primary_agent=domains_detected[0],
                reasoning=f"Multiple domains detected: {', '.join([a.value for a in domains_detected])}"
            )

        return None

    def _determine_complexity(self, agent_count: int) -> TaskComplexity:
        """Determine task complexity based on agent count"""
        if agent_count <= 1:
            return TaskComplexity.SIMPLE
        elif agent_count == 2:
            return TaskComplexity.MODERATE
        elif agent_count == 3:
            return TaskComplexity.COMPLEX
        else:
            return TaskComplexity.VERY_COMPLEX

    def get_swarm_agents(self, task: SwarmTask) -> List[SpecializedAgent]:
        """Get all agents needed for a swarm task"""
        return [self.agent_router.get_agent(agent_type) for agent_type in task.required_agents]

    def format_swarm_status(self, task: SwarmTask) -> str:
        """Format the swarm collaboration status message"""
        agents = self.get_swarm_agents(task)
        agent_emojis = ' '.join([agent.emoji for agent in agents])
        agent_names = ', '.join([agent.name for agent in agents])

        return f"{agent_emojis} Team Swarm: {agent_names}"
