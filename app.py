from flask import Flask, request, jsonify, render_template, Response
import requests
import json
import time

app = Flask(__name__)

OLLAMA_ENDPOINT = "http://localhost:11434/api/chat"
OLLAMA_LIST_ENDPOINT = "http://localhost:11434/api/tags"

def get_local_models():
    try:
        response = requests.get(OLLAMA_LIST_ENDPOINT)
        models = response.json().get('models', [])
        
        # Create a dictionary of model information
        model_dict = {}
        for model in models:
            model_name = model.get('name', '').split(':')[0]  # Remove tag/version if present
            
            # Default model info structure
            model_dict[model_name] = {
                "name": model_name,
                "params": "Unknown",
                "description": f"Local model: {model_name}",
                "creator": "Unknown",
                "size": model.get('size', 'Unknown'),
                "modified_at": model.get('modified_at', ''),
                "digest": model.get('digest', '')[:8]  # First 8 chars of digest
            }
            
            # Add specific information for known models
            if model_name == "llama2":
                model_dict[model_name].update({
                    "params": "7B",
                    "description": "Meta's Llama 2 model, good for general-purpose tasks.",
                    "creator": "Meta"
                })
            elif model_name == "codellama":
                model_dict[model_name].update({
                    "params": "7B",
                    "description": "Specialized for code completion and programming tasks.",
                    "creator": "Meta"
                })
            elif model_name == "mistral":
                model_dict[model_name].update({
                    "params": "7B",
                    "description": "High-performance model with strong reasoning capabilities.",
                    "creator": "Mistral AI"
                })
            # Add more known models here...
            
        return model_dict
    except Exception as e:
        print(f"Error fetching local models: {e}")
        return {}

# Get local models on startup
AVAILABLE_MODELS = get_local_models()

@app.route('/')
def home():
    # Refresh available models on each home page load
    global AVAILABLE_MODELS
    AVAILABLE_MODELS = get_local_models()
    return render_template('index.html', models=AVAILABLE_MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    selected_model = data.get('model')
    
    if selected_model not in AVAILABLE_MODELS:
        return jsonify({'error': 'Invalid model selection'}), 400
    
    ollama_payload = {
        "model": selected_model,
        "messages": [
            {
                "role": "user",
                "content": user_message
            }
        ],
        "stream": True,
        "options": {
            "num_gpu": 99,
            "num_thread": 8,
            "mmap": True,
            "numa": True,
            "f16_kv": True,
            "gpu_layers": -1
        }
    }
    
    def generate():
        try:
            response = requests.post(OLLAMA_ENDPOINT, json=ollama_payload, stream=True)
            start_time = None
            first_token_time = None
            total_tokens = 0
            accumulated_response = ""
            last_token_time = None

            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line.decode('utf-8'))
                    
                    if 'message' in json_response:
                        current_time = time.time()
                        
                        # Initialize start time on first token
                        if start_time is None:
                            start_time = current_time
                            first_token_time = 0
                        
                        token = json_response['message'].get('content', '')
                        if token:  # Only count non-empty tokens
                            accumulated_response += token
                            total_tokens += 1
                            last_token_time = current_time
                            
                            # Calculate time since start
                            elapsed_time = current_time - start_time
                            
                            # Calculate tokens per second based on total time and tokens
                            tokens_per_second = total_tokens / elapsed_time if elapsed_time > 0 else 0

                            stats = {
                                'first_token_time': round(first_token_time, 2),
                                'tokens_per_second': round(tokens_per_second, 2),
                                'total_tokens': total_tokens,
                                'total_time': round(elapsed_time, 2),
                                'response': accumulated_response,
                                'gpu_enabled': True
                            }

                            yield f"data: {json.dumps(stats)}\n\n"

                    # Get context and timing information if available
                    if 'prompt_eval_count' in json_response:
                        prompt_tokens = json_response.get('prompt_eval_count', 0)
                        eval_tokens = json_response.get('eval_count', 0)
                        total_tokens = prompt_tokens + eval_tokens

                    if 'total_duration' in json_response:
                        total_duration = json_response['total_duration'] / 1e9  # Convert nanoseconds to seconds
                        if total_duration > 0:
                            final_tokens_per_second = total_tokens / total_duration
                            
                            stats = {
                                'first_token_time': round(first_token_time, 2),
                                'tokens_per_second': round(final_tokens_per_second, 2),
                                'total_tokens': total_tokens,
                                'total_time': round(total_duration, 2),
                                'response': accumulated_response,
                                'gpu_enabled': True,
                                'done': True
                            }
                            
                            yield f"data: {json.dumps(stats)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True) 