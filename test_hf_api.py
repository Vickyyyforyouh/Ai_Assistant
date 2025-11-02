import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('HUGGINGFACE_API_KEY')
print(f"API Key: {api_key}")

# Initialize the client with a simpler model
client = InferenceClient(
    model="gpt2",
    token=api_key
)

# Test the API
try:
    prompt = "Hello, how are you?"
    response = client.text_generation(
        prompt,
        max_new_tokens=50,
        temperature=0.7
    )
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {str(e)}")