<div align="center">

# NeuraLife

### A Comprehensive Mental Wellness Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://reactjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)

NeuraLife is a full-stack mental wellness application that provides AI-powered chatbot support, therapy session management, mood tracking, journaling, sleep tracking, and mental health assessments, all wrapped in a gamified experience with virtual currency and achievements.

[Getting Started](#getting-started) | [Features](#features) | [API Reference](#api-reference) | [Contributing](#contributing)

</div>

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#1-backend-setup-port-8000)
  - [Frontend Setup](#2-frontend-setup-port-5173)
  - [Therapist Portal Setup](#3-therapist-portal-setup-port-8080)
- [Features](#features)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Architecture

```
                  +------------------+
                  |   React Frontend |  :5173
                  |  (Tailwind CSS)  |
                  +--------+---------+
                           |
                  REST API | (Axios)
                           |
              +------------+------------+
              |    FastAPI Backend      |  :8000
              |  (JWT Auth + OAuth)     |
              +-----+----------+-------+
                    |          |
          +---------+    +-----+-------+
          | SQLite  |    | Gemini LLM  |
          | (SQLAlchemy)| | (LangGraph) |
          +----------+   +-------------+
                  |
    +-------------+-------------+
    |                           |
+---+---+              +-------+-------+
|Therapist|             | Admin Portal  |
| Portal  | :8080       |               | :9000
+---------+             +---------------+
```

## Tech Stack

| Layer          | Technology                           |
|----------------|--------------------------------------|
| **Backend**    | FastAPI, SQLAlchemy, SQLite, Uvicorn  |
| **Auth**       | JWT (python-jose), bcrypt, Google OAuth (Authlib) |
| **AI/Chatbot** | LangGraph, LangChain, Google Gemini  |
| **Frontend**   | React 18, Vite, Tailwind CSS, Axios  |
| **Therapist Portal** | Vanilla JS, Python HTTP Server |
| **Admin Portal** | HTML/JS, Python HTTP Server        |

## Project Structure

```
NeuraLife/
+-- backend/                    # FastAPI backend application
|   +-- app/
|   |   +-- __init__.py         # App package initializer
|   |   +-- main.py             # FastAPI app, routes & middleware
|   |   +-- models.py           # SQLAlchemy ORM models
|   |   +-- auth.py             # JWT & OAuth authentication
|   |   +-- database.py         # Database engine & session setup
|   |   +-- chatbot_service.py  # LangGraph chatbot with Gemini
|   +-- scripts/                # Database setup & utility scripts
|   +-- requirements.txt        # Python dependencies
|   +-- run.py                  # Backend entry point
|   +-- .env.example            # Environment variable template
+-- frontend/                   # React frontend application
|   +-- src/
|   |   +-- components/         # React components
|   |   |   +-- Dashboard.jsx         # Main user dashboard
|   |   |   +-- Login.jsx             # Auth page (login/register)
|   |   |   +-- Chatbot.jsx           # AI chatbot interface
|   |   |   +-- MoodTracker.jsx       # Mood logging & trends
|   |   |   +-- Journal.jsx           # Personal journaling
|   |   |   +-- SleepTracker.jsx      # Sleep quality tracking
|   |   |   +-- Quiz.jsx              # Mental health assessments
|   |   |   +-- Resources.jsx         # Curated resource library
|   |   |   +-- TherapySessions.jsx   # Therapist browsing & booking
|   |   |   +-- TherapyChat.jsx       # Real-time therapy messaging
|   |   |   +-- Premium.jsx           # NeuraLife+ purchase page
|   |   |   +-- BreathingExercises.jsx # Guided breathing exercises
|   |   |   +-- Navbar.jsx            # Navigation bar
|   |   +-- App.jsx             # Root component & router
|   |   +-- main.jsx            # App entry point
|   +-- package.json            # Node.js dependencies
|   +-- vite.config.js          # Vite configuration
|   +-- tailwind.config.js      # Tailwind CSS configuration
+-- therapist-portal/           # Therapist web interface
+-- admin-portal/               # Admin management interface
+-- scripts/                    # Startup & setup scripts
+-- docs/                       # Project documentation
+-- .gitignore
+-- .editorconfig
+-- LICENSE
+-- CONTRIBUTING.md
+-- CODE_OF_CONDUCT.md
+-- CHANGELOG.md
+-- README.md
```

## Getting Started

### Prerequisites

- **Python** 3.8+ ([download](https://www.python.org/downloads/))
- **Node.js** 16+ ([download](https://nodejs.org/))
- **npm** (included with Node.js)

### 1. Backend Setup (Port 8000)

```bash
# Navigate to backend
cd backend

# (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env            # Then edit .env with your API keys

# Initialize test data (first time only)
python scripts/create_test_users.py
python scripts/create_therapists.py

# Start the server
python run.py
```

The backend API will be available at **http://localhost:8000**.

> **Test Credentials:**
> - Premium User: `test1` / `123456`
> - Free Users: `test2` through `test6` / `123456`
> - Therapists: `ritvik@neuralife.com`, `liban@neuralife.com`, etc. / `123456`

### 2. Frontend Setup (Port 5173)

```bash
cd frontend
npm install
npm run dev
```

The user app will be available at **http://localhost:5173**.

### 3. Therapist Portal Setup (Port 8080)

```bash
cd therapist-portal
python server.py
```

The therapist portal will be available at **http://localhost:8080**.

### Quick Start (Windows)

Use the provided batch scripts in the `scripts/` directory:

```powershell
.\scripts\start_backend.bat      # Start backend server
.\scripts\start_frontend.bat     # Start frontend dev server (new terminal)
```

> **Note:** All three servers must be running for full functionality. Start the backend first.

## Features

### Authentication & Security
- JWT-based registration and login with token refresh
- Google OAuth 2.0 sign-in integration
- Protected routes with role-based access
- Secure password hashing with bcrypt

### AI Chatbot
- Mental health support chatbot powered by **Google Gemini** via **LangGraph**
- Emotion detection and empathetic response generation
- Persistent conversation history with session management
- Crisis resource detection and hotline information

### Mental Health Assessments
- **Anxiety**, **Depression**, and **Stress** quizzes with scored results
- Historical result tracking and progress visualization

### Wellness Tracking
- **Mood Tracker** — Daily mood logging with emoji-based input, intensity scale, and activity tags
- **Journal** — Personal entries with guided prompts and mood association
- **Sleep Tracker** — Bedtime/wake time logging with quality ratings and duration analysis
- **Goal System** — Custom wellness goals with daily/weekly tracking, streaks, and completions

### Resource Library
- 60+ curated mental health resources across 5 categories:
  - Music playlists (Spotify) | Guided meditation (YouTube) | Recommended books (Amazon) | Podcasts | Educational videos

### Premium System (NeuraLife+)
- Virtual currency (**NeuraCoins**) earned through platform engagement
- Premium dashboard with enhanced analytics
- Therapy session calendar and scheduling
- Unlocked at 1,000 NeuraCoins

### Therapy Management
- Browse 10+ professional therapist profiles with credentials and ratings
- Opt-in system to connect with multiple therapists
- Real-time bidirectional messaging (polling-based)
- Therapy homework with submission and feedback workflow

### Therapist Portal
- Dedicated web interface for therapist workflows
- Patient management dashboard with message counts and session stats
- Bidirectional messaging with patients

### Gamification & Achievements
- Achievement system with unlockable badges
- NeuraCoins rewards for consistent engagement
- Streak tracking across moods, journal, and goals

## API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Login and receive JWT token |
| `GET`  | `/api/auth/google/login` | Initiate Google OAuth flow |
| `GET`  | `/api/auth/google/callback` | Handle OAuth callback |
| `GET`  | `/api/auth/me` | Get current user profile |

### Chatbot

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chatbot/message` | Send message to AI chatbot |
| `GET`  | `/api/chatbot/history` | Retrieve conversation history |

### Resources

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/resources/music` | Music playlists (12 items) |
| `GET` | `/api/resources/meditation` | Meditation guides (12 items) |
| `GET` | `/api/resources/books` | Recommended books (12 items) |
| `GET` | `/api/resources/podcasts` | Mental health podcasts (12 items) |
| `GET` | `/api/resources/videos` | Educational videos (12 items) |

### Quizzes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/quiz/list` | List available quizzes |
| `GET`  | `/api/quiz/{id}` | Get quiz questions |
| `POST` | `/api/quiz/{id}/submit` | Submit quiz answers |
| `GET`  | `/api/quiz/results/{id}` | Get quiz results |

### Premium & Therapy

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/premium/purchase` | Purchase NeuraLife+ (1000 coins) |
| `GET`  | `/api/therapy/therapists` | List all therapists |
| `POST` | `/api/therapy/opt-in` | Connect with a therapist |
| `GET`  | `/api/therapy/my-therapists` | Get connected therapists |
| `GET`  | `/api/therapy/messages/{therapist_id}` | Get messages |
| `POST` | `/api/therapy/send-message` | Send message to therapist |
| `GET`  | `/api/therapy/sessions` | Get therapy sessions |

### Therapist Portal

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/therapist/login` | Therapist authentication |
| `GET`  | `/api/therapist/patients` | Get therapist's patients |
| `GET`  | `/api/therapist/messages/{user_id}` | Get messages with patient |
| `POST` | `/api/therapist/send-message` | Send message to patient |

## Environment Variables

Create a `.env` file in the `backend/` directory (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy database URI | `sqlite:///./mental_health.db` |
| `SECRET_KEY` | JWT signing secret | (required) |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |
| `GOOGLE_API_KEY` | Google Gemini API key for chatbot | (required for chatbot) |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | (optional) |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | (optional) |
| `GOOGLE_REDIRECT_URI` | OAuth redirect URI | `http://localhost:8000/api/auth/google/callback` |

## Development

### Running in Development Mode

```bash
# Backend with auto-reload
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend with HMR
cd frontend && npm run dev
```

### Project Scripts

| Script | Description |
|--------|-------------|
| `scripts/start_backend.bat` | Start the backend server |
| `scripts/start_frontend.bat` | Start the frontend dev server |
| `scripts/setup_everything.bat` | Full project setup |
| `scripts/setup_users.bat` | Create test users and therapists |

### Code Style

- **Python:** PEP 8, type hints, docstrings on public functions
- **JavaScript/React:** ESLint config included, functional components with hooks
- **CSS:** Tailwind CSS utility-first approach

## Troubleshooting

### Database Issues

```bash
# Reset the database
cd backend
rm mental_health.db              # Windows: del mental_health.db
python scripts/create_test_users.py
python scripts/create_therapists.py
python run.py
```

### Port Conflicts

```bash
# Find process using a port
netstat -ano | findstr :<port>
# Kill the process
taskkill /PID <process_id> /F
```

### CORS Errors

The backend allows requests from:
- `http://localhost:5173` (Frontend)
- `http://localhost:8080` (Therapist Portal)
- `http://localhost:9000` (Admin Portal)

Update `backend/app/main.py` if you change ports.

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
