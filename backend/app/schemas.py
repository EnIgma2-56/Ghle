from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ===== Users =====
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    class Config:
        from_attributes = True

# ===== Auth =====
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

# ===== Positions & Candidates =====
class PositionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PositionOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class CandidateCreate(BaseModel):
    name: str
    manifesto: Optional[str] = None
    photo_url: Optional[str] = None
    position_id: int

class CandidateOut(BaseModel):
    id: int
    name: str
    manifesto: Optional[str] = None
    photo_url: Optional[str] = None
    position_id: int
    class Config:
        from_attributes = True

# ===== Votes =====
class VoteIn(BaseModel):
    position_id: int
    candidate_id: int

class VoteOut(BaseModel):
    id: int
    user_id: int
    position_id: int
    candidate_id: int
    created_at: datetime
    class Config:
        from_attributes = True

# ===== Comments =====
class CommentCreate(BaseModel):
    candidate_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    user_id: int
    candidate_id: int
    content: str
    created_at: datetime
    class Config:
        from_attributes = True
