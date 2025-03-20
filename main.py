import os
import openai
from fastapi import FastAPI, Request

# On récupère la clé depuis la variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/ask-gpt")
async def ask_gpt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return {"assistant_response": response["choices"][0]["message"]["content"]}
