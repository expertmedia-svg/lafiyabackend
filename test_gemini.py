import asyncio
import google.generativeai as genai
import os
import sys

# Ajouter le chemin du projet pour les imports
sys.path.append("c:/Users/BNT/Documents/PROJET LAFIYA/backend")

from app.core.config import settings
from app.services.ai_service import ai_service

async def test():
    print(f"Testing Gemini with key: {settings.GOOGLE_API_KEY[:10]}...")
    history = [{"role": "user", "content": "Bonjour"}]
    response = await ai_service.chat_with_psychologist(history)
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test())
