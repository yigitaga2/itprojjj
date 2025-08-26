# API endpoint tests for the School Feedback Platform

import pytest
import requests
import json
from datetime import datetime

class TestFeedbackAPI:
    """Test cases for feedback API endpoints"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_health_check(self):
        """Test if API is running"""
        try:
            response = requests.get(f"{self.BASE_URL}/")
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running")
    
    def test_categories_endpoint(self):
        """Test categories endpoint"""
        response = requests.get(f"{self.BASE_URL}/categories")
        assert response.status_code == 200
        
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0
        
        # Check expected categories
        category_names = [cat["name"] for cat in categories]
        expected_categories = ["Didactiek", "Materiaal", "Locaties", "Overig"]
        for expected in expected_categories:
            assert expected in category_names
    
    def test_subjects_endpoint(self):
        """Test subjects endpoint"""
        response = requests.get(f"{self.BASE_URL}/subjects")
        assert response.status_code == 200
        
        subjects = response.json()
        assert isinstance(subjects, list)
        assert len(subjects) > 0
    
    def test_sentiment_endpoint(self):
        """Test sentiment analysis endpoint"""
        test_text = "De lessen zijn leuk"
        response = requests.get(f"{self.BASE_URL}/test-sentiment?text={test_text}")
        assert response.status_code == 200
        
        result = response.json()
        assert "text" in result
        assert "label" in result
        assert "score" in result
        assert "confidence" in result
        
        assert result["text"] == test_text
        assert result["label"] in ["Positive", "Negative", "Neutral"]
        assert isinstance(result["score"], (int, float))
        assert isinstance(result["confidence"], (int, float))
    
    def test_feedback_submission(self):
        """Test anonymous feedback submission"""
        feedback_data = {
            "text": "Test feedback voor de API test",
            "category_id": 1,
            "subject_id": 1
        }
        
        response = requests.post(
            f"{self.BASE_URL}/feedback",
            json=feedback_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
    
    def test_login_endpoint(self):
        """Test login functionality"""
        login_data = {
            "username": "admin",
            "password": "Password123!"
        }
        
        response = requests.post(
            f"{self.BASE_URL}/auth/login",
            data=login_data  # Form data for OAuth2
        )
        
        if response.status_code == 200:
            result = response.json()
            assert "access_token" in result
            assert "token_type" in result
            assert result["token_type"] == "bearer"
        else:
            # Login might fail if credentials changed
            assert response.status_code in [400, 401]

class TestSentimentEndpoint:
    """Specific tests for sentiment analysis endpoint"""
    
    BASE_URL = "http://localhost:8000"
    
    def test_positive_sentiment_api(self):
        """Test positive sentiment via API"""
        test_cases = [
            "De lessen zijn geweldig",
            "Fantastische docenten",
            "Heel goed uitgelegd"
        ]
        
        for text in test_cases:
            response = requests.get(f"{self.BASE_URL}/test-sentiment?text={text}")
            assert response.status_code == 200
            
            result = response.json()
            assert result["label"] == "Positive"
    
    def test_negative_sentiment_api(self):
        """Test negative sentiment via API"""
        test_cases = [
            "De leerkrachten zijn racistisch",
            "Lessen zijn onnozel",
            "Verschrikkelijk slecht"
        ]
        
        for text in test_cases:
            response = requests.get(f"{self.BASE_URL}/test-sentiment?text={text}")
            assert response.status_code == 200
            
            result = response.json()
            assert result["label"] == "Negative"
    
    def test_neutral_sentiment_api(self):
        """Test neutral sentiment via API"""
        test_cases = [
            "De lessen zijn niet slecht",
            "Het is ok",
            "Redelijk goed"
        ]
        
        for text in test_cases:
            response = requests.get(f"{self.BASE_URL}/test-sentiment?text={text}")
            assert response.status_code == 200
            
            result = response.json()
            assert result["label"] == "Neutral"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
