# Database models for School Feedback Platform
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="teacher")  # teacher, admin
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    feedback = relationship("Feedback", back_populates="category")

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    feedback = relationship("Feedback", back_populates="subject")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment_label = Column(String)  # Positive, Negative, Neutral
    sentiment_score = Column(Float)   # -1.0 to 1.0
    sentiment_confidence = Column(Float)  # 0.0 to 1.0
    category_id = Column(Integer, ForeignKey("categories.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    created_at = Column(DateTime, default=func.now())
    is_anonymous = Column(Boolean, default=True)
    
    # Relationships
    category = relationship("Category", back_populates="feedback")
    subject = relationship("Subject", back_populates="feedback")
