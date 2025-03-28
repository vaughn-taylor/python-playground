from flask import Blueprint, render_template

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")

@logs_bp.route("/")
def logs_home():
    return "<h2>🗂️ Log Routes: Coming soon...</h2>"