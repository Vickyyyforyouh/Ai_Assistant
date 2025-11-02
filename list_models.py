import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('OPENROUTER_API_KEY')
print(f"API Key: {api_key}")

# OpenRouter configuration
API_URL = "https://openrouter.ai/api/v1/models"
API_HEADERS = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

print(f"Sending request to: {API_URL}")
print(f"Headers: {API_HEADERS}")

# Make request
response = requests.get(
    API_URL,
    headers=API_HEADERS
)

print(f"Response status: {response.status_code}")
if response.status_code == 200:
    response_data = response.json()
    print(f"Available models: {len(response_data.get('data', []))}")
    # Print free models
    free_models = [model for model in response_data.get('data', []) if model.get('pricing', {}).get('completion', '') == '0' and model.get('pricing', {}).get('prompt', '') == '0']
    print(f"Free models: {len(free_models)}")
    for model in free_models[:10]:  # Print first 10 free models
        print(f"  - {model['id']}")
else:
    print(f"Response text: {response.text}")