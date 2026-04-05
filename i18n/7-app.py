#!/usr/bin/env python3
""" 7-app.py: Flask app with Babel, locale and timezone selection """

import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """Config class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

# Saxta istifadəçi bazası
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
    """Select the best match language based on priority"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    best_match = request.accept_languages.best_match(app.config['LANGUAGES'])
    if best_match:
        return best_match

    return app.config['BABEL_DEFAULT_LOCALE']


def get_timezone():
    """Select and validate appropriate timezone based on priority:
    1. URL parameters
    2. User settings
    3. Default to UTC
    """
    # 1. URL-dən saat qurşağını yoxlayırıq
    tz_url = request.args.get('timezone')
    if tz_url:
        try:
            pytz.timezone(tz_url)  # Doğruluğunu test edirik
            return tz_url
        except pytz.exceptions.UnknownTimeZoneError:
            pass  # Xətalıdırsa, növbəti mərhələyə keçir

    # 2. İstifadəçi parametrlərindən yoxlayırıq
    if g.user and g.user.get('timezone'):
        tz_user = g.user.get('timezone')
        try:
            pytz.timezone(tz_user)  # Doğruluğunu test edirik
            return tz_user
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # 3. Heç biri uyğun gəlməsə, Default (UTC) qaytarırıq
    return app.config['BABEL_DEFAULT_TIMEZONE']
