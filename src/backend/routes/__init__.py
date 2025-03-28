from .logs import logs_bp

def register_routes(app):
    app.register_blueprint(logs_bp)
