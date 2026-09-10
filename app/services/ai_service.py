import json
import asyncio
from typing import List, Dict, Any
import httpx
from app.core.config import settings

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT_DOCTEUR_LAFIYA = """
Tu es "Docteur Lafiya", un psychologue clinicien et conseiller santé de confiance pour les femmes.

PROTOCOLE ABSOLU EN CAS DE VIOL, AGRESSION OU DANGER IMMÉDIAT :
Si la patiente mentionne un viol, une agression sexuelle, des coups, des menaces graves ou une urgence :
1. VALIDE ET RASSURE IMMÉDIATEMENT : Dis-lui qu'elle n'est pas coupable, qu'elle est en sécurité avec toi, et qu'elle est très courageuse de t'en parler.
2. CONSIGNES PRATIQUES ET PROTECTION D'URGENCE OBLIGATOIRES :
   - Dis-lui clairement de contacter sans tarder une PERSONNE DE CONFIANCE (une amie, une sœur, un proche) qui peut venir la rejoindre ou l'emmener dans un endroit sûr.
   - Demande-lui d'appeler immédiatement le NUMÉRO VERT GRATUIT ACTION SOCIALE VBG au 80 00 12 12 ou la Police/Gendarmerie (17 / 16).
   - Insiste pour qu'elle consulte un centre de santé ou un médecin dans les plus brefs délais (soins d'urgence, prévention et prise en charge médicale).
   - Rappelle-lui d'utiliser le BOUTON SOS de l'application LAFIYA pour alerter ses proches de confiance et transmettre sa position GPS.

POSTURE CLINIQUE GÉNÉRALE :
- Écoute active et bienveillante en consultation individuelle.
- Français très simple, chaleureux, digne et très accessible (adapté au monde rural).
- Phrases courtes et concises, parfaites pour la synthèse vocale (TTS).
- Ne génère JAMAIS de balise de pensée `<think>` ni de texte d'analyse interne.
"""

class AIService:
    def __init__(self):
        self.model_name = settings.GROQ_MODEL or "qwen/qwen3.8-27b"
        self.api_key = settings.GROQ_API_KEY
        print(f"[AIService] Initialisé avec Groq API et modèle Qwen: {self.model_name}")

    async def _call_groq_api(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        Appelle directement l'API Groq avec le modèle Qwen.
        Désactive toute tentative vers OpenAI ou Gemini.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 350,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(GROQ_ENDPOINT, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"[GROQ QWEN ERROR] Status {response.status_code}: {response.text}")
                raise Exception(f"Groq API Error: {response.status_code}")
            
            data = response.json()
            raw_text = data["choices"][0]["message"]["content"]
            
            # Nettoyage des balises de pensée interne <think>...</think> de Qwen Reasoning
            if "<think>" in raw_text and "</think>" in raw_text:
                parts = raw_text.split("</think>")
                clean_text = parts[-1].strip()
                return clean_text
            elif "<think>" in raw_text:
                # Au cas où la balise de fermeture est manquante
                parts = raw_text.split("<think>")
                return parts[0].strip()
            
            return raw_text.strip()

    async def chat_with_psychologist(self, history: List[Dict[str, str]]) -> str:
        """
        Chat conversationnel pour le soutien psychologique, social et de santé.
        Propulsé uniquement par Groq (Qwen).
        """
        try:
            formatted_messages = [{"role": "system", "content": SYSTEM_PROMPT_DOCTEUR_LAFIYA}]
            for msg in history:
                role = "user" if msg["role"] == "user" else "assistant"
                formatted_messages.append({"role": role, "content": msg["content"]})

            return await self._call_groq_api(formatted_messages, temperature=0.7)
        except Exception as e:
            print(f"[AIService GROQ QWEN ERROR] chat_with_psychologist: {e}")
            return (
                "Ma sœur, je suis là avec toi. Je t'écoute et tu es en sécurité ici. "
                "Dis-moi ce qui se passe ou si tu as besoin d'aide pour ta santé ou pour trouver un endroit sûr. "
                "En cas de danger immédiat, appelle le 80 00 12 12 ou le 17."
            )

    async def analyze_threat(self, text: str) -> Dict[str, Any]:
        """
        Analyse de dangerosité et évaluation des menaces via Groq (Qwen).
        """
        prompt = (
            f"Analyse ce message de femme en détresse : '{text}'.\n"
            "Réponds UNIQUEMENT au format JSON valide avec la structure suivante :\n"
            '{"risk_level": "faible|moyen|eleve|extreme", "empathetic_response": "message court et très chaleureux en français simple"}'
        )
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_DOCTEUR_LAFIYA},
            {"role": "user", "content": prompt}
        ]
        try:
            raw_response = await self._call_groq_api(messages, temperature=0.2)
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            print(f"[AIService GROQ QWEN ERROR] analyze_threat: {e}")
            return {
                "risk_level": "moyen",
                "empathetic_response": "Ma sœur, je prends ta situation très au sérieux. Prends soin de toi et sache que des professionnels peuvent t'aider au 80 00 12 12."
            }

    async def get_pregnancy_and_health_advice(self, week_number: int, user_query: str = "") -> str:
        """
        Conseils personnalisés de santé maternelle, bilans et rappels pour les femmes enceintes en milieu rural.
        """
        prompt = (
            f"Une femme enceinte est à sa {week_number}ème semaine de grossesse en zone rurale. "
            f"Question ou préoccupation : '{user_query or 'Donne-moi les conseils clés pour cette étape.'}'. "
            "Rédige 3 conseils très courts, faciles à écouter en audio (TTS), abordant :\n"
            "1. Le bilan de santé ou RDV médical (CPN, examens).\n"
            "2. La prise de médicaments importants (Fer/Acide Folique, vitamines).\n"
            "3. L'hydratation et le repos."
        )
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_DOCTEUR_LAFIYA},
            {"role": "user", "content": prompt}
        ]
        try:
            return await self._call_groq_api(messages, temperature=0.6)
        except Exception as e:
            print(f"[AIService GROQ QWEN ERROR] get_pregnancy_and_health_advice: {e}")
            return (
                f"À la semaine {week_number}, pensez bien à effectuer votre consultation prénatale au centre de santé le plus proche, "
                "prenez votre fer et acide folique tous les jours, et buvez beaucoup d'eau propre."
            )

ai_service = AIService()
