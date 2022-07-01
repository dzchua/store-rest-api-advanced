# import sqlite3
import traceback
from flask_restful import Resource
from flask import render_template, request, make_response
from hmac import compare_digest
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

USER_ALREADY_EXISTS = "A user with that username already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
USER_LOGGED_OUT = "User <id={}> successfully logged out."
INVALID_CREDENTIALS = "Invalid credentials"
NOT_CONFIRMED_ERROR = "You have not confirmed registration, please check your email <{}>."
USER_CONFIRMED = "User confirmed"
FAILED_TO_CREATE = "Internal server error. Failed to create user."
SUCCESS_REGISTER_MESSAGE = "Account created successfully, an email with an activation link has been sent to your email address, please check."

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        # UserModel inside python
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 404
            # user = UserModel(**user_data) no longer needed
        if UserModel.find_by_email(user.email):
            return {"message": EMAIL_ALREADY_EXISTS}, 404

        try:
            user.save_to_db()
            user.send_confirmation_email()
            return {"message": SUCCESS_REGISTER_MESSAGE}, 201
        except:
            traceback.print_exc()  # current error
            return {"message": FAILED_TO_CREATE}, 500


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        # return user from user_database, json calls the json method of user object
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(
            user_json, partial=("email",))  # user_data = UserModel

        user = UserModel.find_by_username(
            user_data.username)  # Find user in user_database

        # authenticate() function || identity() - allows to retrieve the user.id compared to the past where it is done automatically
        # check password
        if user and compare_digest(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(
                    identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED_ERROR.format(user.username)}, 400
        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user, fresh=False
        )  # fresh means user, pass given | not fresh is after some time
        return {"access_token": new_token}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.activated = True
        user.save_to_db()
        # Tells browser its html not json
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation_page.html", email=user.username), 200, headers)
