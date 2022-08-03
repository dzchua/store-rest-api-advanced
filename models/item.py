from typing import List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)  # read the columns
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

    @classmethod  # returns the object of ItemModel not dictionary
    def find_by_name(cls, name: str) -> "ItemModel":
        # query from class || SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    # ItemModel represents the item and should insert itself, classmethod is not needed since insert(takes in item)
    def save_to_db(self) -> None:  # insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
