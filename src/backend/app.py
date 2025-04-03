import os
from flask import Flask, send_from_directory, request
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

    # ✅ Inject custom context processors
    app.context_processor(inject_now)

    @app.context_processor
    def inject_asset_path():
        return {'get_asset_path': get_asset_path}

    @app.context_processor
    def inject_nav_helpers():
        def is_active_prefix(prefix):
            return request.path.startswith(prefix)

        def nav_link_class(
            path_prefix,
            base_classes='text-gray-700 hover:text-indigo-500',
            active_classes='text-indigo-600 underline'
        ):
            if path_prefix == '/':
                is_active = request.path == '/'
            else:
                is_active = request.path.startswith(path_prefix)
            return f"{base_classes} {active_classes}" if is_active else base_classes

        return {
            'is_active_prefix': is_active_prefix,
            'nav_link_class': nav_link_class
        }

    # ✅ Serve uploaded assets from /assets/
    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(os.path.join(app.root_path, '..', '..', 'assets'), filename)

    # Register your modular routes
    register_routes(app)

    return app
