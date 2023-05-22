import os
import jwt

from flask import Blueprint, request, jsonify
from models import db, Users
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route("/auth/me", methods=["GET"])
def get_user():
    header = request.headers.get("Authorization")
    if header:
        try:
            token = header.split(" ")[1]
            payload = jwt.decode(token, os.environ.get(
                'SECRET_KEY'), algorithms=["HS256"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)
            if user is None:
                return jsonify({"message": "User not found"}), 404
            else:
                return jsonify({
                    "user": {
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "age": user.age,
                        "weight": user.weight,
                        "height": user.height,
                        "sex": user.sex,
                        "activity_level": user.activity_level,
                        "img_url": user.img_url}
                }), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401

    else:
        return jsonify({"message": "Missing token"}), 401


@auth_bp.route("/auth/signin", methods=["POST"])
def signin():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]

    user = Users.query.filter(
        (Users.username == username) | (Users.email == email)).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    elif check_password_hash(user.usr_password, password) is False:
        return jsonify({"message": "Wrong username or password"}), 401
    else:
        token = jwt.encode({"user_id": user.id}, os.environ.get(
            'SECRET_KEY'), algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "weight": user.weight,
                "height": user.height,
                "sex": user.sex,
                "activity_level": user.activity_level,
                "img_url": user.img_url
            }
        }), 200


@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = data["password"]
    age = data["age"]
    weight = data["weight"]
    height = data["height"]
    sex = data["sex"]
    activity_level = data["activity_level"]
    img_url = data["img_url"]

    user_exist = Users.query.filter(
        (Users.username == username) | (Users.email == email)).first()
    if user_exist is not None:
        return jsonify({"message": "User already exist"}), 409
    else:
        new_user = Users(
            username=username,
            email=email,
            usr_password=generate_password_hash(password),
            age=age,
            weight=weight,
            height=height,
            sex=sex,
            activity_level=activity_level,
            img_url=img_url
        )

        db.session.add(new_user)
        db.session.commit()

        token = jwt.encode({"user_id": new_user.id},
                           os.environ.get(
            'SECRET_KEY'), algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "user_id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "age": new_user.age,
                "weight": new_user.weight,
                "height": new_user.height,
                "sex": new_user.sex,
                "activity_level": new_user.activity_level,
                "img_url": new_user.img_url
            }
        }), 201
