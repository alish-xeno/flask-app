import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.store import Store, StoreList
from resources.item import Item, ItemList

app = Flask(__name__)
db_value_conf = os.environ.get('DATABASE_URL', "sqlite:///data.db")
if db_value_conf and db_value_conf.startswith("postgres://"):
    db_value_conf = db_value_conf.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_value_conf
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "alish"
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


