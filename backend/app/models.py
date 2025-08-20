from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, nullable=False)  # email for admin, student_id for students
    name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.student)
    password_hash = Column(String, nullable=False)

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    manifesto = Column(String, nullable=True)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    position = Column(String, nullable=False)  # copy of candidate.position
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("student_id", "position", name="uq_vote_student_position"),
    )

    student = relationship("User")
    candidate = relationship("Candidate")

class ElectionStateEnum(str, enum.Enum):
    Open = "Open"
    Closed = "Closed"

class Election(Base):
    __tablename__ = "election"
    id = Column(Integer, primary_key=True)  # always 1 row
    status = Column(Enum(ElectionStateEnum), nullable=False, default=ElectionStateEnum.Open)
