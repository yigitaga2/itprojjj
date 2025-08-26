# Pytest configuration and fixtures for the School Feedback Platform

import pytest
import sys
import os
from typing import Generator

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL for API testing"""
    return "http://localhost:8000"

@pytest.fixture(scope="session") 
def test_admin_credentials() -> dict:
    """Admin credentials for testing"""
    return {
        "username": "admin",
        "password": "Password123!"
    }

@pytest.fixture(scope="session")
def test_teacher_credentials() -> dict:
    """Teacher credentials for testing"""
    return {
        "username": "noor.jansen", 
        "password": "Welkom123!"
    }

@pytest.fixture
def sample_feedback_data() -> dict:
    """Sample feedback data for testing"""
    return {
        "text": "Dit is test feedback voor de applicatie",
        "category_id": 1,
        "subject_id": 1
    }

@pytest.fixture
def sentiment_test_cases() -> dict:
    """Test cases for sentiment analysis"""
    return {
        "positive": [
            "De lessen zijn geweldig en heel leuk",
            "Fantastische docenten, zeer behulpzaam", 
            "Perfect uitgelegd, super duidelijk"
        ],
        "negative": [
            "De leerkrachten zijn racistisch",
            "Lessen zijn onnozel en waardeloos",
            "Verschrikkelijk slechte uitleg"
        ],
        "neutral": [
            "De lessen zijn niet slecht, het is ok",
            "Redelijk goed, kan beter",
            "Normale lessen, niets bijzonders"
        ]
    }

@pytest.fixture
def spelling_error_cases() -> list:
    """Test cases with spelling errors"""
    return [
        "De kleerkrachten zijn rassistisch",
        "Lessen zijn onozzel", 
        "Heel slegt uitgelegd"
    ]

# Configure pytest
def pytest_configure(config):
    """Configure pytest settings"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add unit marker to sentiment tests
        if "test_sentiment" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to API tests  
        if "test_api" in item.nodeid:
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)
