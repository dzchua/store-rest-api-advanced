from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.item import ItemModel
from flask import request
from marshmallow import Schema, ValidationError
from schemas.item import ItemSchema
#from typing import Dict, list

NAME_ALREADY_EXIST = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)  # pass list of items

# API wont work if it returns object, only dict


class Item(Resource):
    @classmethod
    def get(cls, name: str):  # READ
        item = ItemModel.find_by_name(name)
        if item:
            return (
                item_schema.dump(item), 200
            )  # because it returns object after changing models.item, need to change: JSON represents objects as name/value pairs, just like a Python dictionary.
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):  # CREATE
        if ItemModel.find_by_name(
            name
        ):  # self.get is from jwt_required || self. is from classmethod
            return {"message": NAME_ALREADY_EXIST.format(name)}, 400

        item_json = request.get_json()  # price and store_id
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:  # do this if fails to search, then...
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500  # internal server error

        return item_schema.dump(item), 201  # created, must return json

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):  # UPDATE
        item_json = request.get_json()
        item = ItemModel.find_by_name(
            name
        )  # it is just python entity that has name and price not the database

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name
            item = item_schema.load(item_json)

        item.save_to_db()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        # returns list of each item
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200

        # return {'items': [item.json() for item in ItemModel.find_all()]} #return json instead of all objects
        # or              list(map(lambda x: x.json(), ItemModel.query.all())) || mapping of functions to elements
