# ChatPulse

ChatPulse is a real-time team chat application built with Flask and Socket.IO. It supports lightweight authentication, chat rooms, room search, and file sharing.

## Features
- Real-time messaging with Socket.IO
- Username/password sign-in flow
- Room creation and room search
- File and image sharing in rooms
- SQLite-backed message persistence
- Docker and Render deployment support

## Tech stack
- **Backend:** Python, Flask, Flask-SocketIO, SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Runtime/Deploy:** Gunicorn, Docker, Render, Procfile

## Screenshots
Current screenshot:

<img width="1901" height="908" alt="ChatPulse screenshot" src="https://github.com/user-attachments/assets/ca31a825-2e55-4cc4-8c0a-f36bb77b8f3f" />

You can add more screenshots later under this section as the UI evolves.

## Installation and local setup
```bash
git clone https://github.com/Harshall25/ChatPulse.git
cd ChatPulse
python -m venv .venv
source .venv/bin/activate  # Windows (PowerShell): .venv\\Scripts\\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## Environment configuration
Set these values in `.env` or your shell:
- `SECRET_KEY` (required in production)
- `FLASK_ENV` (`development` or `production`)
- `PORT` (default `5000`)
- `DATABASE_PATH` (default `chat_app.db`)
- `SOCKETIO_CORS_ALLOWED_ORIGINS` (default `*`)

> Never commit `.env` files, API keys, passwords, or real-user data.

## Run the app
```bash
python application.py
```
Open `http://127.0.0.1:5000`.

## Run tests/checks
```bash
python - <<'PY'
import unittest
suite = unittest.defaultTestLoader.discover('.')
print(f"Discovered {suite.countTestCases()} test(s)")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
PY
python -m compileall application.py database.py helpers.py
```

## Docker
Build and run locally:
```bash
docker build -t chatpulse .
docker run --rm -p 5000:5000 --env-file .env chatpulse
```

Or use Compose:
```bash
docker compose up --build
```

## Deployment
See [`DEPLOYMENT.md`](./DEPLOYMENT.md) and [`render.yaml`](./render.yaml) for Render deployment guidance.

## Contributing
Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening issues or pull requests.

- Open issues: https://github.com/Harshall25/ChatPulse/issues
- New issue: https://github.com/Harshall25/ChatPulse/issues/new/choose

## Code of Conduct
Contributors are expected to follow [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## License
No license file is currently present in this repository.

Without an explicit license, others generally cannot legally reuse, modify, or distribute this code beyond rights granted by the platform terms. Choose and add a license before accepting broad external contributions.
