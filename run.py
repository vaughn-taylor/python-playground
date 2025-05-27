# run.py
import os
import sys
from dotenv import load_dotenv

# 🔧 Force unbuffered, real-time output
os.environ["PYTHONUNBUFFERED"] = "1"
sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)

load_dotenv()

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
