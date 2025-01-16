import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv(dotenv_path='.env')

def get_openai_llm(
    model: str = None, 
    temperature: float = None, 
    max_tokens: int = None
) -> ChatOpenAI:
    """
    Create and return an OpenAI Language Model
    
    Args:
        model (str, optional): OpenAI model name
        temperature (float, optional): Sampling temperature
        max_tokens (int, optional): Maximum number of tokens to generate
    
    Returns:
        ChatOpenAI: Configured OpenAI Language Model
    """
    # Use environment variables with fallback values
    model = model or os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
    temperature = temperature or float(os.getenv('WORKFLOW_TEMPERATURE', 0.3))
    max_tokens = max_tokens or int(os.getenv('WORKFLOW_MAX_TOKENS', 1000))
    
    return ChatOpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        model=model, 
        temperature=temperature, 
        max_tokens=max_tokens
    )
