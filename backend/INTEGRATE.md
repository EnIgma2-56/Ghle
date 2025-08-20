
# Backend Add-ons for SecureVote

This bundle adds endpoints used by your new frontend pages:

- `GET/PUT /users/me` — profile read/update
- `POST /users/change-password` — password change (uses bcrypt)
- `GET/PUT /prefs` — language & notification preferences
- `POST /contact` — contact form capture

## 1) Copy files

Place these into your backend package (alongside existing `app/` folder):

```
app/security.py
app/schemas_extra.py
app/models_extra.py
app/routers/users.py
app/routers/prefs.py
app/routers/contact.py
```

## 2) Register routers in `app/main.py`

Add these lines **after** you create the FastAPI app:

```python
from .routers import users as users_router, prefs as prefs_router, contact as contact_router
app.include_router(users_router.router, prefix="/api")
app.include_router(prefs_router.router, prefix="/api")
app.include_router(contact_router.router, prefix="/api")
```

## 3) Ensure DB tables exist

Your `startup` hook already runs `Base.metadata.create_all(bind=engine)`. Since we added new tables (`preferences`, `contact_messages`), they will be created automatically for SQLite.

## 4) Ensure auth dependency

`users.py` and `prefs.py` expect `get_current_user` to be importable from `app/routers/auth.py`. If your function lives elsewhere, update the imports accordingly.

## 5) Install dependencies

```
pip install passlib bcrypt
```

## 6) Restart server

```
uvicorn app.main:app --reload
```

## 7) Frontend wiring

- Edit Profile page → `GET/PUT /api/users/me`
- Change Password page → `POST /api/users/change-password`
- Language page → `GET/PUT /api/prefs`
- Notifications page → `GET/PUT /api/prefs`
- Contact page → `POST /api/contact`

Enjoy!
