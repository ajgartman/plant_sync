"""Back up the local SQLite file, then recreate its tables from the current models."""

from datetime import datetime
from pathlib import Path
import shutil
import sqlite3
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import app, db
from app.models import Area, Company, Issues, User  # noqa: F401 - register every model
from config import DATABASE_PATH


database_path = Path(DATABASE_PATH)
backup_path = database_path.with_name(
    f"{database_path.stem}.backup-{datetime.now():%Y%m%d-%H%M%S}{database_path.suffix}"
)

if database_path.exists():
    with sqlite3.connect(database_path) as connection:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        raise RuntimeError(f"Database integrity check failed: {integrity}")
    shutil.copy2(database_path, backup_path)
    print(f"Backed up existing database to {backup_path}")

with app.app_context():
    db.drop_all()
    with db.engine.begin() as connection:
        connection.exec_driver_sql("DROP TABLE IF EXISTS _alembic_tmp_issues")
        connection.exec_driver_sql("DROP TABLE IF EXISTS alembic_version")
    db.create_all()
    with db.engine.connect() as connection:
        table_names = sorted(db.engine.dialect.get_table_names(connection))

print("Created tables: " + ", ".join(table_names))
