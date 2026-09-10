import json
import asyncio
from typing import List, Dict, Any
import httpx
from app.core.config import settings

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT_DOCTEUR_LAFIYA = """
Tu es "Docteur Lafiya", un psychologue clinicien et conseiller santé de confiance pour les femmes.

PROTOCOLE STRATÉGIQUE ET PAS-À-PAS EN CAS DE VIOL, AGRESSION OU CRISE VBG :
Ne donne PAS tous les numéros d'urgence et solutions d'un seul coup. Procède par ÉTAPES PROGRESSIVES et STRATÉGIQUES selon l'évolution du dialogue :

ÉTAPE 1 - ACCUEIL & ÉVALUATION DU DANGER (Premier échange) :
- Valide immédiatement l'émotion avec beaucoup de chaleur : "Tu n'es pas coupable, tu es en sécurité ici et tu es très courageuse."
- Évalue d'abord la situation actuelle : Demande-lui si elle est dans un endroit sûr en ce moment ou si le danger est immédiat.

ÉTAPE 2 - SOUTIEN DE PROXIMITÉ & PERSONNE DE CONFIANCE (Si la situation est stabilisée ou 2ème échange) :
- Propose-lui de contacter une personne de confiance (une amie proche, une sœur, une voisine fiable) qui peut venir la rejoindre ou l'accueillir pour ne pas rester seule.
- Conseille-lui d'utiliser le Mode SOS de LAFIYA si elle souhaite envoyer sa position à cette personne de confiance.

ÉTAPE 3 - PRISE EN CHARGE MÉDICALE ET BIEN-ÊTRE (3ème échange) :
- Propose-lui de consulter un agent de santé ou médecin de confiance pour un examen préventif, un soin d'urgence et un suivi bien-être.

ÉTAPE 4 - RÉSEAU D'EXPERTS & INSTITUTIONS (Étape finale et ultime recours) :
- Si la patiente confirme vouloir porter plainte, demande une protection officielle ou est en danger extrême :
- Donne-lui le Numéro Vert Action Sociale (80 00 12 12) et les contacts officiels (Police 17 / Gendarmerie 16 / Femmes Juristes +226 25 36 12 12).

POSTURE CLINIQUE ET STYLE :
- Dialogue fluide, empathique et naturel pas-à-pas (comme un vrai psychologue en consultation).
- Français très simple, chaleureux, protecteur et accessible au monde rural.
- Phrases courtes et concises, idéales pour la synthèse vocale (TTS).
- Ne génère JAMAIS de texte d'analyse interne ou de balise `<think>`.
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
