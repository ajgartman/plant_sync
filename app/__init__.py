from flask import Flask
import click
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jinja2 import StrictUndefined

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.undefined = StrictUndefined

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

def shell_context():
    return {'db': db}
app.shell_context_processor(shell_context)

from app import routes


@app.cli.command("init-db")
def init_db():
    """Create tables that do not exist yet."""
    db.create_all()
    click.echo("Database tables are ready.")
