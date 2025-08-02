"""
Logging Configuration
Sets up structured logging for the application
"""

import logging
import sys
from typing import Any
from config.settings import settings


def setup_logging():
    """
    Setup application logging configuration
    """
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log') if not settings.debug else logging.NullHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Suppress noisy third-party loggers in production
    if not settings.debug:
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("anthropic").setLevel(logging.WARNING)
        logging.getLogger("langchain").setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("Logging configuration initialized")