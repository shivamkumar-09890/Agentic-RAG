import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(dotenv_path='.env')

def get_grok_response(
    prompt: str,
    model: str = None,
    temperature: float = None,
    max_tokens: int = None
) -> dict:
    """
    Send a prompt to the Grok chatbot and retrieve its response.
    
    Args:
        prompt (str): User input or question for Grok.
        model (str, optional): Grok model name (if configurable, else default to Grok's standard model).
        temperature (float, optional): Sampling temperature for response generation.
        max_tokens (int, optional): Maximum tokens in the response.
    
    Returns:
        dict: The response from the Grok API.
    """
    # Use environment variables with fallback values
    api_key = os.getenv('GROK_API_KEY')
    base_url = os.getenv('GROK_API_URL', 'https://api.x.ai/v1/chat')  # Example API endpoint
    
    # Fallback default values
    model = model or os.getenv('DEFAULT_MODEL', 'grok-1')
    temperature = temperature or float(os.getenv('WORKFLOW_TEMPERATURE', 0.3))
    max_tokens = max_tokens or int(os.getenv('WORKFLOW_MAX_TOKENS', 1000))
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(base_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# # Example Usage
# if __name__ == "__main__":
#     try:
#         response = get_grok_response(prompt="What is the future of AI?")
#         print("Grok's Response:", response)
#     except Exception as e:
#         print("Error:", e)
