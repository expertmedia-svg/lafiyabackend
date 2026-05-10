from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, emergency, ai, vault, chat, legal, emotions, cycle
from app.db.base import Base
from app.db.session import engine

# Création des tables (en prod, utiliser Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(emergency.router, prefix=settings.API_V1_STR + "/security", tags=["security"])
app.include_router(ai.router, prefix=settings.API_V1_STR + "/ai", tags=["ai"])
app.include_router(vault.router, prefix=settings.API_V1_STR + "/vault", tags=["vault"])
app.include_router(chat.router, prefix=settings.API_V1_STR + "/chat", tags=["chat"])
app.include_router(legal.router, prefix=settings.API_V1_STR + "/legal", tags=["legal"])
app.include_router(emotions.router, prefix=settings.API_V1_STR + "/emotions", tags=["emotions"])
app.include_router(cycle.router, prefix=settings.API_V1_STR + "/cycle", tags=["cycle"])

@app.get("/")
def root():
    return {"message": "Welcome to LAFIYA API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
