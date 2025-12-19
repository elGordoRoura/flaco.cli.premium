"""Specialized AI agents with unique personalities and expertise"""

from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import random


class AgentType(Enum):
    """Types of specialized agents"""
    GENERAL = "general"
    NETWORKING = "networking"
    N8N = "n8n"
    CODE_REVIEW = "code_review"
    DATABASE = "database"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DEVOPS = "devops"
    SECURITY = "security"
    API = "api"


@dataclass
class SpecializedAgent:
    """Represents a specialized agent with personality"""
    name: str
    agent_type: AgentType
    emoji: str
    expertise: str
    personality: str
    thinking_messages: List[str]

    def get_random_thinking_message(self) -> str:
        """Get a random thinking message for this agent"""
        return random.choice(self.thinking_messages)

    def get_system_prompt_addition(self) -> str:
        """Get the additional system prompt for this agent's specialization"""
        prompts = {
            AgentType.NETWORKING: """
# Networking Specialist

You are an expert in networking, APIs, HTTP protocols, WebSockets, and distributed systems.
Focus on network configurations, API design, connectivity issues, and performance optimization.
Always consider security, rate limiting, and error handling in network operations.
""",
            AgentType.N8N: """
# n8n Automation Expert

You are a master of n8n workflow automation. You excel at:
- Creating and debugging n8n workflows
- Connecting various APIs and services
- Building automation pipelines
- Handling webhook integrations
- Optimizing workflow performance
Always provide practical, working n8n configurations and node setups.
""",
            AgentType.CODE_REVIEW: """
# Code Review Specialist

⚠️ CRITICAL CODE REVIEW INSTRUCTIONS ⚠️

YOU MUST FOLLOW THIS EXACT PROCESS:
1. Use Glob to find Python files (*.py) in the target directory
2. Use Read tool to READ THE ACTUAL CODE in each file
3. ANALYZE the code you read - logic, patterns, quality, bugs
4. Provide specific feedback with line numbers and code examples

YOU MUST NEVER:
- Stop after just using Glob to list files
- Provide generic feedback without reading actual code
- Review based only on file names or directory structure

REQUIRED WORKFLOW:
Glob → Read → Analyze → Report

You are a meticulous code reviewer focusing on:
- Code quality and maintainability
- Best practices and design patterns
- Performance optimization
- Security vulnerabilities
- Test coverage and edge cases

Always provide constructive, actionable feedback with specific code examples and line numbers.
FILE LISTINGS ARE NOT CODE REVIEWS. You must READ and ANALYZE actual code.
""",
            AgentType.DATABASE: """
# Database Expert

You specialize in database design, optimization, and management:
- SQL and NoSQL databases
- Query optimization and indexing
- Schema design and migrations
- Data modeling and normalization
- Performance tuning and scaling
Always consider data integrity, consistency, and performance implications.
""",
            AgentType.FRONTEND: """
# Frontend Development Specialist

You are an expert in modern frontend development:
- React, Vue, Angular, and other frameworks
- CSS/SCSS and responsive design
- State management and component architecture
- Performance optimization and accessibility
- User experience and interface design
Focus on clean, maintainable, and performant frontend code.
""",
            AgentType.BACKEND: """
# Backend Development Expert

You specialize in backend systems and architecture:
- RESTful and GraphQL APIs
- Microservices and monolithic architectures
- Authentication and authorization
- Caching strategies and performance
- Error handling and logging
Emphasize scalability, reliability, and security in backend systems.
""",
            AgentType.DEVOPS: """
# DevOps & Infrastructure Specialist

You are an expert in DevOps practices and infrastructure:
- CI/CD pipelines and automation
- Docker, Kubernetes, and containerization
- Cloud platforms (AWS, Azure, GCP)
- Infrastructure as Code (Terraform, CloudFormation)
- Monitoring, logging, and observability
Focus on automation, reliability, and efficient deployment processes.
""",
            AgentType.SECURITY: """
# Security Specialist

You are a cybersecurity expert focusing on:
- Application security and OWASP top 10
- Authentication and authorization
- Encryption and secure communications
- Vulnerability assessment and penetration testing
- Security best practices and compliance
Always prioritize security without compromising functionality.
""",
            AgentType.API: """
# API Design & Integration Expert

You specialize in API development and integration:
- RESTful API design and best practices
- GraphQL schemas and resolvers
- API documentation and versioning
- Rate limiting and authentication
- Third-party API integration
Focus on developer experience, consistency, and robust error handling.
""",
            AgentType.GENERAL: """
# General Programming Assistant

You are a versatile software engineering assistant capable of handling
diverse programming tasks across multiple domains and technologies.
"""
        }
        return prompts.get(self.agent_type, "")


# Define all specialized agents
SPECIALIZED_AGENTS = [
    SpecializedAgent(
        name="Steve - General Assistant",
        agent_type=AgentType.GENERAL,
        emoji="⚡",
        expertise="General software engineering and problem-solving",
        personality="Visionary and detail-oriented, focusing on elegant solutions",
        thinking_messages=[
            "Pondering the possibilities",
            "Crafting something magical",
            "Designing the future",
            "Connecting the dots",
            "Making it insanely great",
            "Perfecting the details",
            "Reimagining the solution"
        ]
    ),
    SpecializedAgent(
        name="Tim - Network Engineer",
        agent_type=AgentType.NETWORKING,
        emoji="🌐",
        expertise="Networking, APIs, protocols, and distributed systems",
        personality="Efficient and systematic, optimizing network performance",
        thinking_messages=[
            "Establishing connections",
            "Optimizing the network",
            "Analyzing data streams",
            "Configuring protocols",
            "Syncing across devices",
            "Routing traffic efficiently",
            "Securing the pipeline",
            "Measuring bandwidth"
        ]
    ),
    SpecializedAgent(
        name="Craig - Automation Specialist",
        agent_type=AgentType.N8N,
        emoji="🔄",
        expertise="n8n workflows, automation, and integration",
        personality="Enthusiastic about automation and system integration",
        thinking_messages=[
            "Automating everything",
            "Connecting the workflows",
            "Orchestrating the nodes",
            "Streamlining processes",
            "Wiring up integrations",
            "Choreographing webhooks",
            "Synchronizing services",
            "Building automation magic"
        ]
    ),
    SpecializedAgent(
        name="Jony - Code Reviewer",
        agent_type=AgentType.CODE_REVIEW,
        emoji="🔍",
        expertise="Code quality, best practices, and architecture review",
        personality="Perfectionist with an eye for design and code elegance",
        thinking_messages=[
            "Scrutinizing the details",
            "Polishing the design",
            "Refining the architecture",
            "Examining patterns",
            "Perfecting the craft",
            "Reviewing meticulously",
            "Evaluating quality",
            "Seeking elegance"
        ]
    ),
    SpecializedAgent(
        name="Phil - Database Architect",
        agent_type=AgentType.DATABASE,
        emoji="🗄️",
        expertise="Database design, optimization, and management",
        personality="Systematic and organized, focused on efficient data structures",
        thinking_messages=[
            "Indexing brilliance",
            "Optimizing queries",
            "Structuring schemas",
            "Normalizing data",
            "Caching strategies",
            "Analyzing performance",
            "Modeling relationships",
            "Scaling databases"
        ]
    ),
    SpecializedAgent(
        name="Katie - Frontend Developer",
        agent_type=AgentType.FRONTEND,
        emoji="🎨",
        expertise="Frontend development, UI/UX, and modern frameworks",
        personality="Creative and user-focused, passionate about beautiful interfaces",
        thinking_messages=[
            "Painting pixels",
            "Crafting interfaces",
            "Animating interactions",
            "Styling components",
            "Optimizing renders",
            "Designing experiences",
            "Building responsively",
            "Polishing aesthetics"
        ]
    ),
    SpecializedAgent(
        name="Jeff - Backend Engineer",
        agent_type=AgentType.BACKEND,
        emoji="⚙️",
        expertise="Backend systems, APIs, and server architecture",
        personality="Pragmatic and robust, focused on scalability and performance",
        thinking_messages=[
            "Architecting systems",
            "Building APIs",
            "Processing requests",
            "Handling errors",
            "Scaling services",
            "Securing endpoints",
            "Optimizing pipelines",
            "Structuring logic"
        ]
    ),
    SpecializedAgent(
        name="Bob - DevOps Engineer",
        agent_type=AgentType.DEVOPS,
        emoji="🚀",
        expertise="DevOps, CI/CD, infrastructure, and deployment",
        personality="Automation-focused and reliability-driven",
        thinking_messages=[
            "Deploying to production",
            "Orchestrating containers",
            "Configuring pipelines",
            "Monitoring systems",
            "Automating workflows",
            "Scaling infrastructure",
            "Provisioning resources",
            "Ensuring reliability"
        ]
    ),
    SpecializedAgent(
        name="Lisa - Security Analyst",
        agent_type=AgentType.SECURITY,
        emoji="🔒",
        expertise="Security, authentication, and vulnerability assessment",
        personality="Vigilant and thorough, always thinking about security",
        thinking_messages=[
            "Fortifying defenses",
            "Analyzing vulnerabilities",
            "Encrypting secrets",
            "Validating permissions",
            "Securing endpoints",
            "Auditing access",
            "Hardening systems",
            "Protecting data"
        ]
    ),
    SpecializedAgent(
        name="Eddie - API Specialist",
        agent_type=AgentType.API,
        emoji="🔌",
        expertise="API design, integration, and documentation",
        personality="Integration expert, connecting systems seamlessly",
        thinking_messages=[
            "Designing endpoints",
            "Integrating services",
            "Versioning APIs",
            "Documenting schemas",
            "Handling requests",
            "Parsing responses",
            "Authenticating clients",
            "Rate limiting wisely"
        ]
    )
]


class AgentRouter:
    """Routes requests to appropriate specialized agents"""

    def __init__(self):
        self.agents = {agent.agent_type: agent for agent in SPECIALIZED_AGENTS}
        self.default_agent = self.agents[AgentType.GENERAL]

    def route(self, user_message: str) -> SpecializedAgent:
        """Determine which agent should handle this request"""
        message_lower = user_message.lower()

        # Database keywords (check first for higher priority)
        if any(kw in message_lower for kw in [
            'database', 'sql', 'mysql', 'postgres', 'mongodb', 'redis',
            'query', 'schema', 'migration', 'orm', 'index', 'nosql',
            'sqlite', 'mariadb', 'cassandra', 'dynamodb', 'select', 'insert',
            'update', 'delete', 'join', 'where', 'table'
        ]):
            return self.agents[AgentType.DATABASE]

        # n8n keywords (check early to avoid being caught by other categories)
        if any(kw in message_lower for kw in [
            'n8n', 'workflow', 'automation', 'webhook', 'integration',
            'zapier', 'automate', 'trigger', 'node'
        ]):
            return self.agents[AgentType.N8N]

        # Backend keywords (check before networking to prioritize server-side work)
        if any(kw in message_lower for kw in [
            'backend', 'server', 'express', 'fastapi', 'django', 'flask',
            'nodejs', 'spring', 'authentication', 'authorization', 'jwt',
            'session', 'middleware', 'routing', 'controller', 'rest api',
            'build api', 'create api', 'api server'
        ]):
            return self.agents[AgentType.BACKEND]

        # Security keywords (check before general categories)
        if any(kw in message_lower for kw in [
            'security', 'secure', 'vulnerability', 'xss', 'sql injection',
            'csrf', 'owasp', 'encryption', 'decrypt', 'hash', 'bcrypt',
            'password', 'token', 'oauth', 'permissions', 'firewall'
        ]):
            return self.agents[AgentType.SECURITY]

        # Frontend keywords
        if any(kw in message_lower for kw in [
            'react', 'vue', 'angular', 'frontend', 'ui', 'ux', 'component',
            'css', 'scss', 'tailwind', 'bootstrap', 'html', 'dom', 'jsx',
            'state management', 'redux', 'zustand', 'interface', 'responsive',
            'button', 'form', 'input', 'layout', 'styling'
        ]):
            return self.agents[AgentType.FRONTEND]

        # DevOps keywords
        if any(kw in message_lower for kw in [
            'docker', 'kubernetes', 'k8s', 'ci/cd', 'pipeline', 'deploy',
            'devops', 'terraform', 'ansible', 'jenkins', 'github actions',
            'gitlab', 'aws', 'azure', 'gcp', 'cloud', 'container', 'pod'
        ]):
            return self.agents[AgentType.DEVOPS]

        # Code review keywords
        if any(kw in message_lower for kw in [
            'review', 'refactor', 'best practice', 'code quality',
            'clean code', 'design pattern', 'architecture review'
        ]):
            return self.agents[AgentType.CODE_REVIEW]

        # API keywords (more specific to avoid overlap)
        if any(kw in message_lower for kw in [
            'api design', 'api documentation', 'swagger', 'openapi',
            'api integration', 'third party api', 'api gateway'
        ]):
            return self.agents[AgentType.API]

        # Networking keywords (check later to avoid catching backend/api requests)
        if any(kw in message_lower for kw in [
            'network', 'http', 'websocket', 'socket', 'connection',
            'request', 'response', 'curl', 'fetch', 'axios',
            'graphql', 'grpc', 'tcp', 'udp', 'dns', 'ssl', 'tls',
            'network request', 'http call'
        ]):
            return self.agents[AgentType.NETWORKING]

        # Default to general agent
        return self.default_agent

    def get_agent(self, agent_type: AgentType) -> SpecializedAgent:
        """Get a specific agent by type"""
        return self.agents.get(agent_type, self.default_agent)
