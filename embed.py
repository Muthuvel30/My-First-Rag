import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_embeed(text):
    api_key=os.environ.get("GEMINI_API_KEY")
    url="https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent"
    response = requests.post(
        url,
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        json={
            "model": "models/text-embedding-004",
            "content": {"parts": [{"text": text}]}
        }
    )
    data = response.json()
    # print(data)
    return data["embedding"]["values"]

if __name__ == "__main__":
    vec = get_embeed("Muthuvel was born on March 5th, 2002.")
    print("Length of vector:", len(vec))
    print("First 5 numbers:", vec[:5])
