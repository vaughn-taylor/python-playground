# src/backend/routes/__init__.py
from .logs import logs_bp
from .dashboard import dashboard_bp
from .chat import chat_bp

def register_routes(app):
    app.register_blueprint(dashboard_bp)         # handles "/"
    app.register_blueprint(logs_bp, url_prefix="/logs")  # handles "/logs"
    app.register_blueprint(chat_bp)
