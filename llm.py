import os
import requests
from dotenv import load_dotenv

load_dotenv()

def ask_llm(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    response = requests.post(
        url,
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

