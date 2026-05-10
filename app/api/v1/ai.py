from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service
# from app.db.session import get_db

router = APIRouter()

class ThreatAnalysisRequest(BaseModel):
    message: str

@router.post("/analyze-threat")
async def analyze_threat(request: ThreatAnalysisRequest):
    """
    Analyse un message pour détecter le niveau de danger et fournir une réponse empathique.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")
        
    analysis_result = await ai_service.analyze_threat(request.message)
    return analysis_result
