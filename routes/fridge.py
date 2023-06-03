import os
import jwt
import math

from flask import Blueprint, request, jsonify
from models import db, Elements, Users, Fridge
from datetime import datetime, timedelta
from sqlalchemy import and_

fridge_bp = Blueprint('fridge_bp', __name__)

@fridge_bp.route("/fridge/get", methods=["GET"])
def get_fridge():
    header = request.headers.get("Authorization")
    if header:
        try:
            token = header.split(" ")[1]
            payload = jwt.decode(token, os.environ.get(
                'SECRET_KEY'), algorithms=["HS512"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)

            if user is None:
                return jsonify({"message": "User not found"}), 404

            else:
                user_fridge_sql = Fridge.query.filter_by(user_id=user_id).all()
                user_fridge = []
                for el in user_fridge_sql:
                    data = {
                        "product_id": el.product_id,
                        "location": el.location,
                        "expire_data": el.expire_data,
                        "weight": el.weight,
                        "how_much" : el.how_much
                    }
                    user_fridge.append(data)

                return jsonify({"user_fridge" : user_fridge}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401

@fridge_bp.route("/fridge/add", methods=["POST"])
def put_product():
    header = request.headers.get("Authorization")
    if header:
        try:
            token = header.split(" ")[1]
            payload = jwt.decode(token, os.environ.get(
                'SECRET_KEY'), algorithms=["HS512"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)

            if user is None:
                return jsonify({"message": "User not found"}), 404

            else:
                
                data = request.get_json()
                new_note = Fridge(user_id = user_id, product_id = data["product_id"], 
                                  location = data["location"], expire_data = data["expire_data"], 
                                  weight = data["weight"], how_much = data["how_much"])

                db.session.add(new_note)
                db.session.commit()

                return jsonify({"message": "Element added"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401



@fridge_bp.route("/fridge/delete", methods=["DELETE"])
def delete_product():
        header = request.headers.get("Authorization")
        if header:
            try:
                token = header.split(" ")[1]
                payload = jwt.decode(token, os.environ.get(
                    'SECRET_KEY'), algorithms=["HS512"])
                user_id = payload["user_id"]
                user = Users.query.get(user_id)

                if user is None:
                    return jsonify({"message": "User not found"}), 404

                else:

                    data = request.get_json()
                    product_id = data["product_id"]
                    
                    Fridge.query.filter_by(product_id=product_id).delete()
                    db.session.commit()

                    return jsonify({"message": "Element deleted"}), 200

            except jwt.exceptions.DecodeError:
                return jsonify({"message": "Invalid token"}), 401
        else:
            return jsonify({"message": "Missing token"}), 401


@fridge_bp.route("/fridge/change", methods=["PUT"])
def change_product():
    header = request.headers.get("Authorization")
    if header:
        try:    
            token = header.split(" ")[1]
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS512"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)
            if user is None:
                return jsonify({"message": "User not found"}), 404
            else:

                data = request.get_json()
                product_id = data["product_id"]
                location = data["location"]
                expire_data = data["expire_data"]
                weight = data["weight"]
                how_much = data["how_much"]
                product = Fridge.query.filter(and_(Fridge.product_id == product_id, Fridge.user_id == user_id)).first()
               
                if product is None:
                    return jsonify({"message": "Product not found"}), 404
               
               
                else:
                    product.location = location
                    product.expire_data = expire_data   
                    product.weight = weight
                    product.how_much = how_much
                    db.session.commit()
                    return jsonify({"message": "success"}), 200
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    