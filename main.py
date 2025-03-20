from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

# Récupération de la clé API depuis les variables d'environnement
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_yGoQaopQ2OBb1g00DfmZNAQv"

# Vérification que la clé API est bien définie
if not OPENAI_API_KEY:
    raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")

# Initialisation de FastAPI
app = FastAPI()

# Définition du modèle de requête
class PromptRequest(BaseModel):
    prompt: str

@app.post("/ask_assistant/")
async def ask_assistant(request: PromptRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": request.prompt}],
            assistant_id=ASSISTANT_ID
        )
        return {"response": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
