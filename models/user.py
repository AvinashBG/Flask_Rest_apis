from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.name = username
        self.password = password

    def json(self):
        return {"name": self.name, "password": self.password}

    @classmethod
    def find_user_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_user_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    def save_user_to_db(self):
        db.session.add(self)
        db.session.commit()
