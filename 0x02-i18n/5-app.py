#!/usr/bin/env python3
""" Updated 0-app.py """
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Configures languages to Eng and Fr """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel.init_app(app)


def get_user():
    """Returns a user dictionary if ID exists, else None."""
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """Set the logged-in user to g.user before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user.get("locale")
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])
