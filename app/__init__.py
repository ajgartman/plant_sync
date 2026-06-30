from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jinja2 import StrictUndefined
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.undefined = StrictUndefined

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

def shell_context():
    return {'db': db}
app.shell_context_processor(shell_context)

from app import routes
