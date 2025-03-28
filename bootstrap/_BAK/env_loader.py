# bootstrap/env_loader.py

from dotenv import load_dotenv
import os

def load_environment(dotenv_path=None):
    load_dotenv(dotenv_path)
    print(f"Environment loaded. APP_MODE = {os.getenv('APP_MODE')}")
