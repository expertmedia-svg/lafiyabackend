from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class EmotionLog(BaseModel):
    user_id: int
    mood: str # joyeux, triste, peur, anxieux, calme
    stress_level: int # 1-5
    note: str = ""

@router.post("/log")
async def log_emotion(log: EmotionLog, db: Session = Depends(get_db)):
    """
    Enregistre l'état émotionnel de l'utilisatrice pour le suivi.
    """
    # En prod: sauvegarder dans une table emotional_logs
    return {"status": "success", "message": "État émotionnel enregistré.", "timestamp": datetime.now()}
