from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import Base, engine, SessionLocal
from app import models
from app.security import hash_password
from app.routers import auth, users, candidates, votes, comments, admin

app = FastAPI(title="SecureVote API", version="1.0.0")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed admin user if configured
def seed_admin():
    with SessionLocal() as db:
        existing = db.query(models.User).filter(models.User.email == settings.ADMIN_EMAIL).first()
        if not existing:
            admin_user = models.User(
                name="Admin",
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                is_admin=True,
            )
            db.add(admin_user); db.commit()

seed_admin()

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(candidates.router)
app.include_router(votes.router)
app.include_router(comments.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "SecureVote backend is running"}
