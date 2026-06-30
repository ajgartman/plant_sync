from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), index=True, unique=True)
    account_type: Mapped[str] = mapped_column(String(30),index=True)
    pw_hash: Mapped[str] = mapped_column(String(256), unique=True)

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

class Issues(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    desc: Mapped[str] = mapped_column(String(150),index=True)
    date: Mapped[datetime] = mapped_column(index=True,default=lambda:datetime.date())
    submitted_by: Mapped[int] = mapped_column(index=True)
    completed_by: Mapped[int] = mapped_column(index=True)
    area: Mapped[int] = mapped_column(index=True)
    status: Mapped[str] = mapped_column(index=True)
    priority: Mapped[str] = mapped_column(index=True)