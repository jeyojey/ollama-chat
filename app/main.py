from flask import Flask, request, jsonify, render_template, Response
import requests
import json
import time
from config import Config

app = Flask(__name__)

def get_local_models():
    try:
        response = requests.get(Config.OLLAMA_LIST_ENDPOINT)
        models = response.json().get('models', [])
        
        model_dict = {}
        for model in models:
            model_name = model.get('name', '').split(':')[0]
            
            # Get known model info or use defaults
            model_info = Config.KNOWN_MODELS.get(model_name, {
                "params": "Unknown",
                "description": f"Local model: {model_name}",
                "creator": "Unknown"
            })
            
            model_dict[model_name] = {
                "name": model_name,
                **model_info,
                "size": model.get('size', 'Unknown'),
                "modified_at": model.get('modified_at', ''),
                "digest": model.get('digest', '')[:8]
            }
            
        return model_dict
    except Exception as e:
        print(f"Error fetching local models: {e}")
        return {}

# ... rest of your existing main.py code ... 