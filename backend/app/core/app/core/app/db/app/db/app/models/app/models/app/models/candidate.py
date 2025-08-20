from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Text
from app.db.base import Base

class Candidate(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    election_id: Mapped[int] = mapped_column(ForeignKey("election.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), index=True)
    manifesto: Mapped[str | None] = mapped_column(Text)
    photo_url: Mapped[str | None] = mapped_column(String(512))

    election = relationship("Election", back_populates="candidates")
    comments = relationship("Comment", back_populates="candidate", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="candidate", cascade="all, delete-orphan")
