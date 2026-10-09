import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "app", "data")
DATABASE_PATH = os.path.join(DATABASE_DIR, "app.db")
os.makedirs(DATABASE_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + DATABASE_PATH.replace(os.sep, "/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
