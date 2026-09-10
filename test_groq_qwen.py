import asyncio
from app.services.ai_service import ai_service

async def main():
    print("Testing Groq Qwen integration for LAFIYA...")
    advice = await ai_service.get_pregnancy_and_health_advice(week_number=16, user_query="Quels sont les bilans à faire ?")
    print("\n--- Groq Qwen Pregnancy Advice Response ---")
    print(advice)
    
    threat = await ai_service.analyze_threat("Une personne me menace et j'ai très peur")
    print("\n--- Groq Qwen Threat Analysis Response ---")
    print(threat)

if __name__ == "__main__":
    asyncio.run(main())
