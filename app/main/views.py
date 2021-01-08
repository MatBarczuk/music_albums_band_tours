from flask import Blueprint, render_template

bp_main = Blueprint('main', __name__, template_folder='templates')


@bp_main.route('/')
def index():
    return render_template('index.html')
