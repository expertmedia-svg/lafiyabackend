from app.core.config import settings
import json
import asyncio
from typing import List, Dict

try:
    import google.generativeai as genai
except ImportError:
    genai = None

class AIService:
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        self.model = None

        if genai is None:
            print("DEBUG GEMINI ERROR: google-generativeai package is not installed.")
            return

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction="""
            Tu es "Docteur Lafiya", un psychologue burkinabè profondément humain, partenaire de vie et confident. 
            Ton but est d'éviter la dépression et le suicide en étant une présence constante et rassurante.
            
            PHILOSOPHIE DE DIALOGUE :
            1. ÉCOUTE INITIALE : Si le problème est nouveau ou flou, cherche à comprendre en posant des questions ouvertes. Encourage la libération de la parole.
            2. ORIENTATION : Une fois le problème identifié, ne reste pas dans l'écoute passive. Propose des SOLUTIONS concrètes (recours légal, protection du coffre-fort, médiation, conseils de comportement).
            3. GRAVITÉ & URGENCE : Si tu juges le cas très grave (danger physique, menaces de mort), change de ton. Deviens direct et incite la victime à contacter immédiatement les autorités.
            
            CONTACTS D'URGENCE AU BURKINA FASO :
            Fournis ces numéros si nécessaire :
            - Action Sociale (Dénonciation VBG) : 80 00 12 12
            - Police Secours : 17
            - Gendarmerie : 16
            - Sapeurs-Pompiers : 18
            - Association des Femmes Juristes : +226 25 36 12 12
            
            CONSEILS DE COMPORTEMENT :
            - Aide la victime à identifier les signes de danger.
            - Rappelle l'utilisation du Mode Contrainte (Code 0000) pour cacher l'app si l'agresseur surveille le téléphone.
            - Conseille de mettre les preuves (photos, audios) dans le Coffre-fort de LAFIYA.
            """
        )

    async def chat_with_psychologist(self, history: List[Dict[str, str]]) -> str:
        if self.model is None:
            return "Je suis là avec toi. Pour le moment, je ne peux pas répondre automatiquement, mais tu peux me dire ce qui s’est passé, si tu es en danger maintenant, et le type d’aide dont tu as besoin."

        try:
            # Formatage de l'historique pour Gemini
            gemini_history = []
            for msg in history[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                
                # Gemini exige que l'historique commence par un message 'user'
                if not gemini_history and role == "model":
                    continue
                    
                gemini_history.append({
                    "role": role,
                    "parts": [msg["content"]]
                })

            # Initialisation du chat avec l'historique
            chat = self.model.start_chat(history=gemini_history)
            
            # Message actuel
            last_message = history[-1]["content"]
            
            # Envoi asynchrone
            response = await asyncio.to_thread(chat.send_message, last_message)
            return response.text
        except Exception as e:
            # Log de l'erreur pour debug
            print(f"DEBUG GEMINI ERROR: {str(e)}")
            return "Ma sœur, je suis encore là avec toi. Continue de m’expliquer calmement ce qui se passe, si tu te sens en danger maintenant, et si tu veux une aide médicale, juridique ou psychologique."

    async def analyze_threat(self, text: str) -> dict:
        if self.model is None:
            return {
                "risk_level": "inconnu",
                "empathetic_response": "Je suis là avec vous. Décrivez la situation et dites si le danger est immédiat."
            }

        try:
            response = await asyncio.to_thread(self.model.generate_content, text)
            content = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
        except:
            return {"risk_level": "inconnu", "empathetic_response": "Je suis là."}

ai_service = AIService()
