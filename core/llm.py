import json
import requests
from openai import OpenAI
from config import USE_OLLAMA, OPENAI_MODEL, OLLAMA_MODEL

client = OpenAI()

SYSTEM = """
Sei un consulente del lavoro senior.
Output SOLO JSON valido.
Niente testo libero.
"""

def call_llm(prompt):

    if USE_OLLAMA:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": SYSTEM + "\n\n" + prompt,
                "stream": False
            }
        )
        return r.json()["response"]

    else:
        res = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return res.choices[0].message.content
