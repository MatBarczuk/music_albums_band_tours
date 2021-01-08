from flask import Flask
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()


def create_app(config_env=''):
    app = Flask(__name__)

    if not config_env:
        config_env = app.env

    app.config.from_object(f'config.{config_env.capitalize()}Config')

    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _l('You need to be logged in to access this page.')
    login_manager.login_message_category = 'danger'

    Migrate(app, db)

    return app
