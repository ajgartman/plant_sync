import os

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app')
class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'super_secret_default_key')
    SQLALCHEMY_DATABASE_URI = os.getenv("FLASK_DATABASE_URI", "sqlite:///" + os.path.join(base_dir, "data", "app.db"))
