from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter()

class LegalQuery(BaseModel):
    query: str

@router.post("/advice")
async def get_legal_advice(request: LegalQuery):
    """
    Fournit des conseils juridiques simplifiés basés sur les droits des femmes et les lois locales.
    """
    prompt = f"""
    En tant qu'expert juridique empathique spécialisé dans les droits des femmes en Afrique, 
    réponds à cette question : "{request.query}".
    Utilise un langage simple, explique les démarches (plainte, certificat médical) 
    et recommande toujours de consulter un vrai avocat.
    """
    # Réutiliser le service AI avec un prompt spécifique
    analysis = await ai_service.analyze_threat(prompt) 
    return analysis
