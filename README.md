# Ollama Web Chat

A web-based chat interface for Ollama models with real-time response streaming and performance metrics.

## Features

- 🚀 Real-time response streaming
- 📊 Performance metrics (tokens/sec, generation time)
- 💻 GPU utilization support
- 🔄 Automatic model detection
- 📱 Responsive design
- ⚡ Live token counting

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- NVIDIA GPU (optional, for GPU acceleration)
- CUDA toolkit (optional, for GPU acceleration)

## Installation

1. Install Ollama
```bash
# For Linux/WSL
curl -fsSL https://ollama.com/install.sh | sh

# For MacOS
brew install ollama
```

2. Clone the repository
```bash
git clone https://github.com/yourusername/ollama-chat.git
cd ollama-chat
```

3. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install requirements
```bash
pip install -r requirements.txt
```

5. Pull some Ollama models
```bash
ollama pull phi
ollama pull neural-chat
ollama pull mistral
# Add any other models you want
```

## Usage

1. Start Ollama server
```bash
ollama serve
```

2. Run the Flask application
```bash
python app/main.py
```

3. Open your browser and navigate to `http://localhost:5000`

## GPU Support

To enable GPU acceleration:

1. Install NVIDIA drivers and CUDA toolkit
2. Pull models with GPU support:
```bash
ollama pull phi --gpu
```

3. Monitor GPU usage:
```bash
nvidia-smi -l 1
```

## Configuration

The application can be configured through environment variables:

- `OLLAMA_HOST`: Ollama API host (default: http://localhost:11434)
- `FLASK_ENV`: Development environment (development/production)
- `PORT`: Application port (default: 5000)

Create a `.env` file in the root directory:
```env
OLLAMA_HOST=http://localhost:11434
FLASK_ENV=development
PORT=5000
```

## Performance Tips

1. Use GPU acceleration when possible
2. Keep models loaded in memory
3. Use appropriate context lengths
4. Monitor system resources

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ollama team for their amazing work
- Flask framework
- All contributors 