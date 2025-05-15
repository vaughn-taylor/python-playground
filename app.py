import os
from flask import Flask, send_from_directory, request
from datetime import datetime, timezone
from routes import register_routes
from utils.assets import get_asset_path
from routes.autocomplete import bp as autocomplete_bp

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/static"
    )

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}

    # 📅 Inject current UTC datetime into all templates
    @app.context_processor
    def inject_now():
        return {"now": datetime.now(timezone.utc)}

    # 🧩 Make get_asset_path available in Jinja templates
    app.jinja_env.globals["get_asset_path"] = get_asset_path

    # ✅ Serve Vite-compiled static assets (JS/CSS from /static/assets)
    @app.route("/static/assets/<path:filename>")
    def vite_static(filename):
        return send_from_directory(os.path.abspath("static/assets"), filename)

    # ✅ Serve user-uploaded or other assets from /assets
    @app.route("/assets/<path:filename>")
    def serve_uploaded_assets(filename):
        return send_from_directory(os.path.abspath("assets"), filename)

    # ✅ Nav helpers (e.g. active link detection)
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
            "is_active_prefix": is_active_prefix,
            "nav_link_class": nav_link_class,
        }
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )

    @app.route('/apple-touch-icon.png')
    def apple_touch_icon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'apple-touch-icon.png',
            mimetype='image/png'
        )


    # 🔁 Register routes
    register_routes(app)

    # ✅ Register autocomplete route
    app.register_blueprint(autocomplete_bp)

    return app
