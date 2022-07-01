from flask_restful import Resource
from schemas.store import StoreSchema
from models.store import StoreModel

NAME_ALREADY_EXIST = "A store with name '{}' already exists."
ERROR_CREATING = "An error occurred while creating the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted"

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    def get(self, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):  # search
        if StoreModel.find_by_name(name):
            return {
                {"message": NAME_ALREADY_EXIST.format(name)},
                400,
            }

        # its a dict, since __init__ is gone
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": ERROR_CREATING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": STORE_DELETED}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_list_schema(StoreModel.find_all())}, 200
        # access query find_all in here instead of making resource interact with database
