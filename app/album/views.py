from flask import Blueprint, render_template, flash, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from flask_babel import _
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app.extentions import db
from app.album.forms import CreateAlbumForm, UpdateAlbumForm
from app.album.models import Album
from app.helpers.helpers import save_image_upload

bp_album = Blueprint('album', __name__, template_folder='templates')


@bp_album.route('/')
@login_required
def albums_list():
    albums = Album.query.all()
    return render_template('list_albums.html', albums=albums)


@bp_album.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateAlbumForm()

    if form.validate_on_submit():
        album = Album(
            form.title.data,
            form.artist.data,
            form.description.data,
            form.genre.data,
            save_image_upload(form.image),
            form.release_date.data,
            current_user.id
        )
        db.session.add(album)
        db.session.commit()
        flash(_('New album has been added.'), 'success')
        return redirect(url_for('album.albums_list'))
    return render_template('create_album.html', form=form)


@bp_album.route('/uploads/<filename>', methods=['GET'])
def uploads(filename):
    return send_from_directory(current_app.config['IMAGE_UPLOADS'], filename)


@bp_album.route('/show/<slug>')
@login_required
def show(slug):
    album = Album.query.filter_by(slug=slug).first()
    if not album:
        abort(404)

    return render_template('show_album.html', album=album)


@bp_album.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    form = UpdateAlbumForm()

    album = Album.query.filter_by(slug=slug).first()

    if not album or not current_user.is_album_owner(album):
        flash(_("You are not authorized to do this."), "danger")
        return redirect(url_for("main.home"))

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data
        description = form.description.data
        genre = form.genre.data

        album.title = title
        album.artist = artist
        album.description = description
        album.genre = genre

        db.session.add(album)
        db.session.commit()
        flash(_("The album has been updated."), "success")
        return redirect(url_for("album.show", slug=album.slug))

    form.title.data = album.title
    form.artist.data = album.artist
    form.description.data = album.description
    form.genre.data = album.genre
    return render_template("edit_album.html", album=album, form=form)


# Route for deleting an album
@bp_album.route("/delete/<slug>", methods=["POST"])
@login_required
def delete(slug):
    album = Album.query.filter_by(slug=slug).first()
    if not album or not current_user.is_album_owner(album):
        flash("You are not authorized to do this.", "danger")
        return redirect(url_for("main.index"))
    db.session.delete(album)
    db.session.commit()
    flash(_("The album has been deleted."), "success")
    return redirect(url_for("main.index"))
