from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    pw_hash: Mapped[str] = mapped_column(String(256), unique=True)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"
