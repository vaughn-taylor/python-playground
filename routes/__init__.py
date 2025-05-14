# src/routes/__init__.py

from flask import Flask
from .finance_chat import finance_chat_bp

def register_routes(app: Flask) -> None:
    """Register all route blueprints here."""
    app.register_blueprint(finance_chat_bp)

    # Future route imports and registrations can go here
    # from .dashboard import dashboard_bp
    # app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
