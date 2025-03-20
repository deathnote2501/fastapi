import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

# Récupération de la clé API OpenAI depuis les variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_WAuvdaU7XJ5cUdh0J2U6oeOh"

# Vérification que la clé API est bien définie
if not OPENAI_API_KEY:
    raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")

print(f"✅ Clé API chargée avec succès : {openai_key[:5]}*****")

# Initialisation du client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialisation de FastAPI
app = FastAPI()

# Modèle de requête
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask_assistant/")
async def ask_assistant(request: PromptRequest):
    try:
        # Étape 1 : Créer un thread
        thread = client.beta.threads.create()

        # Étape 2 : Ajouter un message utilisateur au thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=request.prompt
        )

        # Étape 3 : Exécuter l'assistant sur le thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Attente de la réponse
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status in ["completed", "failed"]:
                break
            time.sleep(2)  # Pause pour éviter de surcharger l'API

        # Vérification si l'assistant a répondu
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = next(
            (msg.content for msg in messages.data if msg.role == "assistant"), None
        )

        if assistant_response:
            return {"response": assistant_response[0].text.value}
        else:
            raise HTTPException(status_code=500, detail="L'assistant n'a pas généré de réponse.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
