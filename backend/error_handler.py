# Error handling utilities for the School Feedback Platform

from fastapi import HTTPException
from typing import Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackError(Exception):
    """Custom exception for feedback-related errors"""
    pass

class SentimentAnalysisError(Exception):
    """Custom exception for sentiment analysis errors"""
    pass

def handle_database_error(error: Exception) -> Dict[str, Any]:
    """Handle database-related errors"""
    logger.error(f"Database error: {str(error)}")
    return {
        "error": "Database operation failed",
        "message": "Er is een probleem opgetreden met de database",
        "status": "error"
    }

def handle_validation_error(error: Exception) -> Dict[str, Any]:
    """Handle validation errors"""
    logger.error(f"Validation error: {str(error)}")
    return {
        "error": "Validation failed",
        "message": "De ingevoerde gegevens zijn niet geldig",
        "status": "error"
    }

def handle_sentiment_error(error: Exception) -> Dict[str, Any]:
    """Handle sentiment analysis errors"""
    logger.error(f"Sentiment analysis error: {str(error)}")
    return {
        "error": "Sentiment analysis failed",
        "message": "Sentiment analyse kon niet worden uitgevoerd",
        "status": "error"
    }
