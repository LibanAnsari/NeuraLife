# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-27

### Added

- **Authentication System** — JWT-based user registration and login with Google OAuth support
- **AI Chatbot** — Mental health support chatbot powered by LangGraph and Google Gemini
- **Mental Health Quizzes** — Anxiety, depression, and stress assessments with scored results
- **Resource Library** — 60+ curated resources including music, meditation, books, podcasts, and videos
- **Premium System (NeuraLife+)** — Subscription unlocked with NeuraCoins virtual currency
- **Therapy Sessions** — Browse therapists, schedule sessions, and real-time messaging
- **Therapist Portal** — Dedicated interface for therapists to manage patients and messages
- **Admin Portal** — Administrative dashboard for system management
- **Mood Tracker** — Daily mood logging with emoji-based tracking and activity correlation
- **Journal** — Personal journaling with guided prompts and mood tagging
- **Sleep Tracker** — Sleep duration and quality logging with trend analysis
- **Goal System** — Personal wellness goals with streak tracking and completions
- **Achievements** — Gamified achievement system with NeuraCoins rewards
- **Therapy Homework** — Therapist-assigned tasks with submission and feedback workflow
- **Breathing Exercises** — Guided breathing exercise component
- **Premium Calendar** — Therapy session calendar for premium users
- **Dark Mode** — Premium dark mode theme for user and therapist portals

### Technical

- FastAPI backend with SQLAlchemy ORM and SQLite database
- React 18 frontend with Vite and Tailwind CSS
- LangGraph-based chatbot with conversation memory
- JWT authentication with refresh token support
- Google OAuth 2.0 integration via Authlib
- CORS configuration for multi-origin support
- Database schema migration helpers for SQLite
