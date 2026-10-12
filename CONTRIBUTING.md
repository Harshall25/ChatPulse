# Contributing to ChatPulse

Thanks for your interest in contributing to ChatPulse.

## Project overview
ChatPulse is a real-time team chat app built with Flask, Flask-SocketIO, SQLite, HTML, CSS, and JavaScript.

## Prerequisites
- Python 3.9+
- pip
- virtual environment tooling (`python -m venv`)
- Git
- Docker (optional, for containerized runs)

## Local development setup (fresh clone)
```bash
git clone https://github.com/Harshall25/ChatPulse.git
cd ChatPulse
python -m venv .venv
source .venv/bin/activate  # Windows (PowerShell): .venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment variables and secrets
Create a local environment file (do not commit it):

```bash
cp .env.example .env
```

Supported variables:
- `SECRET_KEY` (required for production; recommended for local development)
- `FLASK_ENV` (`development` or `production`)
- `PORT` (default `5000`)
- `DATABASE_PATH` (default `chat_app.db`)
- `SOCKETIO_CORS_ALLOWED_ORIGINS` (default `*`)

### Security requirement
Never commit API keys, passwords, private tokens, real-user database files, `.env` files, or any other secrets.

## Database initialization and migrations
- The app initializes SQLite tables automatically at startup via `database.init_database()`.
- There is no migration framework yet; schema changes should be proposed in PRs with clear upgrade notes.

## Run the application
```bash
python application.py
```
Then open `http://127.0.0.1:5000`.

## Run tests and checks
Current automated checks in this repository:

```bash
python -m unittest discover -v
python -m compileall application.py database.py helpers.py
```

## Branch naming convention
Use short, descriptive branches, for example:
- `feat/room-search-a11y`
- `fix/session-secret-config`
- `docs/contributing-guide`

## Commit message convention
Use conventional-style prefixes when possible:
- `feat: add input validation for room names`
- `fix: prevent empty chat messages`
- `docs: expand deployment prerequisites`
- `test: add regression test for room deletion`

## Pull request workflow
1. Fork and create a branch from `main`.
2. Make focused changes.
3. Run checks/tests locally.
4. Open a PR using the repository PR template.
5. Link related issues (for example, `Closes #123`).
6. Respond to review feedback and keep the branch up to date.

## Review expectations
- Keep PRs scoped and readable.
- Include test evidence (command output or explanation when no tests exist).
- Update docs when behavior or setup changes.

## Coding style and testing
- Follow existing Python and frontend style patterns in this repository.
- Prefer small, isolated changes.
- Add or update tests when touching logic-heavy code.
- Avoid breaking existing chat, auth, and room flows.

## Reporting bugs and security issues
- For general bugs, open a GitHub issue using the bug-report template.
- For sensitive security concerns, avoid posting secrets publicly; contact the maintainer privately first via GitHub profile: https://github.com/Harshall25
