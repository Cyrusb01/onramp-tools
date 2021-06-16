"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/home')
def home():
    """Landing page."""
    return "Hello World"

@app.route('/markets')
def markets():
    """Landing page."""
    return render_template("markets.html")
    