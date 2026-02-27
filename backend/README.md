# NeuraLife Backend

FastAPI-based REST API providing authentication, chatbot, therapy management, and wellness tracking services.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Configure your API keys
python run.py
```

## Modules

| Module | Description |
|--------|-------------|
| `app/main.py` | FastAPI application, routes, and middleware |
| `app/models.py` | SQLAlchemy ORM models (User, Therapist, MoodEntry, etc.) |
| `app/auth.py` | JWT authentication and Google OAuth integration |
| `app/database.py` | Database engine, sessions, and migration helpers |
| `app/chatbot_service.py` | LangGraph chatbot with Google Gemini LLM |

## API Documentation

Once the server is running, visit **http://localhost:8000/docs** for the interactive Swagger UI.
