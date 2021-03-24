import os
import re

from flask import Flask
from flask_migrate import Migrate

from app.extentions import init_extensions, db

app_env = os.environ.get('FLASK_ENV')


def create_app(config_env=app_env):
    app = Flask(__name__)

    if not config_env:
        config_env = 'development'

    app.config.from_object(f'config.{config_env.capitalize()}Config')

    init_extensions(app)

    lang_list = ','.join(app.config['LANGUAGES'])
    lang_prefix = f'<any({lang_list}):lang>'

    from app.main.views import root
    app.add_url_rule('/', view_func=root)

    with app.app_context():
        from app.album.views import bp_album
        app.register_blueprint(bp_album, url_prefix=f'/{lang_prefix}/albums')

    from app.main.views import bp_main
    app.register_blueprint(bp_main, url_prefix=f'/{lang_prefix}/')

    from app.tour.views import bp_tour
    app.register_blueprint(bp_tour, url_prefix=f'/{lang_prefix}/tours')

    from app.auth.views import bp_auth
    app.register_blueprint(bp_auth, url_prefix=f'/{lang_prefix}/auth')

    from app.admin.views import bp_admin
    app.register_blueprint(bp_admin, url_prefix=f'/{lang_prefix}/admin')

    from app.errors import forbidden
    app.register_error_handler(403, forbidden)

    from app.errors import page_not_found
    app.register_error_handler(404, page_not_found)

    from app.errors import internal_server_error
    app.register_error_handler(500, internal_server_error)

    from app.filters import date_format
    app.add_template_filter(date_format)

    from app.url_processors import bp_url_processors
    app.register_blueprint(bp_url_processors)

    app.config['ADMIN_VIEWS'] = [re.search('admin.(.*)_table', view).group(1) for view in
                                 list(app.view_functions.keys()) if
                                 re.search('admin.(.*)_table', view)]

    Migrate(app, db)

    from cli import register_click_commands
    register_click_commands(app)

    return app
