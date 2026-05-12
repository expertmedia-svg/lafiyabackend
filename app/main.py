from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.v1 import auth, emergency, ai, vault, chat, legal, emotions, cycle
from app.db.base import Base
from app.db.session import engine

PRIVACY_POLICY_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Politique de confidentialite - Lafiya</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            background: #fff8fb;
            color: #2d2134;
        }
        main {
            max-width: 860px;
            margin: 0 auto;
            padding: 40px 20px 64px;
        }
        h1, h2 {
            color: #7c2d6b;
        }
        section {
            margin-bottom: 28px;
            background: #ffffff;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 8px 24px rgba(124, 45, 107, 0.08);
        }
        a {
            color: #9c2f7c;
        }
    </style>
</head>
<body>
    <main>
        <h1>Politique de confidentialite de Lafiya</h1>
        <p>Derniere mise a jour : 12 mai 2026</p>

        <section>
            <h2>1. Objet</h2>
            <p>Lafiya est une application d'accompagnement, d'information et de soutien qui peut proposer des fonctions de journal, de coffre de preuves, de rappels et d'assistance conversationnelle. Cette politique explique quelles donnees peuvent etre traitees et dans quel but.</p>
        </section>

        <section>
            <h2>2. Donnees traitees</h2>
            <p>Selon les fonctions utilisees, Lafiya peut traiter les categories de donnees suivantes :</p>
            <p>- donnees de compte technique generees pour l'authentification a l'API ;</p>
            <p>- contenus saisis par l'utilisatrice dans le chat d'assistance ;</p>
            <p>- informations de suivi saisies dans le journal ou le suivi de cycle ;</p>
            <p>- fichiers importes ou captures par l'utilisatrice, comme des images ou documents envoyes au coffre ;</p>
            <p>- donnees conservees localement sur l'appareil pour le fonctionnement de l'application.</p>
        </section>

        <section>
            <h2>3. Permissions de l'appareil</h2>
            <p>Lafiya peut demander l'acces a la camera pour capturer une preuve, a la galerie/photos pour selectionner une image, et aux notifications pour afficher des rappels. Ces acces sont utilises uniquement pour les fonctions choisies par l'utilisatrice.</p>
        </section>

        <section>
            <h2>4. Finalites</h2>
            <p>Les donnees sont utilisees pour fournir les fonctionnalites de l'application, notamment :</p>
            <p>- permettre l'acces securise a certains services backend ;</p>
            <p>- enregistrer ou synchroniser des informations de journal et de suivi ;</p>
            <p>- transmettre des messages au service d'assistance conversationnelle ;</p>
            <p>- envoyer des fichiers au service de coffre lorsque l'utilisatrice le demande ;</p>
            <p>- stocker localement des informations utiles au fonctionnement de l'application.</p>
        </section>

        <section>
            <h2>5. Stockage et securite</h2>
            <p>Une partie des donnees peut etre stockee localement sur l'appareil via des mecanismes de stockage securise. Lorsque des donnees sont envoyees au serveur Lafiya, elles transitent via HTTPS. Aucune methode de transmission ou de stockage n'offre une securite absolue, mais des mesures raisonnables sont prises pour proteger les donnees.</p>
        </section>

        <section>
            <h2>6. Partage</h2>
            <p>Lafiya ne revend pas les donnees personnelles. Certaines donnees peuvent etre traitees par les services techniques necessaires au fonctionnement de l'application et de son infrastructure.</p>
        </section>

        <section>
            <h2>7. Choix de l'utilisatrice</h2>
            <p>L'utilisatrice peut limiter certaines permissions depuis les reglages de son appareil et choisir de ne pas utiliser certaines fonctions necessitant un envoi de donnees ou de fichiers.</p>
        </section>

        <section>
            <h2>8. Contact</h2>
            <p>Pour toute question relative a cette politique, vous pouvez contacter l'equipe Lafiya a l'adresse suivante : <a href="mailto:contact@lafiya.app">contact@lafiya.app</a>.</p>
        </section>
    </main>
</body>
</html>
"""

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


@app.get("/privacy-policy", response_class=HTMLResponse, tags=["public"])
def privacy_policy():
    return PRIVACY_POLICY_HTML


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
