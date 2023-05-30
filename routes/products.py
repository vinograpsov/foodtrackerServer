import os
import jwt

from flask import Blueprint, request, jsonify
from models import db, Products, Users
from datetime import datetime, timedelta 
from sqlalchemy import and_

products_bp = Blueprint('products_bp', __name__)


@products_bp.route("/products/added_by_me", methods=["GET"])
def added_by_me():
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
                products_added_by_user = Products.query.filter(Products.user_id == user_id).all()
                if not products_added_by_user:
                    return jsonify({"message": "No products found"}), 404
                else:
                    products = []
                    for product in products_added_by_user:
                        products.append({
                            "product_id" : product.id,
                            "product_name" : product.product_name,
                            "calories" : product.calories,
                            "protein" : product.protein,
                            "fat" : product.fat,
                            "carbohydrates" : product.carbohydrates
                        })
                    return jsonify({"message": "success","products": products}), 200
                
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
        
    else:
        return jsonify({"message": "Missing token"}), 401
    

@products_bp.route("/products/add", methods=["POST"])
def get_calories():
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
                product_name = data["product_name"]
                calories = data["calories"]
                protein = data["protein"]
                fat = data["fat"]
                carbohydrates = data["carbohydrates"]
                
                product = Products.query.filter(Products.product_name == product_name).first()
                if product is not None:
                    return jsonify({"message": "Product already exists"}), 409
                
                product = Products(product_name=product_name, calories=calories, protein=protein, fat=fat, carbohydrates=carbohydrates, user_id=user_id)
                db.session.add(product)
                db.session.commit()

                return jsonify({"message": "success"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    

@products_bp.route("/products/change", methods=["PUT"])
def change_product():
    header = request.headers.get("Authorization")
    if header:
        try:    
            token = header.split(" ")[1]
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)
            if user is None:
                return jsonify({"message": "User not found"}), 404
            else:
                data = request.get_json()
                product_id = data["product_id"]
                product_name = data["product_name"]
                calories = data["calories"]
                protein = data["protein"]
                fat = data["fat"]
                carbohydrates = data["carbohydrates"]
                product = Products.query.filter(and_(Products.id == product_id, Products.user_id == user_id)).first()
                if product is None:
                    return jsonify({"message": "Product not found"}), 404
                else:
                    product.product_name = product_name
                    product.calories = calories
                    product.protein = protein
                    product.fat = fat
                    product.carbohydrates = carbohydrates
                    db.session.commit()
                    return jsonify({"message": "success"}), 200
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    