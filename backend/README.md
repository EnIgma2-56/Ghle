# SecureVote Backend (FastAPI)

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Default accounts
- Admin: email `admin@school.edu` / password `admin123`
- Students: identifier `STU001`..`STU005` / password `student123`

## Key endpoints
- POST `/api/auth/login` → `{ access_token, user }` (body: `{identifier,password,role}`)
- GET `/api/auth/me`
- GET `/api/candidates` / POST (admin) / DELETE (admin)
- GET `/api/election/status` / POST `/api/election/toggle` (admin)
- POST `/api/votes` (student)  — enforces one vote per position
- POST `/api/votes/batch` (optional convenience)
- GET `/api/results/mini`
- GET `/api/healthz`

SQLite DB file: `securevote.db` (created in project root on first run).
