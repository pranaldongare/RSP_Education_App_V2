#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Optional, List, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class SimpleSettings(BaseSettings):
    """Simplified settings for debugging"""
    
    # Basic fields
    debug: bool = Field(default=False, env="DEBUG")
    secret_key: str = Field(default="dev-secret", env="SECRET_KEY")
    
    # CORS - Try the simplest approach first
    cors_origins_raw: str = Field(default="*", env="CORS_ORIGINS")
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from string to list"""
        if self.cors_origins_raw.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins_raw.split(',') if origin.strip()]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from .env file


if __name__ == "__main__":
    print("Testing pydantic-settings configuration...")
    
    # Print environment variables
    print(f"CORS_ORIGINS env var: {os.getenv('CORS_ORIGINS', 'NOT_SET')}")
    
    try:
        settings = SimpleSettings()
        print("SUCCESS: Settings loaded successfully!")
        print(f"  debug: {settings.debug}")
        print(f"  secret_key: {settings.secret_key}")
        print(f"  cors_origins_raw: {settings.cors_origins_raw}")
        print(f"  cors_origins: {settings.cors_origins}")
    except Exception as e:
        print(f"ERROR: Settings failed to load: {e}")
        import traceback
        traceback.print_exc()