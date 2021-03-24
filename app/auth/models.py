from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extentions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    albums = db.relationship('Album', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    tours = db.relationship('Tour', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, username='', email='', password=''):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_album_owner(self, album):
        return self.id == album.user_id

    def is_tour_owner(self, tour):
        return self.id == tour.user_id

    def make_admin(self):
        self.is_admin = True

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
