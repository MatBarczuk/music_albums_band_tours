from flask import Blueprint, url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from flask_babel import _
from werkzeug.utils import redirect

from app import db
from app.auth.forms import RegistrationForm, LoginForm
from app.auth.models import User

bp_auth = Blueprint('auth', __name__, template_folder='templates')


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(_('You are registered.'), 'success')

        login_user(user)

        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user, form.password.data, form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid email or password'), 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, form.remember_me.data)
        flash(_('Logged in.'), 'success')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@bp_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))
