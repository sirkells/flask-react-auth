import os

from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql import func

from app import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


# ModelView allows the admin have access to your database models:
if os.getenv("FLASK_ENV") == "development":
    from app import admin
    from app.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
