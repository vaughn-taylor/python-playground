# src/backend/routes/__init__.py
from .logs import logs_bp
from .dashboard import dashboard_bp
from .chat import chat_bp
from .rag_chat import rag_chat_bp  # ✅ NEW import

def register_routes(app):
    app.register_blueprint(dashboard_bp)                # handles "/"
    app.register_blueprint(logs_bp, url_prefix="/logs") # handles "/logs"
    app.register_blueprint(chat_bp)
    app.register_blueprint(rag_chat_bp)                 # ✅ NEW route
