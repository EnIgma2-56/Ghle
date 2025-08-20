from pydantic import BaseModel
from typing import Optional, List

class LoginIn(BaseModel):
    identifier: str
    password: str
    role: str  # 'admin' or 'student'

class UserOut(BaseModel):
    id: int
    name: str
    role: str

class TokenOut(BaseModel):
    access_token: str
    user: UserOut

class CandidateIn(BaseModel):
    name: str
    position: str
    photo_url: Optional[str] = None
    manifesto: Optional[str] = None

class CandidateOut(CandidateIn):
    id: int

class VoteIn(BaseModel):
    candidate_id: int

class VoteItem(BaseModel):
    candidate_id: int

class VoteBatchIn(BaseModel):
    votes: List[VoteItem]
