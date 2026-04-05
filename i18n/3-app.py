#!/usr/bin/env python3
"""Flask app with Babel and translations"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Config class for Babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel()


def get_locale():
    """Select best language"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])



babel.init_app(app, locale_selector = get_locale)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
