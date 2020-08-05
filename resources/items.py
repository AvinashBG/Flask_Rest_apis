from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="The field cant be left blank!"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="Each item must have a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        return item.json(), 200 if item else 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {"message": f"{name} already exists"}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            return (
                {"message": "error occured while inserting values into db:\t" + str(e)},
                500,
            )
        return {"items": item.json()}, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item:
            item.price = data["price"]
            item.store_id = data["store_id"]
        else:
            item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            return {"message": "error occured while inseting values into db"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_item()
            return {"message": f" item {name} is deleted "}, 200
        else:
            return {"message": f"item {name} not found"}, 404


class Items(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
