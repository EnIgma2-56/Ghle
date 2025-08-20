from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Candidate
from ..schemas import CandidateIn, CandidateOut
from .deps import require_admin

router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.get("", response_model=list[CandidateOut])
def list_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).order_by(Candidate.position, Candidate.name).all()

@router.post("", response_model=CandidateOut)
def create_candidate(body: CandidateIn, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = Candidate(**body.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.delete("/{cid}")
def delete_candidate(cid: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    c = db.get(Candidate, cid)
    if not c: raise HTTPException(404, "Not found")
    db.delete(c); db.commit()
    return {"ok": True}
