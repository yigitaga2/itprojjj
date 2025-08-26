from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from .database import engine, get_db
from .models import Base, User, Category, Subject
from .auth import hash_password
from .sentiment import analyze_sentiment

# Import routers
from .routers_auth import router as auth_router
from .routers_feedback import router as feedback_router
from .routers_catalog import router as catalog_router
from .routers_analytics import router as analytics_router
from .routers_users import router as users_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="School Feedback Platform", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(feedback_router, prefix="", tags=["feedback"])
app.include_router(catalog_router, prefix="", tags=["catalog"])
app.include_router(analytics_router, prefix="", tags=["analytics"])
app.include_router(users_router, prefix="/users", tags=["users"])

# Test endpoint voor sentiment analyse
@app.get("/test-sentiment")
def test_sentiment_endpoint(text: str = "test"):
    try:
        label, score, confidence = analyze_sentiment(text)
        return {
            "text": text,
            "label": label,
            "score": score,
            "confidence": confidence,
            "status": "success"
        }
    except Exception as e:
        return {
            "text": text,
            "error": str(e),
            "status": "error"
        }

@app.get("/")
def read_root():
    return {"message": "School Feedback Platform API", "version": "1.0.0"}

# Startup event to create initial data
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    
    # Create admin user
    admin_email = os.getenv("ADMIN_EMAIL", "admin@school.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "Password123!")
    
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email=admin_email,
            password_hash=hash_password(admin_password),
            role="admin"
        )
        db.add(admin_user)
        print(f"Created admin user with email: {admin_email}")
    else:
        # Update existing admin
        admin_user.email = admin_email
        admin_user.password_hash = hash_password(admin_password)
        print(f"Updated admin user: {admin_user.email}")
    
    # Create categories
    categories = [
        {"name": "Didactiek", "description": "Feedback over lesmethoden en didactische aanpak"},
        {"name": "Materiaal", "description": "Feedback over lesmateriaal en hulpmiddelen"},
        {"name": "Locaties", "description": "Feedback over klaslokalen en faciliteiten"},
        {"name": "Overig", "description": "Overige feedback en suggesties"}
    ]
    
    for cat_data in categories:
        existing_cat = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing_cat:
            category = Category(**cat_data)
            db.add(category)
            print(f"Created category: {cat_data['name']}")
    
    # Create IT subjects
    subjects = [
        {"name": "ServerOS", "description": "Server Operating Systems"},
        {"name": "Backend Web", "description": "Backend Web Development"},
        {"name": ".NET", "description": ".NET Development"},
        {"name": "Software Essentials", "description": "Software Development Essentials"},
        {"name": "IT Project", "description": "IT Project Management"}
    ]
    
    for subj_data in subjects:
        existing_subj = db.query(Subject).filter(Subject.name == subj_data["name"]).first()
        if not existing_subj:
            subject = Subject(**subj_data)
            db.add(subject)
            print(f"Created subject: {subj_data['name']}")
    
    # Create teacher users
    teachers = [
        {"username": "noor.jansen", "email": "noor.jansen@school.com", "password": "Welkom123!"},
        {"username": "pieter.de.vries", "email": "pieter.devries@school.com", "password": "Welkom123!"},
        {"username": "sarah.bakker", "email": "sarah.bakker@school.com", "password": "Welkom123!"},
        {"username": "mohamed.hassan", "email": "mohamed.hassan@school.com", "password": "Welkom123!"}
    ]
    
    for teacher_data in teachers:
        existing_teacher = db.query(User).filter(User.username == teacher_data["username"]).first()
        if not existing_teacher:
            teacher = User(
                username=teacher_data["username"],
                email=teacher_data["email"],
                password_hash=hash_password(teacher_data["password"]),
                role="teacher"
            )
            db.add(teacher)
            print(f"Created teacher: {teacher_data['username']}")
        else:
            # Update existing teacher
            existing_teacher.email = teacher_data["email"]
            existing_teacher.password_hash = hash_password(teacher_data["password"])
            print(f"Updated teacher: {existing_teacher.username}")
    
    db.commit()
    print("Database initialization completed!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
