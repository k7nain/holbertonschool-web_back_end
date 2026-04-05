#!/usr/bin/env python3
from flask import Flask, render_template, request, g
from flask_babel import Babel, _

# -------------------------
# Mock user table
# -------------------------
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# -------------------------
# Flask app & Babel config
# -------------------------


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# -------------------------
# Helper functions
# -------------------------


def get_user():
    """Return user dict or None if login_as invalid or not provided"""
    try:
        user_id = int(request.args.get('login_as', 0))
        return users.get(user_id)
    except (ValueError, TypeError):
        return None


@app.before_request
def before_request():
    """Executed before every request to set g.user"""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Determine the best locale to use"""
    # 1️⃣ URL parameter has highest priority
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param

    # 2️⃣ User locale if valid
    if g.get('user'):
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # 3️⃣ Fallback to Accept-Language header or default
    return request.accept_languages.best_match(app.config['LANGUAGES']) or 'en'

# -------------------------
# Routes
# -------------------------


@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# Run server
# -------------------------


if __name__ == "__main__":
    app.run()
