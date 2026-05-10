from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.cycle_journal_entry import CycleJournalEntry
from app.models.user import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

class CycleData(BaseModel):
    last_period: datetime
    cycle_length: int


class CycleJournalEntryPayload(BaseModel):
    date: str
    lifeStage: Optional[str] = None
    discharge: Optional[str] = None
    cycleLength: Optional[int] = None
    temperature: Optional[float] = None
    sleepHours: Optional[float] = None
    stressLevel: Optional[float] = None
    energyLevel: Optional[float] = None
    activityMinutes: Optional[float] = None
    symptomScore: Optional[float] = None
    symptoms: List[str] = Field(default_factory=list)
    moods: List[str] = Field(default_factory=list)
    consultations: List[Dict[str, str]] = Field(default_factory=list)
    ovulationLabel: Optional[str] = None
    fertileWindowStartLabel: Optional[str] = None
    fertileWindowEndLabel: Optional[str] = None
    aiAnalysis: Dict[str, Any] = Field(default_factory=dict)


class CycleJournalSyncPayload(BaseModel):
    cycleLength: Optional[int] = None
    periodLength: Optional[int] = None
    lutealPhaseDays: Optional[int] = None
    fertileDaysBeforeOvulation: Optional[int] = None
    fertileDaysAfterOvulation: Optional[int] = None
    lifeStage: Optional[str] = None
    selectedDischarge: Optional[str] = None
    historyInsightFilter: Optional[str] = None
    selectedSymptoms: List[str] = Field(default_factory=list)
    selectedMoodTags: List[str] = Field(default_factory=list)
    history: List[CycleJournalEntryPayload] = Field(default_factory=list)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
      subject = payload.get("sub")
      if subject is None:
          raise credentials_exception
      user_id = int(subject)
    except (JWTError, ValueError):
      raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user

@router.post("/predict")
async def predict_cycle(data: CycleData):
    """
    Calcule les prédictions pour le prochain cycle.
    """
    next_period = data.last_period + timedelta(days=data.cycle_length)
    ovulation = next_period - timedelta(days=14)
    
    return {
        "next_period": next_period,
        "ovulation": ovulation,
        "fertile_window": {
            "start": ovulation - timedelta(days=3),
            "end": ovulation + timedelta(days=1)
        }
    }


@router.post("/journal/sync")
def sync_cycle_journal(
    payload: CycleJournalSyncPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    synced_dates: List[str] = []

    for entry in payload.history:
        existing = (
            db.query(CycleJournalEntry)
            .filter(
                CycleJournalEntry.user_id == current_user.id,
                CycleJournalEntry.entry_date == entry.date,
            )
            .first()
        )

        entry_payload = entry.model_dump()
        ai_summary = entry_payload.get("aiAnalysis") or {}
        life_stage = entry_payload.get("lifeStage") or payload.lifeStage

        if existing is None:
            existing = CycleJournalEntry(
                user_id=current_user.id,
                entry_date=entry.date,
                life_stage=life_stage,
                payload=entry_payload,
                ai_summary=ai_summary,
            )
            db.add(existing)
        else:
            existing.life_stage = life_stage
            existing.payload = entry_payload
            existing.ai_summary = ai_summary

        synced_dates.append(entry.date)

    db.commit()
    return {
        "status": "ok",
        "synced_entries": len(synced_dates),
        "dates": synced_dates,
    }


@router.get("/journal")
def get_cycle_journal(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    entries = (
        db.query(CycleJournalEntry)
        .filter(CycleJournalEntry.user_id == current_user.id)
        .order_by(CycleJournalEntry.entry_date.desc())
        .all()
    )
    return {
        "entries": [
            {
                "date": entry.entry_date,
                "life_stage": entry.life_stage,
                "payload": entry.payload,
                "ai_summary": entry.ai_summary,
            }
            for entry in entries
        ]
    }
