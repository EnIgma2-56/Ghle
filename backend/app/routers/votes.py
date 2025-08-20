from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Vote, Candidate, User
from ..schemas import VoteIn, VoteBatchIn
from .deps import require_student
from .election import ensure_open

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("", status_code=201)
def cast_vote(body: VoteIn, db: Session = Depends(get_db), me: User = Depends(require_student)):
    ensure_open(db)
    cand = db.get(Candidate, body.candidate_id)
    if not cand:
        raise HTTPException(404, "Candidate not found")

    exists = db.query(Vote).filter(Vote.student_id == me.id, Vote.position == cand.position).first()
    if exists:
        raise HTTPException(409, f"Already voted for {cand.position}")

    v = Vote(student_id=me.id, candidate_id=cand.id, position=cand.position)
    db.add(v); db.commit(); db.refresh(v)
    return {"id": v.id}

@router.post("/batch", status_code=201)
def cast_batch(body: VoteBatchIn, db: Session = Depends(get_db), me: User = Depends(require_student)):
    ensure_open(db)
    ids = [i.candidate_id for i in body.votes]
    if not ids:
        return {"ok": True, "count": 0}
    cands = {c.id: c for c in db.query(Candidate).filter(Candidate.id.in_(ids)).all()}
    seen_pos = set()
    for cid in ids:
        cand = cands.get(cid)
        if not cand: raise HTTPException(404, f"Candidate {cid} not found")
        if cand.position in seen_pos: raise HTTPException(400, f"Duplicate for position {cand.position}")
        seen_pos.add(cand.position)
        if db.query(Vote).filter(Vote.student_id == me.id, Vote.position == cand.position).first():
            raise HTTPException(409, f"Already voted for {cand.position}")
    for cid in ids:
        cand = cands[cid]
        db.add(Vote(student_id=me.id, candidate_id=cand.id, position=cand.position))
    db.commit()
    return {"ok": True, "count": len(ids)}
