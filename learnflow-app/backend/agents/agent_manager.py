"""
Agent Manager for LearnFlow
Coordinates the multi-agent system for AI tutoring
"""

import asyncio
from typing import Dict, Any, List
from enum import Enum
from .triage_agent import TriageAgent
from .concepts_agent import ConceptsAgent
from .code_review_agent import CodeReviewAgent
from .debug_agent import DebugAgent
from .exercise_agent import ExerciseAgent
from .progress_agent import ProgressAgent

class AgentType(Enum):
    TRIAGE = "triage"
    CONCEPTS = "concepts"
    CODE_REVIEW = "code_review"
    DEBUG = "debug"
    EXERCISE = "exercise"
    PROGRESS = "progress"

class AgentManager:
    def __init__(self):
        self.agents: Dict[AgentType, Any] = {}
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all AI agents"""
        self.agents[AgentType.TRIAGE] = TriageAgent()
        self.agents[AgentType.CONCEPTS] = ConceptsAgent()
        self.agents[AgentType.CODE_REVIEW] = CodeReviewAgent()
        self.agents[AgentType.DEBUG] = DebugAgent()
        self.agents[AgentType.EXERCISE] = ExerciseAgent()
        self.agents[AgentType.PROGRESS] = ProgressAgent()

    async def route_request(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route user request to appropriate agent based on content"""
        # Determine which agent should handle the request
        agent_type = await self._determine_agent_type(user_input, context)

        # Get the agent and execute the request
        agent = self.agents[agent_type]
        result = await agent.process(user_input, context)

        # Update progress through progress agent
        await self._update_progress(user_input, result, context)

        return result

    async def _determine_agent_type(self, user_input: str, context: Dict[str, Any] = None) -> AgentType:
        """Determine which agent should handle the request"""
        user_input_lower = user_input.lower()

        # Keywords that suggest different agent types
        if any(keyword in user_input_lower for keyword in ['debug', 'error', 'fix', 'issue', 'problem']):
            return AgentType.DEBUG
        elif any(keyword in user_input_lower for keyword in ['concept', 'explain', 'topic', 'learn', 'understand']):
            return AgentType.CONCEPTS
        elif any(keyword in user_input_lower for keyword in ['code', 'review', 'improve', 'better', 'style']):
            return AgentType.CODE_REVIEW
        elif any(keyword in user_input_lower for keyword in ['exercise', 'practice', 'challenge', 'problem']):
            return AgentType.EXERCISE
        else:
            # Default to triage for initial assessment
            return AgentType.TRIAGE

    async def _update_progress(self, user_input: str, result: Dict[str, Any], context: Dict[str, Any] = None):
        """Update user progress through the progress agent"""
        progress_agent = self.agents[AgentType.PROGRESS]
        await progress_agent.update_progress(user_input, result, context)

    async def get_student_progress(self, student_id: str) -> Dict[str, Any]:
        """Get comprehensive student progress"""
        progress_agent = self.agents[AgentType.PROGRESS]
        return await progress_agent.get_student_progress(student_id)

    async def get_recommendations(self, student_id: str) -> List[Dict[str, Any]]:
        """Get personalized learning recommendations"""
        progress_agent = self.agents[AgentType.PROGRESS]
        return await progress_agent.get_recommendations(student_id)