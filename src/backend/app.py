import os
from flask import Flask, send_from_directory
from src.backend.context_processors import inject_now
from src.backend.routes import register_routes
from src.backend.utils.assets import get_asset_path

def create_app():
    app = Flask(
        __name__,
        static_folder="../../static",  # where Vite builds to
        template_folder="templates"
    )

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}

    app.context_processor(inject_now)

    @app.context_processor
    def inject_asset_path():
        return {'get_asset_path': get_asset_path}

    # ✅ Serve uploaded assets from /assets/
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(os.path.join(app.root_path, '..', '..', 'assets'), filename)

    register_routes(app)

    return app
