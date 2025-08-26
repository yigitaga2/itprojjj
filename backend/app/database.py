from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Database URL - gebruik PostgreSQL in productie, SQLite voor development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./school_feedback.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
