import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from config.database import create_tables
from core.exceptions import AppException
from core.logging import setup_logging
from api.v1.router import api_router
from agents.coordinator import AgentCoordinator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events"""
    # Startup
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting RSP Education Agent API...")
        
        # Initialize database
        await create_tables()
        logger.info("Database tables created successfully")
        
        # Initialize agent coordinator
        app.state.agent_coordinator = AgentCoordinator()
        await app.state.agent_coordinator.initialize()
        logger.info("Agent coordinator initialized")
        
        logger.info("Application startup completed")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    if hasattr(app.state, 'agent_coordinator'):
        await app.state.agent_coordinator.shutdown()
    logger.info("Application shutdown completed")


# Create FastAPI app
app = FastAPI(
    title="RSP Education Agent API",
    description="An intelligent tutoring API powered by Agentic AI for personalized CBSE education",
    version="2.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    """Handle custom application exceptions"""
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "message": exc.message,
            "code": exc.code,
            "type": exc.__class__.__name__
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions"""
    logger = logging.getLogger(__name__)
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "code": "INTERNAL_ERROR"
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RSP Education Agent API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check agent coordinator status
        agent_status = "unknown"
        if hasattr(app.state, 'agent_coordinator'):
            agent_status = await app.state.agent_coordinator.get_status()
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "agents": agent_status,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": asyncio.get_event_loop().time()
            }
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )