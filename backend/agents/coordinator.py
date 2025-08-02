"""
Agent Coordinator - Multi-Agent System Manager
Coordinates between different AI agents for comprehensive educational support
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from agents.content_generator import ContentGeneratorAgent


class AgentCoordinator:
    """
    Coordinates multiple AI agents for comprehensive educational support
    """
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AgentCoordinator")
        self.agents = {}
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize all agents"""
        try:
            self.logger.info("Initializing Agent Coordinator...")
            
            # Initialize Content Generator Agent
            self.agents['content_generator'] = ContentGeneratorAgent()
            self.logger.info("Content Generator Agent initialized")
            
            # TODO: Initialize other agents in future phases
            # self.agents['assessment'] = AssessmentAgent()
            # self.agents['adaptive_learning'] = AdaptiveLearningAgent()
            # self.agents['engagement'] = EngagementAgent()
            # self.agents['analytics'] = AnalyticsAgent()
            # self.agents['voice_interaction'] = VoiceInteractionAgent()
            # self.agents['learning_coordinator'] = LearningCoordinatorAgent()
            
            self.is_initialized = True
            self.logger.info("Agent Coordinator initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Agent Coordinator: {e}")
            raise

    async def shutdown(self):
        """Shutdown all agents gracefully"""
        try:
            self.logger.info("Shutting down Agent Coordinator...")
            
            # TODO: Implement agent-specific shutdown procedures
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'shutdown'):
                    await agent.shutdown()
                self.logger.info(f"Agent {agent_name} shut down")
            
            self.is_initialized = False
            self.logger.info("Agent Coordinator shut down successfully")
            
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

    async def get_status(self) -> Dict[str, Any]:
        """Get overall status of all agents"""
        try:
            if not self.is_initialized:
                return {"status": "not_initialized", "agents": {}}
            
            agent_statuses = {}
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'get_agent_status'):
                    agent_statuses[agent_name] = await agent.get_agent_status()
                else:
                    agent_statuses[agent_name] = {"status": "unknown"}
            
            return {
                "status": "initialized",
                "total_agents": len(self.agents),
                "initialized_at": datetime.utcnow().isoformat(),
                "agents": agent_statuses
            }
            
        except Exception as e:
            self.logger.error(f"Error getting status: {e}")
            return {"status": "error", "error": str(e)}

    def get_agent(self, agent_name: str) -> Optional[Any]:
        """Get specific agent instance"""
        return self.agents.get(agent_name)

    async def route_request(self, agent_name: str, method: str, **kwargs) -> Any:
        """Route request to specific agent"""
        try:
            agent = self.get_agent(agent_name)
            if not agent:
                raise ValueError(f"Agent '{agent_name}' not found")
            
            if not hasattr(agent, method):
                raise ValueError(f"Method '{method}' not available on agent '{agent_name}'")
            
            method_func = getattr(agent, method)
            if asyncio.iscoroutinefunction(method_func):
                return await method_func(**kwargs)
            else:
                return method_func(**kwargs)
                
        except Exception as e:
            self.logger.error(f"Error routing request to {agent_name}.{method}: {e}")
            raise

    async def generate_content(self, **kwargs) -> Any:
        """Convenience method for content generation"""
        return await self.route_request('content_generator', 'generate_content', **kwargs)

    async def generate_questions(self, **kwargs) -> Any:
        """Convenience method for question generation"""
        return await self.route_request('content_generator', 'generate_questions', **kwargs)

    async def generate_explanation(self, **kwargs) -> Any:
        """Convenience method for explanation generation"""
        return await self.route_request('content_generator', 'generate_explanation', **kwargs)