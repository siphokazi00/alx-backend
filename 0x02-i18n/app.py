#!/usr/bin/env python3
""" DIsplays current time in home page """
from flask import Flask, render_template, g, request
from flask_babel import Babel, format_datetime
from datetime import datetime
import pytz

app = Flask(__name__)
babel = Babel(app)


class Config:
    """ Configures languages to eng and fr """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """ Returns request in local language """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    if g.user:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """REturns local timezone """
    tz = request.args.get('timezone')
    if tz:
        try:
            return pytz.timezone(tz)
        except pytz.UnknownTimeZoneError:
            pass
    if g.user and g.user['timezone']:
        try:
            return pytz.timezone(g.user['timezone'])
        except pytz.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request():
    """ Determines user login """
    login_as = request.args.get('login_as')
    if login_as:
        g.user = users.get(int(login_as))
    else:
        g.user = None


@app.route('/')
def index():
    """ Render_template index """
    user_timezone = get_timezone()
    current_time = datetime.now(user_timezone)
    return render_template('index.html', current_time=current_time)


if __name__ == "__main__":
    app.run()
