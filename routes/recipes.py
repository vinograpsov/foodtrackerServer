import os
import jwt

from flask import Blueprint, request, jsonify
from models import db, Products, Users, Recipes
from datetime import datetime, timedelta 
from sqlalchemy import and_

recipes_bp = Blueprint('recipes_bp', __name__)


@recipes_bp.route("/recipes", methods = ["POST"])
def add_recipes():
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
                    data = request.get_json()
                    name = data["name"] 
                    annotation = data["annotation"]
                    recepe_text = data["text"]
                    
                    new_recipe = Recipes(user_id = user_id, name = name, annotation = annotation, recepe_text = recepe_text)
                    db.session.add(new_recipe)
                    db.session.commit()

                    return jsonify({"message": "Recipe added"}), 200
                    
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401 
    else:
        return jsonify({"message": "Missing token"}), 401
    


    
@recipes_bp.route("/recipes", methods = ["GET"])
def get_recipes():
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
                    
                    recipes = Recipes.query.all()
                    if not recipes:
                        return jsonify({"message": "No recipes found"}), 404
                    else:
                        recipes_json = []
                        for i in recipes:
                            recipes_json.append({
                                "id": i.id,
                                "name": i.name,
                                "annotation": i.annotation,
                                "text": i.recepe_text,
                                "user_id": i.user_id
                            })
                        return jsonify({"recipes" : recipes_json}), 200
                    



        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401 
    else:
        return jsonify({"message": "Missing token"}), 401
    


@recipes_bp.route("/recipes", methods = ["PUT"])
def update_recipes():
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
                    
                    data = request.get_json()
                    recipe_id = data["id"]
                    recipe = Recipes.query.get(recipe_id)
                    if recipe is None:
                        return jsonify({"message": "Recipe not found"}), 404
                    else:
                        recipe.name = data["name"]
                        recipe.annotation = data["annotation"]
                        recipe.recepe_text = data["text"]
                        db.session.commit()
                        return jsonify({"message": "Recipe updated"}), 200
                    
        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401 
    else:
        return jsonify({"message": "Missing token"}), 401    