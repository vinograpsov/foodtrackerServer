import os
import jwt
import math

from flask import Blueprint, request, jsonify
from models import db, Elements, Users, Fridge
from datetime import datetime, timedelta
from sqlalchemy import and_, text

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
                sql_query = text('SELECT * FROM fridge WHERE user_id = user_id')
                user_fridge_sql = db.session.execute(sql_query, {"user_id": user_id})
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
                product_id = data["product_id"]
                location = data["location"]
                expire_data = data["expire_data"]
                weight = data["weight"]
                how_much = data["how_much"]
                
                product = Fridge.query.filter(and_(Fridge.product_id == product_id, Fridge.user_id == user_id,
                                                    Fridge.expire_data == expire_data, Fridge.location == location)).first()

                if product is not None:
                    product.weight += weight
                    product.how_much += how_much
                    db.session.commit()
                    return jsonify({"message": "Element updated"}), 200
                
                else:
                    new_note = Fridge(user_id = user_id, product_id = product_id, 
                                  location = location, expire_data = expire_data, 
                                  weight = weight, how_much = how_much)

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
                    location = data["location"]
                    expire_data = data["expire_data"]
                    
                    Fridge.query.filter(and_(Fridge.product_id == product_id, Fridge.user_id == user_id,
                                            Fridge.expire_data == expire_data, Fridge.location == location)).delete()
                    
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
                new_data = data["new_data"]
                current_data = data["current_data"]

                current_product_id = current_data["product_id"]
                current_location = current_data["location"]
                current_expire_data = current_data["expire_data"]


                new_expire_data = new_data["expire_data"]
                new_location = new_data["location"]
                new_weight = new_data["weight"]
                new_how_much = new_data["how_much"]


                sql_query = text('SELECT * FROM fridge WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :current_expire_data AND location = :current_location')
                user_fridge_sql = db.session.execute(sql_query, {"user_id": user_id, "current_product_id": current_product_id, "current_expire_data": current_expire_data, "current_location": current_location})
                
                if user_fridge_sql is None:
                    return jsonify({"message": "Product not found"}), 404
                
                else:
                    sql_query1 = text("SELECT * FROM fridge WHERE user_id = :user_id AND product_id = :new_product_id AND expire_data = :new_expire_data AND location = :new_location")
                    if sql_query is None:
                        sql_query2 = text("UPDATE fridge SET expire_data = :new_expire_data, location = :new_location, weight = :new_weight, how_much = :new_how_much WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :current_expire_data AND location = :current_location")
                        db.session.execute(sql_query2, {"user_id": user_id, "current_product_id": current_product_id, "current_expire_data": current_expire_data, "current_location": current_location, "new_expire_data": new_expire_data, "new_location": new_location, "new_weight": new_weight, "new_how_much": new_how_much})
                        return jsonify({"message": "Element updated"}), 200
                    else:
                        sql_query2 = text("UPDATE fridge SET weight = weight + new_weight, how_much = how_much + new_how_much WHERE user_id = :user_id AND :product_id = :current_product_id AND :expire_data = :new_expire_data AND location = :new_location")
                        db.session.execute(sql_query2, {"user_id": user_id, "current_product_id": current_product_id, "new_expire_data": new_expire_data, "new_location": new_location, "new_weight": new_weight, "new_how_much": new_how_much})
                        return jsonify ({"message": "Element updated"}), 200
                
                # # product = Fridge.query.filter(and_(Fridge.product_id == current_product_id, Fridge.user_id == user_id,
                #                                    Fridge.expire_data == current_expire_data, Fridge.location == current_location)).first()
               

                # if product is None:
                #     return jsonify({"message": "Product not found"}), 404
               
               
                # else:
                #     product.location = new_location
                #     product.expire_data = new_expire_data   
                #     product.weight = new_weight
                #     product.how_much = new_how_much
                #     db.session.commit()
                #     return jsonify({"message": "success"}), 200
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    

