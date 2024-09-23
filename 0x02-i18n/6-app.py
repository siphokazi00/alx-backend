#!/usr/bin/env python3
""" Update to get_locale """


@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    # Check if 'locale' parameter is in the URL and is valid
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # If a user is logged in, use their preferred locale (if it's supported)
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user.get("locale")

    # Check the request headers for the best match
    return request.accept_languages.best_match(app.config['LANGUAGES'])
