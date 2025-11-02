import requests
import json

# Test the chat endpoint
response = requests.post(
    'http://localhost:5000/chat',
    json={"message": "Hello, how are you?"},
    headers={"Content-Type": "application/json"}
)

print(f"Status Code: {response.status_code}")
print("Response:", json.dumps(response.json(), indent=2))
