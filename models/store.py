# import sqlite3
from pickletools import string1
from typing import List
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)  # read the columns
    name = db.Column(db.String(80), nullable=False, unique=True)

    # lazy='dynamic' to tell ItemModel not to create each item for each store yet
    items = db.relationship("ItemModel", lazy="dynamic")

    @classmethod  # returns the object of ItemModel not dictionary
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(
            name=name
        ).first()  # query from class || SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:  # insert and update
        db.session.add(self)  # for one insert
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
