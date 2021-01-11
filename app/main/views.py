from flask import Blueprint, render_template, current_app

bp_main = Blueprint('main', __name__, template_folder='templates')


@bp_main.route('/')
def index():
    return render_template('index.html')


@current_app.template_filter('date_format')
def date_format(value, format='%m/%d/%Y'):
    return value.strftime(format)
