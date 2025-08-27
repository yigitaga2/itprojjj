# 🎓 School Feedback Platform

Een anoniem feedback platform voor scholen waar studenten feedback kunnen geven en docenten/administrators deze kunnen bekijken en analyseren.

##  Functies

### Voor Studenten
- **Anonieme feedback**: Geen account nodig, volledige privacy
- **Sentiment analyse**: Automatische detectie van positieve/negatieve/neutrale feedback
- **Categorisatie**: Feedback indelen per onderwerp (Didactiek, Materiaal, Locaties, Overig)
- **Vakspecifiek**: Optioneel feedback koppelen aan specifieke vakken
- **Mobiel-vriendelijk**: Responsive design voor alle apparaten

### Voor Docenten/Administrators
- **Dashboard**: Overzicht van alle feedback met filters
- **Analytics**: Statistieken over sentiment en categorieën
- **Gebruikersbeheer**: Admin kan accounts beheren
- **Moderatie**: Admin kan ongepaste feedback verwijderen
- **Real-time**: Direct inzicht in nieuwe feedback

##  Snelle Start

### Vereisten
- Docker & Docker Compose
- Git

### Installatie

1. **Clone het project**
```bash
git clone <repository-url>
cd itprojbund
```

2. **Setup configuratie**
```bash
make dev-setup
# Of handmatig:
cp .env.example .env
```

3. **Start de applicatie**
```bash
make up
# Of handmatig:
docker-compose up -d
```

4. **Toegang tot de applicatie**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentatie: http://localhost:8000/docs

### Standaard Accounts

**Administrator:**
- Email: admin@school.local
- Gebruikersnaam: admin
- Wachtwoord: Password123!

**Test Docenten:**
- noor.jansen / Welkom123!
- bram.devries / Welkom123!
- mevr.koster / Welkom123!
- dhr.vandijk / Welkom123!

## Ontwikkeling

### Lokale Development

```bash
# Start services
make up

# Bekijk logs
make logs

# Draai tests
make test

# Stop services
make down

# Herstart alles
make restart
```

### Project Structuur

```
itprojbund/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Hoofdapplicatie
│   │   ├── models.py       # Database modellen
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── auth.py         # Authenticatie
│   │   ├── sentiment.py    # Sentiment analyse
│   │   └── routers_*.py    # API routes
│   ├── tests/              # Test suite
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile
├── frontend/               # HTML/CSS/JS frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── docker-compose.yml      # Docker configuratie
├── Makefile               # Development commands
└── README.md
```

### Database Schema

**Users** (Gebruikers)
- id, email, username, password_hash, role, is_active, created_at

**Categories** (Categorieën)
- id, name, description, is_active, sort_order

**Subjects** (Vakken)
- id, name, code, department, is_active

**Feedback** (Feedback)
- id, text, category, subject_area, sentiment_label, sentiment_score, confidence_score, word_count, is_active, created_at

##  Testing

### Automatische Tests

```bash
# Alle tests
make test

# Uitgebreide output
make test-verbose

# Specifieke test file
cd backend && python -m pytest tests/test_feedback.py -v
```

### Test Coverage

De test suite dekt:
- ✅ Authenticatie (login, JWT tokens, permissions)
- ✅ Feedback submission en validatie
- ✅ Sentiment analyse
- ✅ API endpoints en filters
- ✅ Admin functionaliteiten
- ✅ Analytics en statistieken

### Handmatige Tests

**Feedback Indienen:**
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"text":"De les was heel duidelijk uitgelegd!","category":"Didactiek","subject_area":"Wiskunde"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Password123!"}'
```

##  API Documentatie

### Publieke Endpoints

- `POST /feedback` - Feedback indienen (anoniem)
- `GET /categories` - Lijst van categorieën
- `GET /subjects` - Lijst van vakken

### Authenticatie Endpoints

- `POST /auth/login` - Inloggen
- `GET /auth/me` - Huidige gebruiker info

### Docent/Admin Endpoints

- `GET /feedback` - Feedback lijst (met filters)
- `GET /feedback/{id}` - Specifieke feedback
- `DELETE /feedback/{id}` - Feedback verwijderen (admin only)
- `GET /analytics/summary` - Statistieken
- `GET /users` - Gebruikerslijst (admin only)
- `POST /users` - Nieuwe gebruiker (admin only)

### Filters

Feedback kan gefilterd worden op:
- `category` - Categorie naam
- `sentiment` - Positive/Negative/Neutral
- `subject` - Vak naam
- `start` - Start datum (YYYY-MM-DD)
- `end` - Eind datum (YYYY-MM-DD)
- `limit` - Aantal resultaten (default: 50)
- `offset` - Offset voor paginatie

## 🔧 Configuratie

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql+psycopg2://sfp:sfp_password@db:5432/sfp

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120

# Admin Account
ADMIN_EMAIL=admin@school.local
ADMIN_PASSWORD=Password123!

# CORS
CORS_ALLOW_ORIGINS=*

# Sentiment Analysis
POSITIVE_THRESHOLD=0.1
NEGATIVE_THRESHOLD=-0.1
```

##  Gebruik

### Voor Studenten

1. Ga naar http://localhost:3000
2. Vul je feedback in (10-1000 tekens)
3. Kies een categorie
4. Optioneel: selecteer een vak
5. Klik "Feedback Versturen"
6. Zie direct het sentiment resultaat

### Voor Docenten

1. Scroll naar "Docenten/Admin Login"
2. Log in met je account
3. Bekijk het dashboard met statistieken
4. Filter feedback op categorie, sentiment, vak of datum
5. Lees individuele feedback items

### Voor Administrators

1. Log in als admin
2. Toegang tot alle docent functies
3. Plus: gebruikersbeheer sectie
4. Kan feedback verwijderen
5. Kan nieuwe accounts aanmaken

##  Privacy & Beveiliging

- **Anonieme feedback**: Geen IP-adressen of identificeerbare informatie opgeslagen
- **JWT authenticatie**: Veilige token-based auth voor docenten/admin
- **Wachtwoord hashing**: Bcrypt voor veilige wachtwoord opslag
- **Soft delete**: Feedback wordt niet permanent verwijderd
- **CORS configuratie**: Controleerbare cross-origin requests
- **Input validatie**: Alle input wordt gevalideerd en gesanitized

 Troubleshooting

### Veelvoorkomende Problemen

**Database connectie fout:**
```bash
# Check of PostgreSQL container draait
docker-compose ps
# Herstart database
docker-compose restart db
```

**Frontend laadt niet:**
```bash
# Check of alle containers draaien
docker-compose ps
# Bekijk logs
make logs-backend
```

**Tests falen:**
```bash
# Installeer dependencies lokaal
cd backend
pip install -r requirements.txt
python -m pytest -v
```

### Logs Bekijken

```bash
# Alle services
make logs

# Alleen backend
make logs-backend

# Alleen database
make logs-db
```

### Database Reset

```bash
# Stop alles en verwijder volumes
make clean

# Start opnieuw
make up
```

##  Roadmap

- [ ] Email notificaties voor nieuwe feedback
- [ ] Export functionaliteit (CSV/PDF)
- [ ] Geavanceerde analytics (trends, grafieken)
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Integration met school systemen

##  Licentie

Dit project is gemaakt voor educatieve doeleinden.(erasmushogeschool brussel)


##  Changelog
