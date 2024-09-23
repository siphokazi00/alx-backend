#!/usr/bin/env python3
"""
Updated 0-app.py
"""
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """Config class for Babel and available languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# Set the app configuration from the Config class
app.config.from_object(Config)

# Instantiate Babel object
babel = Babel(app)


@app.route('/')
def index():
    """Renders the index page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
