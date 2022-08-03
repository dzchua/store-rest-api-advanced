from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema
from libs.strings import gettext

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)  # pass list of items

# API wont work if it returns object, only dict
class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        # because it returns object after changing models.item, need to change: JSON represents objects as name/value pairs, just like a Python dictionary.
        if item:
            return item_schema.dump(item), 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        # self.get is from jwt_required || self. is from classmethod
        if ItemModel.find_by_name(name):
            return {"message": gettext("item_name_exists").format(name)}, 400

        item_json = request.get_json()  # price and store_id
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:  # do this if fails to search, then...
            item.save_to_db()
        except:
            return {"message": gettext("item_error_inserting")}, 500

        return item_schema.dump(item), 201  # created, must return json

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": gettext("item_deleted")}, 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)
        # it is just python entity that has name and price not the database
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
