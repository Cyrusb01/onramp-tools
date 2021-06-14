"""Initialize Flask app."""
from flask import Flask


def init_app():
    """Construct core Flask with embedded Dash application."""
    app = Flask(__name__)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        from .plotlydash.index import init_dashboard
        app = init_dashboard(app)

        return app