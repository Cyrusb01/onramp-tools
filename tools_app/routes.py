"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/home')
def home():
    """Landing page."""
    return "Hello World"

@app.route('/markets')
def markets():
    return render_template("markets.html")

@app.route('/heat')
def heat():
    return render_template("cryptoheat.html")
    