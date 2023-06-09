import os
import jwt

from flask import Blueprint, request, jsonify
from models import db, Users, Fridge
from sqlalchemy import and_, text

fridge_bp = Blueprint('fridge_bp', __name__)


@fridge_bp.route("/fridge", methods=["GET"])
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
                sql_query = text(
                    'SELECT * FROM fridge WHERE user_id = user_id')

                user_fridge_sql = db.session.execute(
                    sql_query, {"user_id": user_id})

                user_fridge = []

                for el in user_fridge_sql:
                    data = {
                        "id": el.product_id,
                        "location": el.location,
                        "expires": el.expire_data,
                        "weight": el.weight,
                        "quantity": el.how_much
                    }
                    user_fridge.append(data)

                return jsonify({"fridge": user_fridge}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401


@fridge_bp.route("/fridge", methods=["POST"])
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

                product_id = data["id"]
                # product_name = data["name"]
                location = data["location"]
                expire_data = data["expires"]
                weight = data["weight"]
                how_much = data["quantity"]

                product = Fridge.query.filter(and_(Fridge.product_id == product_id, Fridge.user_id == user_id,
                                                   Fridge.expire_data == expire_data, Fridge.location == location)).first()

                if product is not None:
                    product.weight += weight
                    product.how_much += how_much

                    db.session.commit()

                    return jsonify({"message": "product updated"}), 200

                else:
                    new_note = Fridge(user_id=user_id, product_id=product_id,
                                      location=location, expire_data=expire_data,
                                      weight=weight, how_much=how_much)

                    db.session.add(new_note)
                    db.session.commit()

                return jsonify({"message": "product added"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401


@fridge_bp.route("/fridge", methods=["DELETE"])
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

                sql_query_delete = text(
                    "DELETE FROM fridge WHERE user_id = :user_id AND product_id = :product_id AND expire_data = :expire_data AND location = :location")
                db.session.execute(sql_query_delete, {
                                   "user_id": user_id, "product_id": product_id, "expire_data": expire_data, "location": location})
                db.session.commit()

                return jsonify({"message": "ok"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401


@fridge_bp.route("/fridge", methods=["PUT"])
def change_product():
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
                new_data = data["new_data"]
                current_data = data["current_data"]

                current_product_id = current_data["product_id"]
                current_location = current_data["location"]
                current_expire_data = current_data["expire_data"]

                new_expire_data = new_data["expire_data"]
                new_location = new_data["location"]
                new_weight = new_data["weight"]
                new_how_much = new_data["how_much"]

                sql_query = text(
                    'SELECT * FROM fridge WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :current_expire_data AND location = :current_location')
                user_fridge_sql = db.session.execute(sql_query, {
                                                     "user_id": user_id, "current_product_id": current_product_id, "current_expire_data": current_expire_data, "current_location": current_location})
                user_fridge_sql_result = user_fridge_sql.first()

                if user_fridge_sql_result is None:
                    return jsonify({"message": "Product not found"}), 404
                else:
                    sql_query_copy = text(
                        'SELECT * FROM fridge WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :new_expire_data AND location = :new_location')
                    copy_element = db.session.execute(sql_query_copy, {
                                                      "user_id": user_id, "current_product_id": current_product_id, "new_expire_data": new_expire_data, "new_location": new_location})
                    copy_element_result = copy_element.first()

                    if copy_element_result is None:
                        sql_query_update = text(
                            "UPDATE fridge SET expire_data = :new_expire_data, location = :new_location, weight = :new_weight, how_much = :new_how_much WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :current_expire_data AND location = :current_location")
                        updated_val = db.session.execute(sql_query_update, {"user_id": user_id, "current_product_id": current_product_id, "current_expire_data": current_expire_data,
                                                         "current_location": current_location, "new_expire_data": new_expire_data, "new_location": new_location, "new_weight": new_weight, "new_how_much": new_how_much})
                        db.session.commit()
                        return jsonify({"message": "Old element updated"}), 200
                    else:
                        copy_element_result
                        new_weight += copy_element_result.weight
                        new_how_much += copy_element_result.how_much
                        sql_query_update = text(
                            "UPDATE fridge SET weight = :new_weight, how_much = :new_how_much WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :new_expire_data AND location = :new_location")
                        sql_query_delete = text(
                            "DELETE FROM fridge WHERE user_id = :user_id AND product_id = :current_product_id AND expire_data = :current_expire_data AND location = :current_location")
                        db.session.execute(sql_query_update, {"user_id": user_id, "current_product_id": current_product_id,
                                           "new_expire_data": new_expire_data, "new_location": new_location, "new_weight": new_weight, "new_how_much": new_how_much})
                        db.session.execute(sql_query_delete, {"user_id": user_id, "current_product_id": current_product_id,
                                           "current_expire_data": current_expire_data, "current_location": current_location})
                        db.session.commit()
                        return jsonify({"message": "Merge elements"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
