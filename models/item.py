# import sqlite3
from typing import Dict, List, Union
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)  # read the columns
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey(
        "stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

    @classmethod  # returns the object of ItemModel not dictionary
    def find_by_name(cls, name: str) -> "ItemModel":
        # query from class || SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return cls(*row) #instead of row[0] and 1, since name and price correspond accordingly

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    # ItemModel represents the item and should insert itself, classmethod is not needed since insert(takes in item)
    def save_to_db(self) -> None:  # insert and update
        db.session.add(self)  # for one insert
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)" #delete specific column: unique
        # cursor.execute(query, (self.name, self.price)) #
        #
        # connection.commit()
        # connection.close()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name)) #
        #
        # connection.commit()
        # connection.close()
