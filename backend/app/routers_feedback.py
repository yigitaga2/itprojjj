from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .database import get_db
from .models import Feedback, Category, Subject, User
from .auth import get_current_active_user
from .sentiment import analyze_sentiment

router = APIRouter()

class FeedbackCreate(BaseModel):
    text: str
    category_id: int
    subject_id: int

@router.post("/feedback")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    # Analyze sentiment
    sentiment_label, sentiment_score, sentiment_confidence = analyze_sentiment(feedback.text)
    
    # Create feedback entry
    db_feedback = Feedback(
        text=feedback.text,
        sentiment_label=sentiment_label,
        sentiment_score=sentiment_score,
        sentiment_confidence=sentiment_confidence,
        category_id=feedback.category_id,
        subject_id=feedback.subject_id,
        is_anonymous=True
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    
    return {
        "message": "Feedback succesvol ingediend",
        "sentiment": {
            "label": sentiment_label,
            "score": sentiment_score,
            "confidence": sentiment_confidence
        }
    }

@router.get("/feedback")
def get_feedback(
    skip: int = 0, 
    limit: int = 100,
    category_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    sentiment: Optional[str] = None,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Feedback)
    
    if category_id:
        query = query.filter(Feedback.category_id == category_id)
    if subject_id:
        query = query.filter(Feedback.subject_id == subject_id)
    if sentiment:
        query = query.filter(Feedback.sentiment_label == sentiment)
    
    feedback_list = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": f.id,
            "text": f.text,
            "sentiment_label": f.sentiment_label,
            "sentiment_score": f.sentiment_score,
            "sentiment_confidence": f.sentiment_confidence,
            "category": f.category.name if f.category else None,
            "subject": f.subject.name if f.subject else None,
            "created_at": f.created_at
        }
        for f in feedback_list
    ]

@router.delete("/feedback/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Only admin can delete feedback
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Alleen admins kunnen feedback verwijderen")

    # Find feedback
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback niet gevonden")

    # Delete feedback
    db.delete(feedback)
    db.commit()

    return {"message": "Feedback succesvol verwijderd"}
