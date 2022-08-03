from requests import Response
from flask import request, url_for
from flask_restful import Resource

from db import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    # activated = db.Column(db.Boolean, default=False)  # we have confirmation.py
    # lazy-dynamic: confirmation only retrieved when accessed, not created table. || delete-orphan: deletes confirmation related to user
    confirmation = (
        db.relationship(  # delete-orphan: deletes all associated confirmations<->user
            "ConfirmationModel",
            lazy="dynamic",
            cascade="all, delete-orphan",
            back_populates="user",
        )
    )

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        # ordered by expiration time (in descending order)
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        # configure e-mail contents
        subject = "Registration Confirmation"
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )  # above comment changed due to accessable to anyone to -> using uuid4 | 127.0.0.1:5000/user_confirm/j32k4j2f

        # string[:-1] means copying from start (inclusive) to the last index (exclusive)
        # from `http://127.0.0.1:5000/` to `http://127.0.0.1:5000`, since the url_for() would also contain a `/`
        # http://127.0.0.1:5000/user_confirm/1 from h to before /
        # https://stackoverflow.com/questions/509211/understanding-pythons-slice-notation
        text = f"Please click the link to confirm your registration: {link}"
        html = f"<html>Please click the link to confirm your registration: <a href={link}>link</a></html>"
        # send e-mail with MailGun
        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
