import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'top_secret'
    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DB_URI') or f'sqlite:///{os.path.join(base_dir, "music.db")}'
    IMAGE_UPLOADS = os.environ.get('FLASK_UPLOADS_FOLDER_URI') or os.path.join(base_dir, 'uploads')


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_dir, "music.db")}'
    IMAGE_UPLOADS = os.path.join(base_dir, 'uploads')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_dir, "test_music.db")}'
    IMAGE_UPLOADS = os.path.join(base_dir, 'uploads')
