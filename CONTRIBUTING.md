# Contributing to NeuraLife

Thank you for your interest in contributing to NeuraLife! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a welcoming community.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/NeuraLife.git
   cd NeuraLife
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your environment variables
python run.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Therapist Portal

```bash
cd therapist-portal
python server.py
```

## Making Changes

1. Write clear, concise commit messages following [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

2. Keep changes focused — one feature or fix per pull request.

3. Update documentation if your changes affect the public API or user-facing features.

## Pull Request Process

1. **Update** the README.md if needed with details of your changes.
2. **Ensure** your code follows the project's coding standards.
3. **Test** your changes thoroughly before submitting.
4. **Submit** a pull request with a clear title and description.
5. **Respond** to code review feedback promptly.

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines where possible

### JavaScript/React (Frontend)

- Use functional components with hooks
- Follow consistent naming conventions (PascalCase for components, camelCase for functions)
- Use Tailwind CSS utility classes for styling
- Keep components modular and reusable

### General

- Write meaningful variable and function names
- Comment complex logic, not obvious code
- Handle errors gracefully with appropriate user feedback
- Keep dependencies up to date

## Questions?

If you have questions about contributing, please open an issue for discussion.

Thank you for helping make NeuraLife better!
