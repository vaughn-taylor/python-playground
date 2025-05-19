# src/routes/__init__.py

from flask import Flask
from .chat import bp as chat_bp
from .analyze import bp as analyze_bp  # ⬅️ stays the same

def register_routes(app: Flask) -> None:
    """Register all route blueprints here."""
    app.register_blueprint(chat_bp)
    app.register_blueprint(analyze_bp)  # ⬅️ removed url_prefix so /analyze works

    # Future route imports and registrations can go here
    # from .dashboard import dashboard_bp
    # app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
