from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from datetime import datetime

router = APIRouter()

# TODO: Add JWT dependency to get current user
@router.post("/panic-wipe")
def panic_wipe(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint activé lors du Panic Mode.
    Marque le compte comme étant en mode panique sur le serveur,
    sans pour autant effacer les données vitales côté serveur.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.panic_mode_active = True
    user.panic_mode_activated_at = datetime.utcnow()
    user.local_wipe_requested = True
    user.server_data_retained = True
    
    db.commit()
    
    # L'application mobile recevra la confirmation et s'effacera localement
    return {"status": "success", "message": "Panic mode activated. Local wipe authorized. Server data retained."}
