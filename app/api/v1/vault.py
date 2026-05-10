from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "/app/secure_storage"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_secure_file(file: UploadFile = File(...)):
    """
    Upload sécurisé d'une preuve (photo, audio, document).
    Dans une vraie prod, le fichier serait chiffré avant d'être écrit sur le disque ou envoyé sur S3.
    """
    try:
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
            
        return {"info": f"Fichier '{file.filename}' sauvegardé dans le coffre-fort avec succès."}
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
