from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

bp_main = Blueprint('main', __name__, template_folder='templates')


def root():
    return redirect(url_for('main.index'))


@bp_main.route('/')
def index():
    return render_template('index.html')
