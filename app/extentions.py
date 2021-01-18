from flask import g
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()


def init_extensions(app):
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _l('You need to be logged in to access this page.')
    login_manager.login_message_category = 'danger'


@babel.localeselector
def get_locale():
    return g.lang
