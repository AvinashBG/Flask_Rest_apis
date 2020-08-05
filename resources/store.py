from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.json(), 200
        return {"messgae": f"{name}store not found"}, 404

    def post(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {"message": f"{name} already exists"}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
            return {"message": "store is created"}, 201
        except:
            return {"messgae": "an error has occured while saving to db"}, 500

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            try:
                store.delete_store()
                return {"message": "Store been deleted "}, 200
            except:
                return {"message": "An error occured while deleting the store"}, 500
        return {"message": f"Unable to locate {name}"}, 404


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda store: store.json(), StoreModel.query.all()))}
