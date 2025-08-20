from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .models import User, RoleEnum, Candidate, Election, ElectionStateEnum
from .security import hash_password

# Create the app with explicit docs paths
app = FastAPI(
    title="SecureVote API",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
)

# CORS for dev servers (add or remove ports you use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", "http://localhost:5500",
        "http://127.0.0.1:5173", "http://localhost:5173",
        "http://localhost:63342", "http://127.0.0.1:63342",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables + seed on startup
@app.on_event("startup")
def startup():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Seed data if empty
    db: Session = SessionLocal()
    try:
        created = False

        # admin
        if not db.query(User).filter(User.role == RoleEnum.admin).first():
            admin = User(
                identifier="admin@school.edu",
                name="Super Admin",
                role=RoleEnum.admin,
                password_hash=hash_password("admin123"),
            )
            db.add(admin)
            created = True

        # students
        if db.query(User).filter(User.role == RoleEnum.student).count() == 0:
            for i in range(1, 6):
                s = User(
                    identifier=f"STU{i:03}",
                    name=f"Student {i}",
                    role=RoleEnum.student,
                    password_hash=hash_password("student123"),
                )
                db.add(s)
            created = True

        # candidates
        if db.query(Candidate).count() == 0:
            demo = [
                ("Ama Asante", "President"),
                ("Kojo Mensah", "President"),
                ("Efua Danquah", "Secretary"),
                ("Yaw Boateng", "Secretary"),
            ]
            for name, pos in demo:
                db.add(Candidate(name=name, position=pos, photo_url=None, manifesto=""))
            created = True

        # default election row
        if not db.get(Election, 1):
            db.add(Election(id=1, status=ElectionStateEnum.Open))
            created = True

        if created:
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Routers
from .routers import auth, candidates, election, votes, results  # after app is defined

app.include_router(auth.router, prefix="/api")
app.include_router(candidates.router, prefix="/api")
app.include_router(election.router, prefix="/api")
app.include_router(votes.router, prefix="/api")
app.include_router(results.router, prefix="/api")

@app.get("/api/healthz")
def healthz():
    return {"ok": True}
