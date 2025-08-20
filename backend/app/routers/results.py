from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models import Candidate, Vote, User

router = APIRouter(prefix="/results", tags=["results"])

@router.get("/mini")
def mini(db: Session = Depends(get_db)):
    rows = (
        db.query(
            Candidate.id.label("candidate_id"),
            Candidate.name.label("name"),
            Candidate.position.label("position"),
            func.count(Vote.id).label("count"),
        )
        .outerjoin(Vote, Vote.candidate_id == Candidate.id)
        .group_by(Candidate.id)
        .order_by(Candidate.position, Candidate.name)
        .all()
    )
    totals = [dict(candidate_id=r.candidate_id, name=r.name, position=r.position, count=int(r.count)) for r in rows]
    total_votes = sum(r["count"] for r in totals)
    voters_voted = db.query(Vote.student_id).distinct().count()
    registered = db.query(User.id).filter(User.role == "student").count()
    turnout_pct = round((voters_voted / registered) * 100) if registered else 0
    return {"title": "President Student Council", "totals": totals, "totalVotes": total_votes,
            "registered": registered, "turnoutPct": turnout_pct}
