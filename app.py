from flask import Flask, jsonify
from flask_jwt import JWT, timedelta
from flask_restful import Api
from resources.users import UserRegister
from security import authenticate, identity as identity_function
from resources.items import Items, Item
from resources.store import StoreList, Store

app = Flask(__name__)
api = Api(app)
app.secret_key = "abc"
app.config["JWT_AUTH_URL_RULE"] = "/login"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
app.config["JWT_AUTH_USERNAME_KEY"] = "email"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
jwt = JWT(app, authenticate, identity_function)


@jwt.jwt_error_handler
def custom_error_handler(error):
    return (
        jsonify({"message": error.description, "code": error.status_code}),
        error.status_code,
    )


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run("localhost", port=9001, debug=True)
