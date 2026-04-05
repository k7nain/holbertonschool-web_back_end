#!/usr/bin/env python3
""" 6-app.py: Flask app with Babel and priority-based locale selection """

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Config class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

# Saxta istifadəçi bazası (Mock database)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if ID cannot be found"""
    login_id = request.args.get('login_as')
    if login_id:
        try:
            return users.get(int(login_id))
        except ValueError:
            return None
    return None


@app.before_request
def before_request():
    """Find a user and set it as a global on flask.g.user"""
    g.user = get_user()


def get_locale():
    """Select the best match language based on priority:
    1. URL parameters
    2. User settings
    3. Request header
    4. Default locale
    """
    # 1. Locale from URL parameters
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    # 2. Locale from user settings
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    # 3. Locale from request header
    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    if best_match:
        return best_match

    # 4. Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


# Yeni versiya Babel inisializasiyası (localeselector parametri ilə)
babel = Babel(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def index():
    """Home page"""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
