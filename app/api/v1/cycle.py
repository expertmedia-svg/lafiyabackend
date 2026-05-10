from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

class CycleData(BaseModel):
    last_period: datetime
    cycle_length: int

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
