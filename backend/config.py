# Configuration settings for the School Feedback Platform

import os
from typing import Optional

class Settings:
    """Application settings and configuration"""
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://sfp:sfp@localhost:5432/sfp")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin settings
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@school.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "Password123!")
    
    # Sentiment analysis settings
    POSITIVE_THRESHOLD: float = float(os.getenv("POSITIVE_THRESHOLD", "0.1"))
    NEGATIVE_THRESHOLD: float = float(os.getenv("NEGATIVE_THRESHOLD", "-0.1"))
    
    # CORS settings
    CORS_ALLOW_ORIGINS: str = os.getenv("CORS_ALLOW_ORIGINS", "*")
    
    # Application settings
    APP_NAME: str = "School Feedback Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

# Create settings instance
settings = Settings()

def get_database_url() -> str:
    """Get the database URL for the current environment"""
    return settings.DATABASE_URL

def is_development() -> bool:
    """Check if we're running in development mode"""
    return settings.DEBUG
