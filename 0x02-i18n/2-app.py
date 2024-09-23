#!/usr/bin/env python3
"""
Get locale function
"""
from flask import Flask, request, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """
    Configures languages to English and French
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

# Instantiate Babel
babel = Babel(app)


# Define the get_locale function with the babel.localeselector decorator
@babel.localeselector
def get_locale():
    """ Uses the request accept_languages to determine the best match """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ Returns render template """
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
