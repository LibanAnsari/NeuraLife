from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=True)  # For Google OAuth
    is_premium = Column(Boolean, default=False)
    neuracoins = Column(Integer, default=0)  # Start with 0, earn through activities
    created_at = Column(DateTime, default=datetime.utcnow)
    
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, default="New Conversation")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    session_id = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    emotion = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    quiz_type = Column(String, nullable=False)  # anxiety, depression, stress
    score = Column(Integer, nullable=False)
    result_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Therapist(Base):
    __tablename__ = "therapists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    credentials = Column(String, nullable=False)
    experience = Column(Integer, nullable=False)
    rating = Column(Integer, default=5)
    reviews = Column(Integer, default=0)
    cost = Column(Integer, nullable=False)  # in NeuraCoins
    bio = Column(Text)
    avatar = Column(String, default='👨‍⚕️')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserTherapist(Base):
    __tablename__ = "user_therapists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    therapist_id = Column(Integer, nullable=False)
    opted_in_at = Column(DateTime, default=datetime.utcnow)

class TherapyMessage(Base):
    __tablename__ = "therapy_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    therapist_id = Column(Integer, nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'therapist'
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

class TherapySession(Base):
    __tablename__ = "therapy_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    therapist_id = Column(Integer, nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    time = Column(String, nullable=False)  # HH:MM
    status = Column(String, default='scheduled')  # scheduled, completed, cancelled
    type = Column(String, default='Video Call')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class MoodEntry(Base):
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(String, nullable=False)  # emoji: 😊, 😐, 😢, 😰, 😡
    intensity = Column(Integer, nullable=False)  # 1-5
    notes = Column(Text, nullable=True)
    activities = Column(String, nullable=True)  # comma-separated: sleep,exercise,social
    date = Column(String, nullable=False)  # YYYY-MM-DD
    created_at = Column(DateTime, default=datetime.utcnow)

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    prompt = Column(String, nullable=True)  # Which prompt was used
    mood = Column(String, nullable=True)  # Associated mood emoji
    is_private = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SleepLog(Base):
    __tablename__ = "sleep_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    bedtime = Column(String, nullable=False)  # HH:MM
    waketime = Column(String, nullable=False)  # HH:MM
    duration = Column(Integer, nullable=False)  # minutes
    quality = Column(Integer, nullable=False)  # 1-5 stars
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # sleep, exercise, social, mindfulness, self-care
    frequency = Column(String, nullable=False)  # daily, weekly, custom
    target_days = Column(String, nullable=True)  # JSON array: ["Mon", "Wed", "Fri"]
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class GoalCompletion(Base):
    __tablename__ = "goal_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TherapyHomework(Base):
    __tablename__ = "therapy_homework"
    
    id = Column(Integer, primary_key=True, index=True)
    therapist_id = Column(Integer, ForeignKey("therapists.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(String, nullable=True)  # YYYY-MM-DD
    status = Column(String, default='assigned')  # assigned, in_progress, completed, reviewed
    submission = Column(Text, nullable=True)
    therapist_feedback = Column(Text, nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_type = Column(String, nullable=False)  # mood_streak_7, journal_10, session_5, etc.
    achievement_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    icon = Column(String, default='🏆')
    coins_earned = Column(Integer, default=0)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
