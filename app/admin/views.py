from functools import wraps

from flask import Blueprint, render_template, url_for, flash
from flask.views import View, MethodView
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from flask_babel import _

from app.extentions import db
from app.album.forms import UpdateAlbumForm
from app.album.models import Album
from app.auth.models import User
from app.tour.forms import UpdateTourForm
from app.tour.models import Tour

bp_admin = Blueprint('admin', __name__, template_folder='templates')


def admin_required(fn):
    @wraps(fn)
    def _admin_required(*args, **kwargs):
        if not current_user.is_admin:
            flash(_('You need to be an administrator to access this page.'), 'danger')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)

    return _admin_required


class TableView(View):
    decorators = [admin_required, login_required]

    def __init__(self, model, edit_allowed=False):
        self.model = model
        self.columns = self.model.__mapper__.columns.keys()
        self.resource_name = self.model.__name__.lower()
        self.edit_allowed = edit_allowed
        super(TableView, self).__init__()

    def dispatch_request(self):
        return render_template('resource_table.html', columns=self.columns, instances=self.model.query.all(),
                               edit_allowed=self.edit_allowed, resource_name=self.resource_name)


class ModifyResourceView(MethodView):
    decorators = [admin_required, login_required]

    def __init__(self, model, edit_form):
        self.model = model
        self.edit_form = edit_form
        self.columns = self.model.__mapper__.columns.keys()
        self.resource_name = self.model.__name__.lower()
        self.form = edit_form()
        super(MethodView, self).__init__()

    def get(self, resource_id):
        form = self.form
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instance(resource_id)

        for parameter in parameters:
            form_attr = getattr(form, parameter)
            form_attr.data = getattr(model_instance, parameter)

        return render_template('resource_edit.html', resource_name=self.resource_name, model_instance=model_instance,
                               form=form, parameters=parameters)

    def post(self, resource_id):
        form = self.form
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instance(resource_id)
        if form.validate_on_submit():
            for parameter in parameters:
                form_attr = getattr(form, parameter).data
                setattr(model_instance, parameter, form_attr)
            db.session.add(model_instance)
            db.session.commit()
            return redirect(url_for(f"admin.{self.resource_name}_table"))

        for parameter in parameters:
            form_attr = getattr(form, parameter)
            form_attr.data = getattr(model_instance, parameter)

        return render_template('resource_edit.html', resource_name=self.resource_name, model_instance=model_instance,
                               form=form, parameters=parameters)

    def delete(self, resource_id):
        model_instance = self.get_model_instance(resource_id)
        db.session.delete(model_instance)
        db.session.commit()
        return ""

    def get_model_instance(self, resource_id):
        return self.model.query.filter_by(id=resource_id).first()

    @staticmethod
    def get_update_parameters(form_instance):
        parameter_list = list(form_instance.__dict__.keys())
        parameter_list = [parameter for parameter in parameter_list if
                          parameter[0] != '_' and parameter not in ['submit', 'csrf_token', 'meta']]
        return parameter_list


def register_admin_resource(model, edit_form=None):
    resource_name = model.__name__.lower()
    view_func = ModifyResourceView.as_view(resource_name, model=model, edit_form=edit_form)
    edit_allowed = True
    view_methods = ['GET', 'POST', 'DELETE']

    if edit_form is None:
        edit_allowed = False
        view_methods = ['DELETE']

    bp_admin.add_url_rule(f'/{resource_name}/',
                          view_func=TableView.as_view(f'{resource_name}_table', model=model, edit_allowed=edit_allowed))
    bp_admin.add_url_rule(f'/{resource_name}/<int:resource_id>', view_func=view_func, methods=view_methods)


register_admin_resource(Album, UpdateAlbumForm)
register_admin_resource(Tour, UpdateTourForm)
register_admin_resource(User)
