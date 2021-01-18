from secrets import token_urlsafe

from slugify import slugify
from sqlalchemy import event

from app.extentions import db


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text(), nullable=False)
    release_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), index=True, nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title, artist, description, genre, image, release_date, user_id):
        self.title = title
        self.artist = artist
        self.description = description
        self.genre = genre
        self.image = image
        self.release_date = release_date
        self.user_id = user_id


def update_slug(target, value, old_value, initiator):
    print(target, value, old_value, initiator)

    target.slug = slugify(value) + '-' + token_urlsafe(3)


event.listen(Album.title, 'set', update_slug)
