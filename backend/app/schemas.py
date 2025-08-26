from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class Subject(SubjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FeedbackBase(BaseModel):
    text: str
    category_id: int
    subject_id: int

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    sentiment_label: Optional[str]
    sentiment_score: Optional[float]
    sentiment_confidence: Optional[float]
    is_anonymous: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
