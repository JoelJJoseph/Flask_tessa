import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please check your .env file.")
        
        # Correct API URL with API key passed as a query parameter
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"

    def generate_response(self, prompt):
        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "prompt": {
                "text": prompt
            },
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            api_response = response.json()
            # Correctly parsing the Google Gemini response structure
            if "candidates" in api_response:
                return api_response["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return "No valid response from API."
        else:
            return f"Error: {response.status_code} - {response.text}"
