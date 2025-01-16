import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load environment variables
load_dotenv(dotenv_path='.env')

def get_huggingface_model(
    model_name: str = None,
    temperature: float = None,
    max_tokens: int = None
):
    """
    Create and return a Hugging Face language model pipeline.
    
    Args:
        model_name (str, optional): Hugging Face model name (e.g., 'gpt2').
        temperature (float, optional): Sampling temperature for the model.
        max_tokens (int, optional): Maximum tokens for the output.
    
    Returns:
        pipeline: A text generation pipeline from Hugging Face Transformers.
    """
    # Use environment variables with fallback values
    model_name = model_name or os.getenv('HF_MODEL_NAME', 'gpt2')
    temperature = temperature or float(os.getenv('WORKFLOW_TEMPERATURE', 0.7))
    max_tokens = max_tokens or int(os.getenv('WORKFLOW_MAX_TOKENS', 50))

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Set up pipeline
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        framework="pt",  # Use PyTorch (default) or "tf" for TensorFlow
    )

    return generator, temperature, max_tokens

def generate_text(prompt: str):
    """
    Generate text using a Hugging Face model.
    
    Args:
        prompt (str): The input text for the model.
    
    Returns:
        str: The generated text.
    """
    generator, temperature, max_tokens = get_huggingface_model()
    output = generator(
        prompt,
        max_length=max_tokens,
        temperature=temperature,
        num_return_sequences=1
    )
    return output[0]["generated_text"]

# # Example Usage
# if __name__ == "__main__":
#     try:
#         result = generate_text(prompt="What is the future of artificial intelligence?")
#         print("Hugging Face Model Response:", result)
#     except Exception as e:
#         print("Error:", e)
