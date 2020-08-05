from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cant be blank!!!!!!!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This filed cant be blank!!!!!!"
    )

    def post(self):
        try:
            data = UserRegister.parser.parse_args()
            if UserModel.find_user_by_name(data["username"]):
                return {"message": "User with this name already exists!!!"}, 400
            user = UserModel(**data)
            user.save_user_to_db()
            return {"message": "user created sucussfully"}, 201
        except Exception as err:
            print(err)
