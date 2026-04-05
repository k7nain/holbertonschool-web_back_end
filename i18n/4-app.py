#!/usr/bin/env python3
"""
Flask i18n app
"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """
    Config class for Babel
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'


app = Flask(__name__)
app.config.from_object(Config)


def get_locale():
    """
    Get locale from URL parameter if present,
    otherwise use the best match from headers
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)


@app.route('/')
def main_page():
    """
    Main page of the app
    """
    return render_template('4-index.html'), 200


if __name__ == '__main__':
    app.run()
