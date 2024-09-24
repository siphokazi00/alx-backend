#!/usr/bin/env python3
""" Updated 0-app.py """
from flask import request, g
from flask_babel import Babel
import pytz
from pytz.exceptions import UnknownTimeZoneError

# Initialize Babel
babel = Babel(app)


@babel.timezoneselector
def get_timezone():
    """ 1. Check if the 'timezone' parameter is present in the URL """
    timezone = request.args.get('timezone')

    if timezone:
        try:
            # Validate the timezone from the URL
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            # If the timezone is invalid, fall through to other methods
            pass

    # 2. Check the user's preferred timezone (if logged in)
    if g.user and g.user.get('timezone'):
        try:
            # Validate the timezone from user settings
            return pytz.timezone(g.user['timezone']).zone
        except UnknownTimeZoneError:
            # If the user's timezone is invalid, fall through to the default
            pass

    # 3. Default to UTC if no valid timezone is found
    return 'UTC'
