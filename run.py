# run.py
import os
from src.backend.app import create_app

MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3")
OLLAMA_URL = "http://localhost:11434/api/generate"

app = create_app()

# 🚀 Start Flask
app.run(debug=True, port=5050)
