# Testing Guide

## Overzicht

Dit document beschrijft hoe je de tests kunt uitvoeren voor de School Feedback Platform.

## Test Structuur

```
tests/
├── conftest.py          # Pytest configuratie en fixtures
├── test_sentiment.py    # Unit tests voor sentiment analyse
└── test_api.py         # Integration tests voor API endpoints
```

## Vereisten

Installeer test dependencies:

```bash
pip install pytest requests
```

## Tests Uitvoeren

### Alle Tests
```bash
# Vanuit project root
pytest tests/ -v
```

### Specifieke Test Bestanden
```bash
# Alleen sentiment tests
pytest tests/test_sentiment.py -v

# Alleen API tests  
pytest tests/test_api.py -v
```

### Tests per Categorie
```bash
# Alleen unit tests
pytest -m unit -v

# Alleen integration tests
pytest -m integration -v

# Exclude slow tests
pytest -m "not slow" -v
```

## Test Categorieën

### Unit Tests (`test_sentiment.py`)
- **Doel:** Test sentiment analyse functionaliteit
- **Scope:** Individuele functies zonder externe dependencies
- **Snelheid:** Snel (< 1 seconde per test)

**Test Cases:**
- Positieve sentiment detectie
- Negatieve sentiment detectie  
- Neutrale sentiment detectie
- Negatie handling ("niet slecht" = neutraal)
- Spelling tolerantie (fuzzy matching)
- Constructieve kritiek detectie
- Confidence score validatie

### Integration Tests (`test_api.py`)
- **Doel:** Test API endpoints end-to-end
- **Scope:** Volledige API calls naar running server
- **Snelheid:** Langzamer (vereist running server)

**Test Cases:**
- Health check endpoint
- Categories endpoint
- Subjects endpoint  
- Sentiment analysis endpoint
- Feedback submission
- Authentication endpoints

## Test Data

### Sentiment Test Cases

**Positief:**
- "De lessen zijn geweldig en heel leuk"
- "Fantastische docenten, zeer behulpzaam"
- "Perfect uitgelegd, super duidelijk"

**Negatief:**
- "De leerkrachten zijn racistisch"
- "Lessen zijn onnozel en waardeloos"
- "Verschrikkelijk slechte uitleg"

**Neutraal:**
- "De lessen zijn niet slecht, het is ok"
- "Redelijk goed, kan beter"
- "Normale lessen, niets bijzonders"

### Spelling Errors
- "De kleerkrachten zijn rassistisch" → Negatief
- "Lessen zijn onozzel" → Negatief
- "Heel slegt uitgelegd" → Negatief

## Server Vereisten

Voor integration tests moet de server draaien:

```bash
# Start de applicatie
docker-compose up -d

# Controleer of server draait
curl http://localhost:8000/
```

## Test Output

### Successful Run
```
tests/test_sentiment.py::TestSentimentAnalysis::test_positive_sentiment PASSED
tests/test_sentiment.py::TestSentimentAnalysis::test_negative_sentiment PASSED
tests/test_sentiment.py::TestSentimentAnalysis::test_neutral_sentiment PASSED
tests/test_api.py::TestFeedbackAPI::test_health_check PASSED
```

### Failed Test
```
FAILED tests/test_sentiment.py::TestSentimentAnalysis::test_negation_handling
AssertionError: Expected Neutral for: De lessen zijn niet slecht, got Negative
```

## Troubleshooting

### Import Errors
Als je import errors krijgt:
```bash
# Zorg dat je in de project root bent
cd /path/to/itprojbund

# Run tests vanuit project root
pytest tests/ -v
```

### API Connection Errors
Als API tests falen:
```bash
# Controleer of server draait
docker-compose ps

# Start server als nodig
docker-compose up -d

# Wacht tot server ready is
sleep 10
```

### Slow Tests
Om snelle feedback te krijgen:
```bash
# Skip integration tests
pytest tests/test_sentiment.py -v

# Of skip slow tests
pytest -m "not slow" -v
```

## Continuous Integration

Voor CI/CD pipelines:
```bash
# Install dependencies
pip install -r backend/requirements.txt
pip install pytest requests

# Run unit tests only (no server required)
pytest tests/test_sentiment.py -v

# For full test suite, start server first
docker-compose up -d
sleep 30  # Wait for startup
pytest tests/ -v
docker-compose down
```
