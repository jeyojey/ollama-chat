import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    OLLAMA_CHAT_ENDPOINT = f"{OLLAMA_HOST}/api/chat"
    OLLAMA_LIST_ENDPOINT = f"{OLLAMA_HOST}/api/tags"
    
    # Model configurations
    DEFAULT_MODEL_CONFIG = {
        "num_gpu": 99,
        "num_thread": 8,
        "mmap": True,
        "numa": True,
        "f16_kv": True,
        "gpu_layers": -1,
        "gpu_memory_utilization": 0.9,
    }
    
    # Known model information
    KNOWN_MODELS = {
        "phi": {
            "params": "2.7B",
            "description": "Microsoft's compact yet powerful model.",
            "creator": "Microsoft"
        },
        "mistral": {
            "params": "7B",
            "description": "High-performance model with strong reasoning.",
            "creator": "Mistral AI"
        },
        # Add more models here
    } 