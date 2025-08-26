from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import get_db
from .models import Feedback, Category, Subject
from .auth import get_current_active_user

router = APIRouter()

@router.get("/analytics")
def get_analytics(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # Total feedback count
    total_feedback = db.query(Feedback).count()
    
    # Sentiment distribution
    sentiment_stats = db.query(
        Feedback.sentiment_label,
        func.count(Feedback.id).label('count')
    ).group_by(Feedback.sentiment_label).all()
    
    # Feedback by category
    category_stats = db.query(
        Category.name,
        func.count(Feedback.id).label('count')
    ).join(Feedback).group_by(Category.name).all()
    
    # Feedback by subject
    subject_stats = db.query(
        Subject.name,
        func.count(Feedback.id).label('count')
    ).join(Feedback).group_by(Subject.name).all()
    
    # Average sentiment score
    avg_sentiment = db.query(func.avg(Feedback.sentiment_score)).scalar() or 0
    
    return {
        "total_feedback": total_feedback,
        "average_sentiment": round(avg_sentiment, 3),
        "sentiment_distribution": {
            stat.sentiment_label: stat.count for stat in sentiment_stats
        },
        "feedback_by_category": {
            stat.name: stat.count for stat in category_stats
        },
        "feedback_by_subject": {
            stat.name: stat.count for stat in subject_stats
        }
    }
