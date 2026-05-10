from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from pathlib import Path

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = Path(
    os.getenv("VAULT_STORAGE_DIR", str(PROJECT_ROOT / "secure_storage"))
)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload")
async def upload_secure_file(file: UploadFile = File(...)):
    """
    Upload sécurisé d'une preuve (photo, audio, document).
    Dans une vraie prod, le fichier serait chiffré avant d'être écrit sur le disque ou envoyé sur S3.
    """
    try:
        safe_name = Path(file.filename).name
        file_location = UPLOAD_DIR / safe_name
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        return {
            "info": f"Fichier '{safe_name}' sauvegardé dans le coffre-fort avec succès.",
            "stored_name": safe_name,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def list_files():
    """Liste les fichiers du coffre fort de l'utilisatrice."""
    try:
        files = os.listdir(UPLOAD_DIR)
        return {"files": files}
    except Exception as e:
        return {"files": []}
