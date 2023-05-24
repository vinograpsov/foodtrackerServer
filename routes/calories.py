import os
import jwt

from flask import Blueprint, request, jsonify
from models import db, Elements, Users
from datetime import datetime, timedelta 
from sqlalchemy import and_

calories_bp = Blueprint('calories_bp', __name__)

@calories_bp.route("/calories", methods=["GET"])
def get_calories():
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

                start_date = datetime.now() - timedelta(days=7)
                end_date = datetime.now()

                user_elements = Elements.query.filter(and_(Elements.user_id == user_id, 
                                                      Elements.date_usr.between(start_date, end_date))).all()


                if not user_elements:
                    return jsonify({"message": "No elements found"}), 404

                else:
                    user_stats = []
                    for el in user_elements:
                        user_stats.append({
                            "calories" : el.calories,
                            "protein" : el.protein,
                            "fat" : el.fat,
                            "carbohydrates" : el.carbohydrates
                        })

                    return jsonify({
                        "user_id" : user_id,
                        "stats" : user_stats,
                        "start_date" : start_date,
                        "end_date" : end_date
                    }), 200  


        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    

@calories_bp.route("/calories", methods=["POST"])
def add_calories():
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

                calories = data["calories"]
                protein = data["protein"]
                fat = data["fat"]
                carbohydrates = data["carbohydrates"]
                current_datetime = datetime.now()

                new_element = Elements(user_id = user_id, date_usr = current_datetime,
                                       calories = calories, protein = protein, fat = fat,
                                       carbohydrates = carbohydrates)

                db.session.add(new_element)
                db.session.commit()

                return jsonify({"message": "Element added"}), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401