from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.base import Base


class CycleJournalEntry(Base):
    __tablename__ = "cycle_journal_entries"
    __table_args__ = (
        UniqueConstraint("user_id", "entry_date", name="uq_cycle_journal_user_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    entry_date = Column(String, nullable=False, index=True)
    life_stage = Column(String, nullable=True)
    payload = Column(JSON, nullable=False)
    ai_summary = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
