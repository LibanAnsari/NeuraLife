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

# ==================== AUTH ROUTES ====================

@app.post("/api/auth/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user with initial NeuraCoins
    hashed_password = get_password_hash(user_data.password)
    
    # Give test users (test2-test6) 5000 NeuraCoins, others start with 0
    initial_coins = 0
    if user_data.username in ['test2', 'test3', 'test4', 'test5', 'test6']:
        initial_coins = 5000
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        neuracoins=initial_coins
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    # Generate a random state for CSRF protection
    state = secrets.token_urlsafe(32)
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")
    
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)

@app.get("/api/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:
        # Get the token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")
        
        email = user_info.get('email')
        name = user_info.get('name', '')
        google_id = user_info.get('sub')
        
        if not email:
            raise HTTPException(status_code=400, detail="Email not provided by Google")
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        is_new_user = False
        
        if not user:
            # Create new user
            is_new_user = True
            # Generate username from email or name
            username = email.split('@')[0]
            
            # Ensure username is unique
            base_username = username
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            # Create user with a random password (they'll use Google OAuth)
            random_password = secrets.token_urlsafe(32)
            hashed_password = get_password_hash(random_password)
            
            user = User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                google_id=google_id
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update google_id if not set
            if not user.google_id:
                user.google_id = google_id
                db.commit()
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        frontend_url = "http://localhost:5173"
        redirect_url = f"{frontend_url}?token={access_token}&username={user.username}&isNewUser={is_new_user}"
        
        print(f"✅ Google OAuth Success: Redirecting user '{user.username}' to frontend")
        print(f"   Redirect URL: {redirect_url[:100]}...")
        
        return RedirectResponse(url=redirect_url)
        
    except Exception as e:
        print(f"❌ Google OAuth error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@app.get("/api/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_premium": current_user.is_premium,
        "neuracoins": current_user.neuracoins,
        "created_at": current_user.created_at
    }

# ==================== PREMIUM ROUTES ====================

@app.post("/api/premium/purchase")
def purchase_premium(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Purchase NeuraLife+ subscription"""
    PREMIUM_COST = 1000
    
    if current_user.is_premium:
        raise HTTPException(status_code=400, detail="You already have NeuraLife+")
    
    if current_user.neuracoins < PREMIUM_COST:
        raise HTTPException(status_code=400, detail="Insufficient NeuraCoins")
    
    # Deduct coins and grant premium
    current_user.neuracoins -= PREMIUM_COST
    current_user.is_premium = True
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": "Successfully purchased NeuraLife+!",
        "is_premium": True,
        "remaining_coins": current_user.neuracoins
    }

# ==================== THERAPY ROUTES ====================

@app.get("/api/therapy/therapists")
def get_therapists(current_user: User = Depends(get_current_user)):
    """Get all available therapists"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    db = next(get_db())
    therapists = db.query(Therapist).filter(Therapist.is_active == True).all()
    
    return {
        "therapists": [
            {
                "id": t.id,
                "name": t.name,
                "specialization": t.specialization,
                "credentials": t.credentials,
                "experience": t.experience,
                "rating": t.rating,
                "reviews": t.reviews,
                "cost": t.cost,
                "bio": t.bio,
                "avatar": t.avatar
            }
            for t in therapists
        ]
    }

@app.get("/api/therapy/my-therapists")
def get_my_therapists(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get therapists user has opted in for"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    user_therapists = db.query(UserTherapist).filter(UserTherapist.user_id == current_user.id).all()
    therapist_ids = [ut.therapist_id for ut in user_therapists]
    
    therapists = db.query(Therapist).filter(Therapist.id.in_(therapist_ids)).all()
    
    return {
        "therapists": [
            {
                "id": t.id,
                "name": t.name,
                "specialization": t.specialization,
                "avatar": t.avatar,
                "last_session": "No sessions yet"
            }
            for t in therapists
        ]
    }

@app.post("/api/therapy/opt-in")
def opt_in_therapist(data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Opt in to a therapist"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    therapist_id = data.get("therapist_id")
    
    # Check if already opted in
    existing = db.query(UserTherapist).filter(
        UserTherapist.user_id == current_user.id,
        UserTherapist.therapist_id == therapist_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already opted in to this therapist")
    
    # Create opt-in relationship
    user_therapist = UserTherapist(
        user_id=current_user.id,
        therapist_id=therapist_id
    )
    db.add(user_therapist)
    db.commit()
    
    return {"message": "Successfully opted in"}

@app.get("/api/therapy/therapist/{therapist_id}")
def get_therapist(therapist_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get specific therapist info"""
    therapist = db.query(Therapist).filter(Therapist.id == therapist_id).first()
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    
    return {
        "id": therapist.id,
        "name": therapist.name,
        "specialization": therapist.specialization,
        "avatar": therapist.avatar,
        "bio": therapist.bio
    }

@app.post("/api/therapy/opt-in/{therapist_id}")
def opt_in_therapist(therapist_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Opt-in for a therapist (add to my therapists)"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    # Check if therapist exists
    therapist = db.query(Therapist).filter(Therapist.id == therapist_id).first()
    if not therapist:
        raise HTTPException(status_code=404, detail="Therapist not found")
    
    # Check if already opted in
    existing = db.query(UserTherapist).filter(
        UserTherapist.user_id == current_user.id,
        UserTherapist.therapist_id == therapist_id
    ).first()
    
    if existing:
        return {"message": "Already opted in for this therapist", "therapist_name": therapist.name}
    
    # Create relationship
    user_therapist = UserTherapist(
        user_id=current_user.id,
        therapist_id=therapist_id
    )
    db.add(user_therapist)
    db.commit()
    
    return {"message": "Successfully opted in for therapist", "therapist_name": therapist.name}

@app.get("/api/therapy/messages/{therapist_id}")
def get_messages(therapist_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get messages with a therapist"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == current_user.id,
        TherapyMessage.therapist_id == therapist_id
    ).order_by(TherapyMessage.timestamp).all()
    
    return {
        "messages": [
            {
                "id": m.id,
                "sender": m.sender,
                "message": m.message,
                "timestamp": m.timestamp.isoformat()
            }
            for m in messages
        ]
    }

@app.post("/api/therapy/send-message")
def send_message(data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Send message to therapist"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    therapist_id = data.get("therapist_id")
    message_text = data.get("message")
    
    # Check if user-therapist relationship exists, if not create it
    existing_relationship = db.query(UserTherapist).filter(
        UserTherapist.user_id == current_user.id,
        UserTherapist.therapist_id == therapist_id
    ).first()
    
    if not existing_relationship:
        # Create the relationship (user opts in for this therapist)
        user_therapist = UserTherapist(
            user_id=current_user.id,
            therapist_id=therapist_id
        )
        db.add(user_therapist)
        db.commit()
    
    # Send the message
    message = TherapyMessage(
        user_id=current_user.id,
        therapist_id=therapist_id,
        sender="user",
        message=message_text
    )
    db.add(message)
    db.commit()
    
    return {"message": "Message sent"}

@app.get("/api/therapy/my-sessions")
def get_my_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's therapy sessions"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    sessions = db.query(TherapySession).filter(
        TherapySession.user_id == current_user.id,
        TherapySession.status == 'accepted'
    ).all()
    
    result_sessions = []
    for session in sessions:
        therapist = db.query(Therapist).filter(Therapist.id == session.therapist_id).first()
        result_sessions.append({
            "id": session.id,
            "therapist_name": therapist.name if therapist else "Unknown",
            "date": session.date,
            "time": session.time,
            "status": session.status,
            "type": session.type
        })
    
    return {"sessions": result_sessions}

@app.post("/api/therapy/book-appointment")
def book_appointment(data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Book a therapy appointment"""
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium subscription required")
    
    therapist_id = data.get("therapist_id")
    date = data.get("date")
    time = data.get("time")
    session_type = data.get("type", "individual")
    notes = data.get("notes", "")
    
    # Create appointment with pending status
    appointment = TherapySession(
        user_id=current_user.id,
        therapist_id=therapist_id,
        date=date,
        time=time,
        type=session_type,
        notes=notes,
        status='pending'
    )
    db.add(appointment)
    db.commit()
    
    return {"message": "Appointment request sent successfully! Waiting for therapist approval."}


# ==================== THERAPIST PORTAL ROUTES ====================

@app.post("/api/therapist/login")
def therapist_login(credentials: dict, db: Session = Depends(get_db)):
    """Therapist login"""
    email = credentials.get("email")
    password = credentials.get("password")
    
    therapist = db.query(Therapist).filter(Therapist.email == email).first()
    
    if not therapist or not verify_password(password, therapist.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token (reusing the same token system)
    access_token = create_access_token(data={"sub": f"therapist_{therapist.id}"})
    
    return {
        "token": access_token,
        "therapist": {
            "id": therapist.id,
            "name": therapist.name,
            "email": therapist.email,
            "specialization": therapist.specialization
        }
    }

def get_current_therapist(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current therapist from token"""
    token = credentials.credentials
    token_data = verify_token(token)
    if token_data is None or not token_data.username.startswith("therapist_"):
        raise HTTPException(status_code=401, detail="Invalid therapist credentials")
    
    therapist_id = int(token_data.username.split("_")[1])
    therapist = db.query(Therapist).filter(Therapist.id == therapist_id).first()
    if therapist is None:
        raise HTTPException(status_code=404, detail="Therapist not found")
    return therapist

@app.get("/api/therapist/patients")
def get_therapist_patients(current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Get all patients for a therapist"""
    user_therapists = db.query(UserTherapist).filter(UserTherapist.therapist_id == current_therapist.id).all()
    user_ids = [ut.user_id for ut in user_therapists]
    
    patients = []
    for user_id in user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Get last message
            last_msg = db.query(TherapyMessage).filter(
                TherapyMessage.user_id == user_id,
                TherapyMessage.therapist_id == current_therapist.id
            ).order_by(TherapyMessage.timestamp.desc()).first()
            
            patients.append({
                "user_id": user.id,
                "username": user.username,
                "last_message": last_msg.message[:50] + "..." if last_msg and len(last_msg.message) > 50 else (last_msg.message if last_msg else None)
            })
    
    return {"patients": patients}

@app.get("/api/therapist/messages/{user_id}")
def get_therapist_messages(user_id: int, current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Get messages with a specific patient"""
    messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == user_id,
        TherapyMessage.therapist_id == current_therapist.id
    ).order_by(TherapyMessage.timestamp).all()
    
    return {
        "messages": [
            {
                "id": m.id,
                "sender": m.sender,
                "message": m.message,
                "timestamp": m.timestamp.isoformat()
            }
            for m in messages
        ]
    }

@app.post("/api/therapist/send-message")
def therapist_send_message(data: dict, current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Send message to patient"""
    user_id = data.get("user_id")
    message_text = data.get("message")
    
    message = TherapyMessage(
        user_id=user_id,
        therapist_id=current_therapist.id,
        sender="therapist",
        message=message_text
    )
    db.add(message)
    db.commit()
    
    return {"message": "Message sent"}

@app.get("/api/therapist/pending-appointments")
def get_pending_appointments(current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Get all pending appointment requests for therapist"""
    appointments = db.query(TherapySession).filter(
        TherapySession.therapist_id == current_therapist.id,
        TherapySession.status == 'pending'
    ).all()
    
    result = []
    for apt in appointments:
        user = db.query(User).filter(User.id == apt.user_id).first()
        result.append({
            "id": apt.id,
            "user_id": apt.user_id,
            "username": user.username if user else "Unknown",
            "date": apt.date,
            "time": apt.time,
            "type": apt.type,
            "notes": apt.notes,
            "created_at": apt.created_at.isoformat() if hasattr(apt, 'created_at') else None
        })
    
    return {"appointments": result}

@app.post("/api/therapist/appointments/{appointment_id}/accept")
def accept_appointment(appointment_id: int, current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Accept an appointment request"""
    appointment = db.query(TherapySession).filter(
        TherapySession.id == appointment_id,
        TherapySession.therapist_id == current_therapist.id,
        TherapySession.status == 'pending'
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = 'accepted'
    db.commit()
    
    return {"message": "Appointment accepted successfully"}

@app.post("/api/therapist/appointments/{appointment_id}/reject")
def reject_appointment(appointment_id: int, current_therapist: Therapist = Depends(get_current_therapist), db: Session = Depends(get_db)):
    """Reject an appointment request"""
    appointment = db.query(TherapySession).filter(
        TherapySession.id == appointment_id,
        TherapySession.therapist_id == current_therapist.id,
        TherapySession.status == 'pending'
    ).first()
    
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appointment.status = 'rejected'
    db.commit()
    
    return {"message": "Appointment rejected"}


# ==================== RESOURCES ROUTES ====================

@app.get("/api/resources/music")
def get_music(current_user: User = Depends(get_current_user)):
    """Get music therapy playlists"""
    return {
        "playlists": [
            {"id": 1, "title": "Peaceful Piano", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO", "duration": "3h+", "description": "Relax and focus with beautiful piano pieces"},
            {"id": 2, "title": "Deep Focus", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ", "duration": "3h+", "description": "Keep calm and focus with ambient music"},
            {"id": 3, "title": "Sleep", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp", "duration": "5h+", "description": "Gentle ambient piano to help you fall asleep"},
            {"id": 4, "title": "Calm Meditation", "url": "https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u", "duration": "2h+", "description": "Soothing meditation music"},
            {"id": 5, "title": "Nature Sounds", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4PP3DA4J0N8", "duration": "3h+", "description": "Immerse yourself in calming nature sounds"},
            {"id": 6, "title": "Stress Relief", "url": "https://open.spotify.com/playlist/37i9dQZF1DWXe9gFZP0gtP", "duration": "2h+", "description": "Music designed to reduce stress and anxiety"},
            {"id": 7, "title": "Jazz Vibes", "url": "https://open.spotify.com/playlist/37i9dQZF1DX0SM0LYsmbMT", "duration": "3h+", "description": "Smooth jazz for relaxation"},
            {"id": 8, "title": "Acoustic Chill", "url": "https://open.spotify.com/playlist/37i9dQZF1DX4E3UdUs7fUx", "duration": "4h+", "description": "Laid-back acoustic songs"},
            {"id": 9, "title": "Lo-Fi Beats", "url": "https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn", "duration": "3h+", "description": "Chill lo-fi hip hop beats"},
            {"id": 10, "title": "Ambient Relaxation", "url": "https://open.spotify.com/playlist/37i9dQZF1DX3Ogo9pFvBkY", "duration": "4h+", "description": "Ambient sounds for deep relaxation"},
            {"id": 11, "title": "Yoga & Meditation", "url": "https://open.spotify.com/playlist/37i9dQZF1DX9uKNf5jGX6m", "duration": "2h+", "description": "Perfect music for yoga and meditation"},
            {"id": 12, "title": "Classical Essentials", "url": "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0", "duration": "5h+", "description": "Timeless classical pieces for calm"},
        ]
    }

@app.get("/api/resources/meditation")
def get_meditation(current_user: User = Depends(get_current_user)):
    """Get meditation guides"""
    return {
        "meditations": [
            {"id": 1, "title": "5-Minute Breathing Exercise", "duration": "5 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=odADwWzHR24"},
            {"id": 2, "title": "Body Scan Meditation", "duration": "15 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=15q-N-_kkrU"},
            {"id": 3, "title": "Mindfulness for Anxiety", "duration": "10 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=O-6f5wQXSu8"},
            {"id": 4, "title": "Morning Meditation", "duration": "10 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=nJshjMyLW8s"},
            {"id": 5, "title": "Guided Sleep Meditation", "duration": "30 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=aEqlQvczMJQ"},
            {"id": 6, "title": "Loving-Kindness Meditation", "duration": "20 min", "difficulty": "Intermediate", "url": "https://www.youtube.com/watch?v=sz7cpV7ERsM"},
            {"id": 7, "title": "Chakra Meditation", "duration": "25 min", "difficulty": "Intermediate", "url": "https://www.youtube.com/watch?v=cH-HQpAf9l0"},
            {"id": 8, "title": "Stress Relief Meditation", "duration": "15 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=z6X5oEIg6Ak"},
            {"id": 9, "title": "Mindful Movement", "duration": "20 min", "difficulty": "Intermediate", "url": "https://www.youtube.com/watch?v=4pLUleLdwY4"},
            {"id": 10, "title": "Deep Relaxation", "duration": "30 min", "difficulty": "Intermediate", "url": "https://www.youtube.com/watch?v=nj-F9X5JskI"},
            {"id": 11, "title": "Walking Meditation", "duration": "12 min", "difficulty": "Beginner", "url": "https://www.youtube.com/watch?v=CXJcTDvLwN4"},
            {"id": 12, "title": "Transcendental Meditation", "duration": "40 min", "difficulty": "Advanced", "url": "https://www.youtube.com/watch?v=RP7SMG2VuMI"},
        ]
    }

@app.get("/api/resources/books")
def get_books(current_user: User = Depends(get_current_user)):
    """Get recommended books"""
    return {
        "books": [
            {"id": 1, "title": "The Anxiety and Phobia Workbook", "author": "Edmund J. Bourne", "url": "https://www.amazon.com/Anxiety-Phobia-Workbook-Edmund-Bourne/dp/1626252157"},
            {"id": 2, "title": "Feeling Good: The New Mood Therapy", "author": "David D. Burns", "url": "https://www.amazon.com/Feeling-Good-New-Mood-Therapy/dp/0380810336"},
            {"id": 3, "title": "The Mindful Way Through Depression", "author": "Mark Williams", "url": "https://www.amazon.com/Mindful-Way-through-Depression-Unhappiness/dp/1593851286"},
            {"id": 4, "title": "Dare: The New Way to End Anxiety", "author": "Barry McDonagh", "url": "https://www.amazon.com/Dare-Anxiety-Stop-Panic-Attacks/dp/0956596258"},
            {"id": 5, "title": "The Body Keeps the Score", "author": "Bessel van der Kolk", "url": "https://www.amazon.com/Body-Keeps-Score-Healing-Trauma/dp/0143127748"},
            {"id": 6, "title": "Lost Connections", "author": "Johann Hari", "url": "https://www.amazon.com/Lost-Connections-Uncovering-Depression-Unexpected/dp/1632868318"},
            {"id": 7, "title": "Man's Search for Meaning", "author": "Viktor E. Frankl", "url": "https://www.amazon.com/Mans-Search-Meaning-Viktor-Frankl/dp/0807014273"},
            {"id": 8, "title": "The Gifts of Imperfection", "author": "Brené Brown", "url": "https://www.amazon.com/Gifts-Imperfection-Think-Supposed-Embrace/dp/159285849X"},
            {"id": 9, "title": "Mindfulness for Beginners", "author": "Jon Kabat-Zinn", "url": "https://www.amazon.com/Mindfulness-Beginners-Reclaiming-Present-Moment/dp/1604076585"},
            {"id": 10, "title": "The Upward Spiral", "author": "Alex Korb", "url": "https://www.amazon.com/Upward-Spiral-Neuroscience-Reverse-Depression/dp/1626251207"},
            {"id": 11, "title": "Self-Compassion", "author": "Kristin Neff", "url": "https://www.amazon.com/Self-Compassion-Proven-Power-Being-Yourself/dp/0061733520"},
            {"id": 12, "title": "Atomic Habits", "author": "James Clear", "url": "https://www.amazon.com/Atomic-Habits-Proven-Build-Break/dp/0735211299"},
        ]
    }

@app.get("/api/resources/podcasts")
def get_podcasts(current_user: User = Depends(get_current_user)):
    """Get mental health podcasts"""
    return {
        "podcasts": [
            {"id": 1, "title": "The Anxiety Podcast", "host": "Anxiety United", "url": "https://open.spotify.com/show/7jDwopC9MxPTTzSqoAeY4F"},
            {"id": 2, "title": "Mental Health Happy Hour", "host": "Paul Gilmartin", "url": "https://open.spotify.com/show/1jYckhoPIVmKxRAEEaUVWc"},
            {"id": 3, "title": "The Calm Collective", "host": "Cassandra Eldridge", "url": "https://open.spotify.com/show/0tHY5YWAWPvNYKDrQKcxnz"},
            {"id": 4, "title": "Therapy for Black Girls", "host": "Dr. Joy Harden Bradford", "url": "https://open.spotify.com/show/37DOXjMd5z2IEqMgPEMb3t"},
            {"id": 5, "title": "The Hilarious World of Depression", "host": "John Moe", "url": "https://open.spotify.com/show/5XZT90DslQPGvEkTn1vTGe"},
            {"id": 6, "title": "Unlocking Us", "host": "Brené Brown", "url": "https://open.spotify.com/show/4P86ZzHf7EOlRG7do9LkKZ"},
            {"id": 7, "title": "The Mindful Kind", "host": "Rachael Kable", "url": "https://open.spotify.com/show/6HFBC6KiG1M2SxxQx2P0S9"},
            {"id": 8, "title": "On Being", "host": "Krista Tippett", "url": "https://open.spotify.com/show/0r2XmtZlQBvabj88fCdm1r"},
            {"id": 9, "title": "The Happiness Lab", "host": "Dr. Laurie Santos", "url": "https://open.spotify.com/show/3i5TCKhc6GY42pOWkpWveG"},
            {"id": 10, "title": "Terrible, Thanks for Asking", "host": "Nora McInerny", "url": "https://open.spotify.com/show/7ATWfFH1jwZWrUrKXvnQlg"},
            {"id": 11, "title": "The Mind Deconstructed", "host": "Various", "url": "https://open.spotify.com/show/4cxQx9O3DKI0cLZhqPj8Bo"},
            {"id": 12, "title": "Self-Care with Shaheen", "host": "Shaheen Halim", "url": "https://open.spotify.com/show/2YvNp6g4YdVMGBOQqjWxGz"},
        ]
    }

@app.get("/api/resources/videos")
def get_videos(current_user: User = Depends(get_current_user)):
    """Get educational videos"""
    return {
        "videos": [
            {"id": 1, "title": "Understanding Anxiety", "duration": "12 min", "url": "https://www.youtube.com/watch?v=OpBhbGoADkU"},
            {"id": 2, "title": "Coping with Depression", "duration": "18 min", "url": "https://www.youtube.com/watch?v=z-IR48Mb3W0"},
            {"id": 3, "title": "Stress Management Techniques", "duration": "15 min", "url": "https://www.youtube.com/watch?v=hnpQrMqDoqE"},
            {"id": 4, "title": "Cognitive Behavioral Therapy Explained", "duration": "20 min", "url": "https://www.youtube.com/watch?v=0ViaCs0k2jM"},
            {"id": 5, "title": "How to Deal with Panic Attacks", "duration": "10 min", "url": "https://www.youtube.com/watch?v=8Un_Vcf2NNk"},
            {"id": 6, "title": "Building Self-Esteem", "duration": "14 min", "url": "https://www.youtube.com/watch?v=w-HYZv6HzAs"},
            {"id": 7, "title": "Mindfulness and Mental Health", "duration": "16 min", "url": "https://www.youtube.com/watch?v=mjtK6X1vKGI"},
            {"id": 8, "title": "Breaking the Cycle of Negative Thinking", "duration": "22 min", "url": "https://www.youtube.com/watch?v=EgNy1Kq5xOU"},
            {"id": 9, "title": "The Science of Happiness", "duration": "18 min", "url": "https://www.youtube.com/watch?v=GXy__kBVq1M"},
            {"id": 10, "title": "Overcoming Social Anxiety", "duration": "15 min", "url": "https://www.youtube.com/watch?v=oU5S8lPBH6g"},
            {"id": 11, "title": "Managing PTSD Symptoms", "duration": "25 min", "url": "https://www.youtube.com/watch?v=e_jgykOqIUY"},
            {"id": 12, "title": "Self-Care Strategies for Mental Health", "duration": "13 min", "url": "https://www.youtube.com/watch?v=w0iZJDxdw2I"},
        ]
    }

# ==================== CHATBOT ROUTES ====================

@app.post("/api/chatbot/sessions")
def create_chat_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new chat session"""
    session_id = str(uuid.uuid4())
    
    new_session = ChatSession(
        user_id=current_user.id,
        session_id=session_id,
        title="New Conversation"
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "session_id": session_id,
        "title": new_session.title,
        "created_at": new_session.created_at
    }

@app.get("/api/chatbot/sessions")
def get_chat_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all chat sessions for the current user"""
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()
    
    return {
        "sessions": [
            {
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at
            }
            for session in sessions
        ]
    }

@app.post("/api/chatbot/message")
def send_message(message: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Send message to chatbot using LangGraph and Gemini"""
    user_message = message.get("message", "")
    session_id = message.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required")
    
    # Verify session belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    try:
        # Get chatbot instance and generate response
        from app.chatbot_service import get_chatbot
        chatbot = get_chatbot()
        result = chatbot.chat(user_message, session_id)
        
        response_text = result["response"]
        emotion = result.get("emotion", "neutral")
        
        # Update session title if it's the first message
        message_count = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).count()
        
        if message_count == 0 and len(user_message) > 0:
            # Use first message as title (truncated)
            session.title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            db.commit()
        
        # Save to database
        chat = ChatMessage(
            user_id=current_user.id,
            session_id=session_id,
            message=user_message,
            response=response_text,
            emotion=emotion
        )
        db.add(chat)
        
        # Update session timestamp to current time
        session.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(session)  # Refresh to get the updated timestamp
        
        return {
            "response": response_text,
            "emotion": emotion,
            "session_id": session_id
        }
    except ValueError as e:
        # This catches the "GOOGLE_API_KEY not found" error
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Configuration error: {str(e)}. Ensure backend/.env contains GOOGLE_API_KEY (or GEMINI_API_KEY). Restart backend after changes.")
    except Exception as e:
        # Log the full error for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/api/chatbot/history/{session_id}")
def get_chat_history(session_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get chat history for a specific session"""
    # Verify session belongs to user
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return {
        "session_id": session_id,
        "title": session.title,
        "history": [
            {
                "id": msg.id,
                "message": msg.message,
                "response": msg.response,
                "emotion": msg.emotion,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }

@app.delete("/api/chatbot/sessions/{session_id}")
def delete_chat_session(session_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete a chat session"""
    session = db.query(ChatSession).filter(
        ChatSession.session_id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Delete associated messages
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    
    # Delete session
    db.delete(session)
    db.commit()
    
    return {"message": "Session deleted successfully"}

# ==================== QUIZ ROUTES ====================

@app.get("/api/quiz/list")
def get_quizzes(current_user: User = Depends(get_current_user)):
    """Get available quizzes - standardized clinical screening tools"""
    return {
        "quizzes": [
            {"id": "phq9", "title": "PHQ-9 (Depression)", "questions": 9, "description": "Patient Health Questionnaire - 9 item depression scale"},
            {"id": "gad7", "title": "GAD-7 (Anxiety)", "questions": 7, "description": "Generalized Anxiety Disorder - 7 item scale"},
            {"id": "pss10", "title": "PSS-10 (Stress)", "questions": 10, "description": "Perceived Stress Scale - 10 item version"},
        ]
    }

@app.get("/api/quiz/{quiz_id}")
def get_quiz(quiz_id: str, current_user: User = Depends(get_current_user)):
    """Get specific quiz questions - standardized clinical screening tools"""
    
    # PHQ-9: Patient Health Questionnaire (Depression)
    phq9_options = [
        "Not at all",
        "Several days",
        "More than half the days",
        "Nearly every day"
    ]
    
    # GAD-7: Generalized Anxiety Disorder (Anxiety)
    gad7_options = [
        "Not at all",
        "Several days",
        "More than half the days",
        "Nearly every day"
    ]
    
    # PSS-10: Perceived Stress Scale (Stress)
    pss10_options = [
        "Never",
        "Almost never",
        "Sometimes",
        "Fairly often",
        "Very often"
    ]
    
    quizzes = {
        "phq9": {
            "id": "phq9",
            "title": "PHQ-9: Patient Health Questionnaire",
            "description": "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            "questions": [
                {"id": 1, "question": "Little interest or pleasure in doing things", "options": phq9_options},
                {"id": 2, "question": "Feeling down, depressed, or hopeless", "options": phq9_options},
                {"id": 3, "question": "Trouble falling or staying asleep, or sleeping too much", "options": phq9_options},
                {"id": 4, "question": "Feeling tired or having little energy", "options": phq9_options},
                {"id": 5, "question": "Poor appetite or overeating", "options": phq9_options},
                {"id": 6, "question": "Feeling bad about yourself - or that you are a failure or have let yourself or your family down", "options": phq9_options},
                {"id": 7, "question": "Trouble concentrating on things, such as reading the newspaper or watching television", "options": phq9_options},
                {"id": 8, "question": "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual", "options": phq9_options},
                {"id": 9, "question": "Thoughts that you would be better off dead, or of hurting yourself in some way", "options": phq9_options},
            ]
        },
        "gad7": {
            "id": "gad7",
            "title": "GAD-7: Generalized Anxiety Disorder Scale",
            "description": "Over the last 2 weeks, how often have you been bothered by the following problems?",
            "questions": [
                {"id": 1, "question": "Feeling nervous, anxious, or on edge", "options": gad7_options},
                {"id": 2, "question": "Not being able to stop or control worrying", "options": gad7_options},
                {"id": 3, "question": "Worrying too much about different things", "options": gad7_options},
                {"id": 4, "question": "Trouble relaxing", "options": gad7_options},
                {"id": 5, "question": "Being so restless that it's hard to sit still", "options": gad7_options},
                {"id": 6, "question": "Becoming easily annoyed or irritable", "options": gad7_options},
                {"id": 7, "question": "Feeling afraid as if something awful might happen", "options": gad7_options},
            ]
        },
        "pss10": {
            "id": "pss10",
            "title": "PSS-10: Perceived Stress Scale",
            "description": "In the last month, how often have you experienced the following?",
            "questions": [
                {"id": 1, "question": "How often have you been upset because of something that happened unexpectedly?", "options": pss10_options},
                {"id": 2, "question": "How often have you felt that you were unable to control the important things in your life?", "options": pss10_options},
                {"id": 3, "question": "How often have you felt nervous and stressed?", "options": pss10_options},
                {"id": 4, "question": "How often have you felt confident about your ability to handle your personal problems?", "options": pss10_options, "reverse": True},
                {"id": 5, "question": "How often have you felt that things were going your way?", "options": pss10_options, "reverse": True},
                {"id": 6, "question": "How often have you found that you could not cope with all the things that you had to do?", "options": pss10_options},
                {"id": 7, "question": "How often have you been able to control irritations in your life?", "options": pss10_options, "reverse": True},
                {"id": 8, "question": "How often have you felt that you were on top of things?", "options": pss10_options, "reverse": True},
                {"id": 9, "question": "How often have you been angered because of things that were outside of your control?", "options": pss10_options},
                {"id": 10, "question": "How often have you felt difficulties were piling up so high that you could not overcome them?", "options": pss10_options},
            ]
        }
    }
    
    if quiz_id not in quizzes:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return quizzes[quiz_id]

@app.post("/api/quiz/{quiz_id}/submit")
def submit_quiz(quiz_id: str, answers: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Submit quiz answers - uses clinical scoring algorithms"""
    user_answers = answers.get("answers", [])
    
    # Calculate score based on the specific quiz
    score = 0
    result_text = ""
    severity = ""
    
    if quiz_id == "phq9":
        # PHQ-9 Scoring: Each item scored 0-3, total 0-27
        score = sum(user_answers)
        
        # PHQ-9 Interpretation (Clinical Standard)
        if score <= 4:
            severity = "Minimal"
            result_text = "Minimal depression. Your symptoms suggest minimal or no depression."
        elif score <= 9:
            severity = "Mild"
            result_text = "Mild depression. Your symptoms suggest mild depression. Consider monitoring your symptoms."
        elif score <= 14:
            severity = "Moderate"
            result_text = "Moderate depression. Your symptoms suggest moderate depression. Consider professional support."
        elif score <= 19:
            severity = "Moderately Severe"
            result_text = "Moderately severe depression. Your symptoms suggest moderately severe depression. Professional treatment is recommended."
        else:
            severity = "Severe"
            result_text = "Severe depression. Your symptoms suggest severe depression. Please seek professional help immediately."
            
        # Check for suicide risk (question 9)
        if user_answers[8] > 0:  # Question 9 about self-harm
            result_text += " ⚠️ IMPORTANT: You indicated thoughts of self-harm. Please contact a mental health professional or call 988 immediately."
    
    elif quiz_id == "gad7":
        # GAD-7 Scoring: Each item scored 0-3, total 0-21
        score = sum(user_answers)
        
        # GAD-7 Interpretation (Clinical Standard)
        if score <= 4:
            severity = "Minimal"
            result_text = "Minimal anxiety. Your symptoms suggest minimal or no anxiety."
        elif score <= 9:
            severity = "Mild"
            result_text = "Mild anxiety. Your symptoms suggest mild anxiety. Consider stress management techniques."
        elif score <= 14:
            severity = "Moderate"
            result_text = "Moderate anxiety. Your symptoms suggest moderate anxiety. Professional support may be beneficial."
        else:
            severity = "Severe"
            result_text = "Severe anxiety. Your symptoms suggest severe anxiety. Please consider seeking professional help."
    
    elif quiz_id == "pss10":
        # PSS-10 Scoring: Items 4, 5, 7, 8 are reverse scored
        # Regular scoring: 0-4, Reverse scoring: 4-0
        reverse_items = [3, 4, 6, 7]  # 0-indexed (questions 4, 5, 7, 8)
        
        for i, answer in enumerate(user_answers):
            if i in reverse_items:
                score += (4 - answer)  # Reverse score
            else:
                score += answer
        
        # PSS-10 Interpretation (range 0-40)
        if score <= 13:
            severity = "Low"
            result_text = "Low stress. You are experiencing low levels of stress. Your coping strategies seem effective."
        elif score <= 26:
            severity = "Moderate"
            result_text = "Moderate stress. You are experiencing moderate stress levels. Consider implementing stress management techniques."
        else:
            severity = "High"
            result_text = "High stress. You are experiencing high stress levels. Professional support and stress management strategies are recommended."
    
    else:
        raise HTTPException(status_code=400, detail="Invalid quiz type")
    
    # Check if this is the first time completing this quiz type
    previous_results = db.query(QuizResult).filter(
        QuizResult.user_id == current_user.id,
        QuizResult.quiz_type == quiz_id
    ).count()
    
    is_first_time = (previous_results == 0)
    coins_earned = 0
    
    # Save result
    quiz_result = QuizResult(
        user_id=current_user.id,
        quiz_type=quiz_id,
        score=score,
        result_text=f"{severity}: {result_text}"
    )
    db.add(quiz_result)
    
    # Award 500 NeuraCoins for first-time completion
    if is_first_time:
        coins_earned = 500
        current_user.neuracoins += coins_earned
    
    db.commit()
    db.refresh(quiz_result)
    
    return {
        "quiz_id": quiz_id,
        "score": score,
        "severity": severity,
        "result": result_text,
        "result_id": quiz_result.id,
        "first_time_completion": is_first_time,
        "coins_earned": coins_earned,
        "total_coins": current_user.neuracoins
    }

@app.get("/api/quiz/results/{result_id}")
def get_quiz_result(result_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get quiz result"""
    result = db.query(QuizResult).filter(
        QuizResult.id == result_id,
        QuizResult.user_id == current_user.id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return {
        "id": result.id,
        "quiz_type": result.quiz_type,
        "score": result.score,
        "result": result.result_text,
        "created_at": result.created_at
    }

# ============================================================================
# ADMIN API ENDPOINTS
# ============================================================================

@app.get("/api/admin/users")
def get_all_users(db: Session = Depends(get_db)):
    """Get all users for admin dashboard"""
    users = db.query(User).all()
    return [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_premium": user.is_premium,
        "neuracoins": user.neuracoins,
        "created_at": user.created_at
    } for user in users]

@app.get("/api/admin/therapists")
def get_all_therapists(db: Session = Depends(get_db)):
    """Get all therapists for admin dashboard"""
    therapists = db.query(Therapist).all()
    result = []
    for therapist in therapists:
        session_count = db.query(TherapySession).filter(
            TherapySession.therapist_id == therapist.id
        ).count()
        result.append({
            "id": therapist.id,
            "name": therapist.name,
            "email": therapist.email,
            "specialization": therapist.specialization,
            "avatar": therapist.avatar,
            "session_count": session_count
        })
    return result

@app.get("/api/admin/sessions")
def get_all_sessions(db: Session = Depends(get_db)):
    """Get all therapy sessions for admin dashboard"""
    sessions = db.query(TherapySession).all()
    result = []
    for session in sessions:
        user = db.query(User).filter(User.id == session.user_id).first()
        therapist = db.query(Therapist).filter(Therapist.id == session.therapist_id).first()
        result.append({
            "id": session.id,
            "user_id": session.user_id,
            "user_username": user.username if user else "Unknown",
            "therapist_id": session.therapist_id,
            "therapist_name": therapist.name if therapist else "Unknown",
            "session_type": session.session_type,
            "date": session.date,
            "time": session.time,
            "status": session.status,
            "created_at": session.created_at
        })
    return result

@app.get("/api/admin/quiz-results")
def get_all_quiz_results(db: Session = Depends(get_db)):
    """Get all quiz results for admin dashboard"""
    results = db.query(QuizResult).all()
    result_list = []
    for quiz_result in results:
        user = db.query(User).filter(User.id == quiz_result.user_id).first()
        result_list.append({
            "id": quiz_result.id,
            "user_id": quiz_result.user_id,
            "user_username": user.username if user else "Unknown",
            "quiz_type": quiz_result.quiz_type,
            "score": quiz_result.score,
            "result": quiz_result.result_text,
            "created_at": quiz_result.created_at
        })
    return result_list

@app.put("/api/admin/users/{username}/premium")
def toggle_user_premium(username: str, premium_data: dict, db: Session = Depends(get_db)):
    """Toggle premium status for a user"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_premium = premium_data.get("is_premium", False)
    db.commit()
    
    return {
        "message": f"Premium status updated for {username}",
        "is_premium": user.is_premium
    }

@app.get("/api/admin/stats")
def get_admin_stats(db: Session = Depends(get_db)):
    """Get overall platform statistics"""
    total_users = db.query(User).count()
    premium_users = db.query(User).filter(User.is_premium == True).count()
    total_therapists = db.query(Therapist).count()
    total_sessions = db.query(TherapySession).count()
    pending_sessions = db.query(TherapySession).filter(TherapySession.status == "pending").count()
    accepted_sessions = db.query(TherapySession).filter(TherapySession.status == "accepted").count()
    total_quiz_results = db.query(QuizResult).count()
    
    return {
        "total_users": total_users,
        "premium_users": premium_users,
        "free_users": total_users - premium_users,
        "total_therapists": total_therapists,
        "total_sessions": total_sessions,
        "pending_sessions": pending_sessions,
        "accepted_sessions": accepted_sessions,
        "total_quiz_results": total_quiz_results
    }

# ================================
# MOOD TRACKING ENDPOINTS
# ================================

@app.post("/api/mood/log")
def log_mood(
    mood_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a daily mood entry"""
    from app.models import MoodEntry, Achievement
    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Check if already logged mood today
    today = datetime.now().strftime("%Y-%m-%d")
    existing = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id,
        MoodEntry.date == today
    ).first()
    
    if existing:
        # Update existing entry
        existing.mood = mood_data.get("mood")
        existing.intensity = mood_data.get("intensity", 3)
        existing.notes = mood_data.get("notes", "")
        existing.activities = mood_data.get("activities", "")
    else:
        # Create new entry
        mood_entry = MoodEntry(
            user_id=current_user.id,
            mood=mood_data.get("mood"),
            intensity=mood_data.get("intensity", 3),
            notes=mood_data.get("notes", ""),
            activities=mood_data.get("activities", ""),
            date=today
        )
        db.add(mood_entry)
    
    # Check for weekly streak achievement
    entries_this_week = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id
    ).order_by(MoodEntry.date.desc()).limit(7).all()
    
    if len(entries_this_week) == 7:
        # Award 50 NeuraCoins for weekly mood logging
        existing_achievement = db.query(Achievement).filter(
            Achievement.user_id == current_user.id,
            Achievement.achievement_type == f"mood_week_{today}"
        ).first()
        
        if not existing_achievement:
            current_user.neuracoins += 50
            achievement = Achievement(
                user_id=current_user.id,
                achievement_type=f"mood_week_{today}",
                achievement_name="7-Day Mood Tracker",
                description="Logged mood for 7 consecutive days",
                icon="📊",
                coins_earned=50
            )
            db.add(achievement)
    
    db.commit()
    
    return {
        "message": "Mood logged successfully",
        "coins_earned": 50 if len(entries_this_week) == 7 else 0,
        "total_coins": current_user.neuracoins
    }

@app.get("/api/mood/history")
def get_mood_history(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mood history for the last N days"""
    from app.models import MoodEntry
    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id
    ).order_by(MoodEntry.date.desc()).limit(days).all()
    
    return {
        "entries": [
            {
                "id": entry.id,
                "mood": entry.mood,
                "intensity": entry.intensity,
                "notes": entry.notes,
                "activities": entry.activities,
                "date": entry.date,
                "created_at": entry.created_at.isoformat()
            }
            for entry in entries
        ]
    }

@app.get("/api/mood/analytics")
def get_mood_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get mood analytics and insights"""
    from app.models import MoodEntry
    from collections import Counter
    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Get last 30 days of mood data
    entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id
    ).order_by(MoodEntry.date.desc()).limit(30).all()
    
    if not entries:
        return {"message": "No mood data yet", "entries": []}
    
    # Calculate statistics
    moods = [e.mood for e in entries]
    intensities = [e.intensity for e in entries]
    mood_counts = Counter(moods)
    
    avg_intensity = sum(intensities) / len(intensities)
    most_common_mood = mood_counts.most_common(1)[0][0] if mood_counts else "😊"
    
    return {
        "total_entries": len(entries),
        "average_intensity": round(avg_intensity, 2),
        "most_common_mood": most_common_mood,
        "mood_distribution": dict(mood_counts),
        "recent_entries": [
            {"mood": e.mood, "date": e.date, "intensity": e.intensity}
            for e in entries[:7]
        ]
    }

# ================================
# JOURNALING ENDPOINTS
# ================================

@app.post("/api/journal/entry")
def create_journal_entry(
    entry_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new journal entry"""
    from app.models import JournalEntry, Achievement
    
    # Create journal entry
    journal_entry = JournalEntry(
        user_id=current_user.id,
        title=entry_data.get("title", ""),
        content=entry_data.get("content"),
        prompt=entry_data.get("prompt", ""),
        mood=entry_data.get("mood", ""),
        is_private=entry_data.get("is_private", True)
    )
    db.add(journal_entry)
    
    # Check if already earned coins today
    today = datetime.now().strftime("%Y-%m-%d")
    existing_achievement = db.query(Achievement).filter(
        Achievement.user_id == current_user.id,
        Achievement.achievement_type == f"journal_daily_{today}"
    ).first()
    
    coins_earned = 0
    if not existing_achievement:
        # Award 50 coins for daily journaling (max 1/day)
        current_user.neuracoins += 50
        coins_earned = 50
        achievement = Achievement(
            user_id=current_user.id,
            achievement_type=f"journal_daily_{today}",
            achievement_name="Daily Journaling",
            description="Wrote in journal today",
            icon="📔",
            coins_earned=50
        )
        db.add(achievement)
    
    db.commit()
    
    return {
        "message": "Journal entry created",
        "entry_id": journal_entry.id,
        "coins_earned": coins_earned,
        "total_coins": current_user.neuracoins
    }

@app.get("/api/journal/entries")
def get_journal_entries(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all journal entries for current user"""
    from app.models import JournalEntry
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    entries = db.query(JournalEntry).filter(
        JournalEntry.user_id == current_user.id
    ).order_by(JournalEntry.created_at.desc()).limit(limit).all()
    
    return {
        "entries": [
            {
                "id": entry.id,
                "title": entry.title,
                "content": entry.content,
                "prompt": entry.prompt,
                "mood": entry.mood,
                "created_at": entry.created_at.isoformat(),
                "updated_at": entry.updated_at.isoformat()
            }
            for entry in entries
        ]
    }

@app.get("/api/journal/{entry_id}")
def get_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific journal entry"""
    from app.models import JournalEntry
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == entry_id,
        JournalEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    return {
        "id": entry.id,
        "title": entry.title,
        "content": entry.content,
        "prompt": entry.prompt,
        "mood": entry.mood,
        "created_at": entry.created_at.isoformat(),
        "updated_at": entry.updated_at.isoformat()
    }

@app.delete("/api/journal/{entry_id}")
def delete_journal_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a journal entry"""
    from app.models import JournalEntry
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == entry_id,
        JournalEntry.user_id == current_user.id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    
    db.delete(entry)
    db.commit()
    
    return {"message": "Journal entry deleted"}

# ================================
# SLEEP TRACKING ENDPOINTS
# ================================

@app.post("/api/sleep/log")
def log_sleep(
    sleep_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a sleep entry"""
    from app.models import SleepLog, Achievement
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Calculate duration
    bedtime = sleep_data.get("bedtime")  # "22:30"
    waketime = sleep_data.get("waketime")  # "07:00"
    
    from datetime import datetime, timedelta
    bed = datetime.strptime(bedtime, "%H:%M")
    wake = datetime.strptime(waketime, "%H:%M")
    
    # Handle overnight sleep
    if wake < bed:
        wake += timedelta(days=1)
    
    duration = int((wake - bed).total_seconds() / 60)  # minutes
    
    # Check if already logged sleep for this date
    date = sleep_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    existing = db.query(SleepLog).filter(
        SleepLog.user_id == current_user.id,
        SleepLog.date == date
    ).first()
    
    if existing:
        existing.bedtime = bedtime
        existing.waketime = waketime
        existing.duration = duration
        existing.quality = sleep_data.get("quality", 3)
        existing.notes = sleep_data.get("notes", "")
    else:
        sleep_log = SleepLog(
            user_id=current_user.id,
            date=date,
            bedtime=bedtime,
            waketime=waketime,
            duration=duration,
            quality=sleep_data.get("quality", 3),
            notes=sleep_data.get("notes", "")
        )
        db.add(sleep_log)
        
        # Award 30 coins per sleep log
        current_user.neuracoins += 30
    
    db.commit()
    
    return {
        "message": "Sleep logged successfully",
        "duration_minutes": duration,
        "duration_hours": round(duration / 60, 1),
        "coins_earned": 30 if not existing else 0,
        "total_coins": current_user.neuracoins
    }

@app.get("/api/sleep/history")
def get_sleep_history(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sleep history"""
    from app.models import SleepLog
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    logs = db.query(SleepLog).filter(
        SleepLog.user_id == current_user.id
    ).order_by(SleepLog.date.desc()).limit(days).all()
    
    return {
        "logs": [
            {
                "id": log.id,
                "date": log.date,
                "bedtime": log.bedtime,
                "waketime": log.waketime,
                "duration": log.duration,
                "duration_hours": round(log.duration / 60, 1),
                "quality": log.quality,
                "notes": log.notes,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
    }

@app.get("/api/sleep/insights")
def get_sleep_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sleep analytics and insights"""
    from app.models import SleepLog
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    logs = db.query(SleepLog).filter(
        SleepLog.user_id == current_user.id
    ).order_by(SleepLog.date.desc()).limit(30).all()
    
    if not logs:
        return {"message": "No sleep data yet"}
    
    avg_duration = sum(log.duration for log in logs) / len(logs)
    avg_quality = sum(log.quality for log in logs) / len(logs)
    
    # Sleep recommendations
    tips = []
    if avg_duration < 420:  # Less than 7 hours
        tips.append("Try to get 7-9 hours of sleep each night")
    if avg_quality < 3:
        tips.append("Consider improving sleep environment (dark, quiet, cool)")
    
    return {
        "total_logs": len(logs),
        "average_duration_hours": round(avg_duration / 60, 1),
        "average_quality": round(avg_quality, 1),
        "recommendations": tips
    }

# ================================
# GOAL TRACKING ENDPOINTS
# ================================

@app.post("/api/goals/create")
def create_goal(
    goal_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new goal"""
    from app.models import Goal
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    goal = Goal(
        user_id=current_user.id,
        title=goal_data.get("title"),
        description=goal_data.get("description", ""),
        category=goal_data.get("category", "self-care"),
        frequency=goal_data.get("frequency", "daily"),
        target_days=goal_data.get("target_days", "")
    )
    db.add(goal)
    db.commit()
    
    return {
        "message": "Goal created successfully",
        "goal_id": goal.id,
        "goal": {
            "id": goal.id,
            "title": goal.title,
            "category": goal.category,
            "frequency": goal.frequency,
            "current_streak": goal.current_streak
        }
    }

@app.get("/api/goals/list")
def get_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all goals for current user"""
    from app.models import Goal
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    goals = db.query(Goal).filter(
        Goal.user_id == current_user.id,
        Goal.is_active == True
    ).all()
    
    return {
        "goals": [
            {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "category": goal.category,
                "frequency": goal.frequency,
                "current_streak": goal.current_streak,
                "longest_streak": goal.longest_streak,
                "total_completions": goal.total_completions,
                "created_at": goal.created_at.isoformat()
            }
            for goal in goals
        ]
    }

@app.post("/api/goals/{goal_id}/complete")
def complete_goal(
    goal_id: int,
    completion_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a goal as completed for today"""
    from app.models import Goal, GoalCompletion, Achievement
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Check if already completed today
    today = datetime.now().strftime("%Y-%m-%d")
    existing = db.query(GoalCompletion).filter(
        GoalCompletion.goal_id == goal_id,
        GoalCompletion.date == today
    ).first()
    
    if existing:
        return {"message": "Goal already completed today"}
    
    # Create completion record
    completion = GoalCompletion(
        goal_id=goal_id,
        user_id=current_user.id,
        date=today,
        notes=completion_data.get("notes", "")
    )
    db.add(completion)
    
    # Update goal stats
    goal.total_completions += 1
    goal.current_streak += 1
    
    if goal.current_streak > goal.longest_streak:
        goal.longest_streak = goal.current_streak
    
    # Award coins for streaks
    coins_earned = 0
    if goal.current_streak == 7:
        current_user.neuracoins += 100
        coins_earned = 100
        achievement = Achievement(
            user_id=current_user.id,
            achievement_type=f"goal_streak_7_{goal_id}",
            achievement_name="7-Day Goal Streak",
            description=f"Completed '{goal.title}' for 7 days straight",
            icon="🔥",
            coins_earned=100
        )
        db.add(achievement)
    elif goal.current_streak == 30:
        current_user.neuracoins += 500
        coins_earned = 500
        achievement = Achievement(
            user_id=current_user.id,
            achievement_type=f"goal_streak_30_{goal_id}",
            achievement_name="30-Day Goal Champion",
            description=f"Completed '{goal.title}' for 30 days straight!",
            icon="🏆",
            coins_earned=500
        )
        db.add(achievement)
    
    db.commit()
    
    return {
        "message": "Goal completed!",
        "current_streak": goal.current_streak,
        "coins_earned": coins_earned,
        "total_coins": current_user.neuracoins
    }

@app.delete("/api/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete/deactivate a goal"""
    from app.models import Goal
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    goal.is_active = False
    db.commit()
    
    return {"message": "Goal deleted"}

# ================================
# HOMEWORK ENDPOINTS (Premium)
# ================================

@app.get("/api/homework/list")
def get_homework(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all homework assignments for current user"""
    from app.models import TherapyHomework
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    homework = db.query(TherapyHomework).filter(
        TherapyHomework.user_id == current_user.id
    ).order_by(TherapyHomework.assigned_at.desc()).all()
    
    # Get therapist names
    result = []
    for hw in homework:
        therapist = db.query(Therapist).filter(Therapist.id == hw.therapist_id).first()
        result.append({
            "id": hw.id,
            "title": hw.title,
            "description": hw.description,
            "due_date": hw.due_date,
            "status": hw.status,
            "submission": hw.submission,
            "therapist_feedback": hw.therapist_feedback,
            "therapist_name": therapist.name if therapist else "Unknown",
            "assigned_at": hw.assigned_at.isoformat(),
            "submitted_at": hw.submitted_at.isoformat() if hw.submitted_at else None
        })
    
    return {"homework": result}

@app.post("/api/homework/{homework_id}/submit")
def submit_homework(
    homework_id: int,
    submission_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit homework assignment"""
    from app.models import TherapyHomework
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    homework = db.query(TherapyHomework).filter(
        TherapyHomework.id == homework_id,
        TherapyHomework.user_id == current_user.id
    ).first()
    
    if not homework:
        raise HTTPException(status_code=404, detail="Homework not found")
    
    homework.submission = submission_data.get("submission")
    homework.status = "completed"
    homework.submitted_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Homework submitted successfully"}

# ================================
# ANALYTICS ENDPOINTS (Premium)
# ================================

@app.get("/api/analytics/progress")
def get_progress_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive progress analytics for premium users"""
    from app.models import MoodEntry, SleepLog, Goal, GoalCompletion
    

    
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium feature only")
    
    # Get quiz results trend
    quiz_results = db.query(QuizResult).filter(
        QuizResult.user_id == current_user.id
    ).order_by(QuizResult.created_at.desc()).limit(10).all()
    
    # Get therapy sessions count
    therapy_sessions = db.query(TherapySession).filter(
        TherapySession.user_id == current_user.id,
        TherapySession.status == "accepted"
    ).count()
    
    # Get mood data
    mood_entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id
    ).order_by(MoodEntry.date.desc()).limit(30).all()
    
    # Get sleep data
    sleep_logs = db.query(SleepLog).filter(
        SleepLog.user_id == current_user.id
    ).order_by(SleepLog.date.desc()).limit(30).all()
    
    # Get active goals
    active_goals = db.query(Goal).filter(
        Goal.user_id == current_user.id,
        Goal.is_active == True
    ).count()
    
    return {
        "quiz_results": [
            {
                "quiz_type": q.quiz_type,
                "score": q.score,
                "date": q.created_at.strftime("%Y-%m-%d")
            }
            for q in quiz_results
        ],
        "therapy_sessions_count": therapy_sessions,
        "mood_entries_count": len(mood_entries),
        "sleep_logs_count": len(sleep_logs),
        "active_goals_count": active_goals,
        "mood_trend": [
            {"date": m.date, "mood": m.mood, "intensity": m.intensity}
            for m in mood_entries[:14]
        ],
        "sleep_trend": [
            {"date": s.date, "duration_hours": round(s.duration / 60, 1), "quality": s.quality}
            for s in sleep_logs[:14]
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
