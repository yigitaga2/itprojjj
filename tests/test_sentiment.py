# Test suite for sentiment analysis functionality

import pytest
import sys
import os

# Add backend to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.sentiment import analyze_sentiment

class TestSentimentAnalysis:
    """Test cases for Dutch sentiment analysis"""
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        test_cases = [
            "De lessen zijn geweldig en heel leuk",
            "Fantastische docenten, zeer behulpzaam",
            "Perfect uitgelegd, super duidelijk"
        ]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == "Positive", f"Expected Positive for: {text}"
            assert score > 0, f"Expected positive score for: {text}"
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        test_cases = [
            "De leerkrachten zijn racistisch",
            "Lessen zijn onnozel en waardeloos", 
            "Verschrikkelijk slechte uitleg"
        ]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == "Negative", f"Expected Negative for: {text}"
            assert score < 0, f"Expected negative score for: {text}"
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        test_cases = [
            "De lessen zijn niet slecht, het is ok",
            "Redelijk goed, kan beter",
            "Normale lessen, niets bijzonders"
        ]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == "Neutral", f"Expected Neutral for: {text}"
            assert abs(score) < 0.3, f"Expected neutral score for: {text}"
    
    def test_negation_handling(self):
        """Test negation logic (niet + negative word = neutral)"""
        test_cases = [
            ("De lessen zijn slecht", "Negative"),
            ("De lessen zijn niet slecht", "Neutral"),
            ("Het is verschrikkelijk", "Negative"),
            ("Het is niet verschrikkelijk", "Neutral")
        ]
        
        for text, expected_label in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == expected_label, f"Expected {expected_label} for: {text}, got {label}"
    
    def test_spelling_tolerance(self):
        """Test fuzzy matching for spelling errors"""
        test_cases = [
            "De kleerkrachten zijn rassistisch",  # Should detect as negative
            "Lessen zijn onozzel",  # Should detect as negative
            "Heel slegt uitgelegd"  # Should detect as negative
        ]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == "Negative", f"Expected Negative for misspelled: {text}"
    
    def test_constructive_criticism(self):
        """Test detection of constructive criticism as negative"""
        test_cases = [
            "Docenten hebben nood aan motivatie",
            "De lessen kunnen beter",
            "Zou fijn zijn als er meer uitleg komt"
        ]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            assert label == "Negative", f"Expected Negative for constructive criticism: {text}"
    
    def test_confidence_scores(self):
        """Test that confidence scores are within valid range"""
        test_texts = [
            "Geweldig!",
            "Verschrikkelijk slecht",
            "Het is ok",
            "Niet slecht"
        ]
        
        for text in test_texts:
            label, score, confidence = analyze_sentiment(text)
            assert 0 <= confidence <= 1, f"Confidence should be 0-1, got {confidence} for: {text}"
    
    def test_empty_text(self):
        """Test handling of empty or whitespace text"""
        test_cases = ["", "   ", "\n\t"]
        
        for text in test_cases:
            label, score, confidence = analyze_sentiment(text)
            # Should handle gracefully without crashing
            assert label in ["Positive", "Negative", "Neutral"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
