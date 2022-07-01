import sqlite3
from db import db
from typing import Dict, Union
from requests import Response
from flask import request, url_for
from libs.mailgun import Mailgun

MAILGUN_DOMAIN = "sandbox59616f7311ed441080f9ff5ee27692ce.mailgun.org"
MAILGUN_API_KEY = "pubkey-fa2a2750a75017046a571eae39e9c92a"
FROM_TITLE = "Stores REST API"
FROM_EMAIL = "postmaster@sandbox59616f7311ed441080f9ff5ee27692ce.mailgun.org"


class UserModel(db.Model):  # API
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def send_confirmation_email(self) -> Response:
        # http://127.0.0.1:5000/user_confirm/1 from h to before /
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)
        subject = "Registration confirmation"
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"

        return Mailgun.send_email([self.email], subject, text, html)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(
            username=username
        ).first()  # SELECT * FROM users LIMIT 1

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: int) -> "UserModel":
        return cls.query.filter_by(email=email).first()
