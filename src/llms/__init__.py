from typing import Union
from langchain_core.language_models import BaseChatModel
from .openai_api import get_openai_llm
from .huggingface_api import get_huggingface_model

def get_llm(llm_type="hugging_face_api"):
    if llm_type == "openai_api":
        return get_openai_llm()
    elif llm_type == "hugging_face_api":
        return get_huggingface_model()
    elif llm_type == "gemini":
        return get_gemini_model()
    else:
        raise ValueError(f"Unsupported LLM type: {llm_type}")

def __init__(self, llm_type: str = 'openai'):
    return get_llm(llm_type)
