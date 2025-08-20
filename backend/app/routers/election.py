from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Election, ElectionStateEnum
from .deps import require_admin

router = APIRouter(prefix="/election", tags=["election"])

def get_singleton(db: Session) -> Election:
    e = db.get(Election, 1)
    if not e:
        e = Election(id=1, status=ElectionStateEnum.Open)
        db.add(e); db.commit(); db.refresh(e)
    return e

@router.get("/status")
def status(db: Session = Depends(get_db)):
    return {"status": get_singleton(db).status.value}

@router.post("/toggle")
def toggle(db: Session = Depends(get_db), _=Depends(require_admin)):
    e = get_singleton(db)
    e.status = ElectionStateEnum.Closed if e.status == ElectionStateEnum.Open else ElectionStateEnum.Open
    db.add(e); db.commit(); db.refresh(e)
    return {"status": e.status.value}

def ensure_open(db: Session):
    e = get_singleton(db)
    if e.status != ElectionStateEnum.Open:
        raise HTTPException(status_code=403, detail="Election is closed.")
