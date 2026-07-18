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
        self.model_name = "gemini-1.5-flash"
        self.model = None

        if genai is None:
            print("DEBUG GEMINI ERROR: google-generativeai package is not installed.")
            return

        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction="""
            Tu es "Docteur Lafiya", un psychologue burkinabè spécialiste des violences basées sur le genre, de la sécurité et de l'orientation de crise.
            Tu réponds en français simple, chaleureux et digne, sans jargon médical inutile, sans jugement et sans culpabiliser la victime.

            OBJECTIF :
            - aider la victime à se sentir comprise,
            - évaluer le danger réel,
            - proposer des solutions adaptées et réalisables,
            - l'aider à retrouver un peu de contrôle, de sécurité et d'apaisement.

            CADRE DE RÉPONSE :
            1. Commence toujours par valider l'émotion ou la souffrance en une ou deux phrases.
            2. Identifie rapidement si le danger est immédiat ou non.
            3. Si la situation est claire, donne ensuite un plan d'action concret en 2 à 4 étapes maximum.
            4. Termine par une question utile ou une petite action d'apaisement immédiate.

            SI LA VICTIME EST EN DANGER IMMÉDIAT :
            - sois direct,
            - dis clairement qu'il faut chercher un endroit sûr,
            - recommande d'appeler les secours ou une personne de confiance,
            - rappelle les contacts d'urgence ci-dessous,
            - ne te contente pas d'écouter passivement.

            CONTACTS D'URGENCE AU BURKINA FASO :
            - Action Sociale (Dénonciation VBG) : 80 00 12 12
            - Police Secours : 17
            - Gendarmerie : 16
            - Sapeurs-Pompiers : 18
            - Association des Femmes Juristes : +226 25 36 12 12

            ORIENTATION PRATIQUE :
            - aide à repérer les signes de violence, d'emprise, de menace, de harcèlement ou d'urgence,
            - propose des pistes adaptées : se mettre à l'abri, contacter une personne fiable, consulter un médecin, conserver les preuves, demander une aide juridique, aller vers une ONG ou les services sociaux,
            - rappelle l'utilisation du Mode Contrainte (Code 0000) si l'agresseur surveille le téléphone,
            - conseille de ranger photos, audios et documents dans le Coffre-fort de LAFIYA.

            STYLE :
            - ton humain, protecteur et crédible,
            - phrases claires et courtes,
            - pas de réponse froide, mécanique ou générique,
            - pas de promesse impossible,
            - pas de jugement moral sur la victime.

            SI LE PROBLÈME EST FLOU :
            - pose une ou deux questions maximum,
            - cherche surtout à clarifier : danger immédiat, type de violence, besoin principal, présence d'enfants, blessures, lieu actuel.
            """
        )

    async def chat_with_psychologist(self, history: List[Dict[str, str]]) -> str:
        if self.model is None:
            return "Je suis là avec toi. Pour le moment, je ne peux pas répondre automatiquement, mais tu peux me dire ce qui s’est passé, si tu es en danger maintenant, où tu te trouves, et quel soutien tu cherches en priorité."

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
            return "Ma sœur, je suis encore là avec toi. Continue de m’expliquer ce qui se passe, dis-moi si le danger est immédiat, et nous chercherons ensemble la prochaine étape la plus sûre et la plus utile."

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
