#!/usr/bin/env python3
""" Updated 0-app.py """
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config:
    """ Configures languages to Eng and Fr """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ Checks if 'locale' is in the URL query parameters """
    locale = request.args.get('locale')
    # If it's a supported locale, use it; otherwise, use the default method
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ Returns render template """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
