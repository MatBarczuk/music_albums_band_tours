from flask import Blueprint, g, current_app, request, after_this_request

bp_url_processors = Blueprint('url_processors', __name__)


@bp_url_processors.before_app_request
def before_request():
    if request.endpoint is 'static':
        return

    if request.cookies.get('lang') != g.lang:
        @after_this_request
        def set_cookie(response):
            response.set_cookie('lang', g.lang, max_age=60*60*24*100)
            return response


@bp_url_processors.app_url_value_preprocessor
def pull_lang_code(endpoint, values):
    try:
        if endpoint is 'static':
            return
        g.lang = values.pop('lang')
    except Exception:
        if request.cookies.get('lang') and request.cookies.get('lang') in current_app.config['LANGUAGES']:
            g.lang = request.cookies.get('lang')
        else:
            g.lang = current_app.config['LANGUAGES'][0]


@bp_url_processors.app_url_defaults
def add_language_code(endpoint, values):
    if 'lang' in values:
        return

    if current_app.url_map.is_endpoint_expecting(endpoint, 'lang'):
        values['lang'] = g.lang
