import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('OPENROUTER_API_KEY')
print(f"API Key: {api_key}")

# OpenRouter configuration
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "AI Assistant",
    "Content-Type": "application/json"
}

# Test payload with a simple user message only
payload = {
    "model": "mistralai/mistral-7b-instruct:free",
    "messages": [
        {"role": "user", "content": "Hello, how are you? Reply in one sentence."}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

print(f"Sending request to: {API_URL}")
print(f"Headers: {API_HEADERS}")
print(f"Payload: {payload}")

# Make request
response = requests.post(
    API_URL,
    headers=API_HEADERS,
    json=payload
)

print(f"Response status: {response.status_code}")
print(f"Response text: {response.text}")

# Parse response
if response.status_code == 200:
    response_data = response.json()
    if "choices" in response_data and len(response_data["choices"]) > 0:
        ai_response = response_data["choices"][0]["message"]["content"].strip()
        print(f"AI Response: '{ai_response}'")
    else:
        print("No choices in response")
else:
    print("Request failed")