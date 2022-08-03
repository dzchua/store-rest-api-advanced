from flask import Flask, jsonify
from flask_restful import Api

# JWT string of info encoded, to know it refers to which user
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_uploads import configure_uploads
from dotenv import load_dotenv, find_dotenv

from db import db
from ma import ma
from blocklist import BLOCKLIST
from resources.user import (
    UserRegister,
    UserLogin,
    User,
    TokenRefresh,
    UserLogout,
    UserConfirm,
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
from libs.image_helper import IMAGE_SET


app = Flask(__name__)
load_dotenv(find_dotenv(), verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
# override with config.py (APPLICATION_SETTINGS points to config.py)
app.config.from_envvar("APPLICATION_SETTINGS")
# restrict max upload image size to 10MB
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

# app.config['UPLOADED_FILES_DEST'] = os.path.join(app.root_path, 'static', 'uploads', 'files')
# app.config['GENERATED_DIR'] = os.path.join(app.root_path, app.config['BUILD_DEST'])
configure_uploads(app, IMAGE_SET)
api = Api(app)


@app.before_first_request  # create database
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):  # except validationerror as err
    return jsonify(err.messages), 400


# app.config['JWT_AUTH_URL_RULE'] = '/login' # changes /auth to /login
jwt = JWTManager(app)  # not creating /auth


# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Confirmation, "/user_confirm/<string:confirmation_id>")
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(UserConfirm, "/user_confirm/<int:user_id>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")

# only file that is run = main, if main=name: run the file and start flask server
if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000)
