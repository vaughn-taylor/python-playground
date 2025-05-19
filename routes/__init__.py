# src/routes/__init__.py

from flask import Flask
from .chat import bp as chat_bp
from .analyze import bp as analyze_bp
from .analyze_upload import bp as analyze_upload_bp  # ⬅️ NEW

def register_routes(app: Flask) -> None:
    """Register all route blueprints here."""
    app.register_blueprint(chat_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(analyze_upload_bp)  # ⬅️ REGISTERED HERE
