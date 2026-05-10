from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter()

class MessageItem(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    history: List[MessageItem]

@router.post("/ai-chat")
async def chat_ai(payload: ChatRequest):
    try:
        # On convertit le payload en liste de dicts simple pour le service
        messages = [{"role": m.role, "content": m.content} for m in payload.history]
        response = await ai_service.chat_with_psychologist(messages)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ConnectionManager:
    def __init__(self):
        # Stocker les connexions actives: dict[user_id, WebSocket]
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Dans un cas réel, sauvegarder le message en base et le router vers le bon destinataire (ex: psy ou ONG)
            # Ici on fait un echo simulant une réponse d'assistance humaine
            await manager.send_personal_message(f"Assistant Partenaire: Nous avons bien reçu: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
