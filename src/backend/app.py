from flask import Flask
from src.backend.context_processors import inject_now
from src.backend.routes import register_routes
from src.backend.utils.assets import get_asset_path  # 👈 import this

def create_app():
    app = Flask(
        __name__,
        static_folder="../../static",
        template_folder="templates"
    )

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.jinja_env.cache = {}

    # ⬇️ inject global template context
    app.context_processor(inject_now)

    @app.context_processor
    def inject_asset_path():
        return {'get_asset_path': get_asset_path}

    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5050)
