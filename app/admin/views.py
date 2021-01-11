from functools import wraps

from flask import Blueprint, render_template, url_for, flash
from flask.views import View, MethodView
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from flask_babel import _

from app import db
from app.album.forms import UpdateAlbumForm
from app.album.models import Album
from app.auth.models import User
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


bp_admin.add_url_rule('/tours', view_func=TableView.as_view('tour', model=Tour))
bp_admin.add_url_rule('/users', view_func=TableView.as_view('user', model=User))


class ModifyResourceView(MethodView):
    decorators = [admin_required, login_required]

    def __init__(self, model, edit_form):
        self.model = model
        self.edit_form = edit_form
        self.columns = self.model.__mapper__.columns.keys()
        self.resource_name = self.model.__name__.lower()
        super(ModifyResourceView, self).__init__()

    def get(self, resource_id):
        form = self.edit_form()
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instence(resource_id)

        for parameter in parameters:
            form_attr = getattr(form, parameter)
            form_attr.data = getattr(model_instance, parameter)

        return render_template('resource_edit.html', resource_name=self.resource_name, model_instance=model_instance,
                               form=form, parameters=parameters)

    def post(self, resource_id):
        form = self.edit_form()
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instance(resource_id)
        if form.validate_on_submit():
            for parameter in parameters:
                form_attr = getattr(form, parameter).data
                setattr(model_instance, parameter, form_attr)
            db.session.add(model_instance)
            db.session.commit()
            return redirect(url_for(f"admin.{self.resource_name}_table"))
        return redirect(url_for(f"admin.{self.resource_name}", resource_id=model_instance.id))

    def delete(self, resource_id):
        model_instance = self.get_model_instance(resource_id)
        db.session.delete(model_instance)
        db.session.commit()
        return ""

    def get_model_instance(self, resource_id):
        return self.model.query.filter_by(id=resource_id).first()

    def get_update_parameters(self, form_instance):
        parameter_list = list(form_instance.__dict__.keys())
        parameter_list = [parameter for parameter in parameter_list if
                          parameter[0] != '_' and parameter not in ['submit', 'csrf_token', 'meta']]
        return parameter_list


bp_admin.add_url_rule('/albums', view_func=TableView.as_view('album', model=Album))
bp_admin.add_url_rule('/albums/<int:resource_id>',
                      view_func=ModifyResourceView.as_view('album_edit', model=Album, edit_form=UpdateAlbumForm))
