import os  # read the virtual environment

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
# JWT string of info encoded, to know it refers to which user
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from ma import ma
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, UserConfirm
from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

# uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # to know object changed but not saved in database: turn it off as it is a tracker
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
# app.config['JWT_SECRET_KEY']
app.secret_key = os.environ.get("APP_SECRET_KEY")
api = Api(app)


@app.before_first_request  # create database
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except validationerror as err
    return jsonify(err.messages), 400


# app.config['JWT_AUTH_URL_RULE'] = '/login' # changes /auth to /login
jwt = JWTManager(app)  # not creating /auth


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload["jti"] in BLACKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")

# only file that is run = main, if main=name: run the file and start flask server
if __name__ == "__main__":
    ma.init_app(app)
    db.init_app(app)
    app.run(port=5000, debug=True)  # error msg to tell
