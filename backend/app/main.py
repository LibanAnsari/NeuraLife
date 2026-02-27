from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from app.database import engine, get_db, Base, ensure_schema
import uuid
from app.models import (
    User, ChatMessage, ChatSession, QuizResult, Therapist, UserTherapist, 
    TherapyMessage, TherapySession, MoodEntry, JournalEntry, SleepLog, 
    Goal, GoalCompletion, TherapyHomework, Achievement
)
from app.auth import (
    create_access_token, 
    verify_token, 
    get_password_hash, 
    verify_password,
    UserCreate,
    UserLogin,
    Token,
    GoogleAuthResponse,
    oauth,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from dotenv import load_dotenv, find_dotenv
import os
import secrets
from starlette.requests import Request

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NeuraLife API")

# Session middleware (MUST be before CORS for OAuth to work)
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production-please"),
    max_age=3600  # 1 hour session timeout
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000", "http://localhost:8080", "http://localhost:9000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Load .env early and validate API key presence on startup for clearer errors
@app.on_event("startup")
def _startup_check_env():
    try:
        env_path = find_dotenv(usecwd=False)
        if env_path:
            load_dotenv(env_path, override=False)
    except Exception:
        # Non-fatal; continue
        pass

    # Accept multiple env var names to reduce configuration errors
    api_key = (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY"))
    if not (api_key and api_key.strip()):
        # Don't crash the app; warn in logs so other routes still work
        print("[Startup] WARNING: GOOGLE_API_KEY/GEMINI_API_KEY is not set. Chatbot route will return configuration error until set.")

    # Ensure DB schema has required columns
    try:
        ensure_schema()
    except Exception as e:
        print(f"[Startup] WARNING: Failed to ensure DB schema: {e}")

# Dependency to get current user
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
def read_root():
    return {"message": "NeuraLife API", "status": "running"}

# ==================== AUTH ROUTES =============