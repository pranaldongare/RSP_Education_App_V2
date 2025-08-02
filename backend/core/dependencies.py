"""
FastAPI Dependencies
Provides dependency injection for FastAPI endpoints
"""

from fastapi import Request, HTTPException, status
from agents.coordinator import AgentCoordinator


def get_agent_coordinator(request: Request) -> AgentCoordinator:
    """
    Get the agent coordinator from FastAPI app state
    """
    if not hasattr(request.app.state, 'agent_coordinator'):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent Coordinator not initialized"
        )
    
    coordinator = request.app.state.agent_coordinator
    if not coordinator.is_initialized:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent Coordinator not ready"
        )
    
    return coordinator