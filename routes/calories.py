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
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS512"])
            user_id = payload["user_id"]
            user = Users.query.get(user_id)
            if user is None:
                return jsonify({"message": "User not found"}), 404
            else:

                start_date = datetime.now() - timedelta(days=31)
                end_date = datetime.now()

                user_elements = Elements.query.filter(and_(Elements.user_id == user_id, 
                                                      Elements.date_usr.between(start_date, end_date))).all()


                if not user_elements:
                    return jsonify({"message": "No elements found"}), 404

                else:
            
                    user_stats = {}
                    for el in user_elements:
                        date = el.date_usr.date()
                        if date in user_stats:
                            user_stats[date]["calories"] += el.calories
                            user_stats[date]["protein"] += el.protein
                            user_stats[date]["fat"] += el.fat
                            user_stats[date]["carbohydrates"] += el.carbohydrates
                        else:
                            user_stats[date] = {
                                "calories" : el.calories,
                                "protein" : el.protein,
                                "fat" : el.fat,
                                "carbohydrates" : el.carbohydrates
                            }
                            

                    response = []
                    for key, value in user_stats.items():
                        response.append({
                            "date" : key,
                            "calories" : value["calories"],
                            "protein" : value["protein"],
                            "fat" : value["fat"],
                            "carbohydrates" : value["carbohydrates"]
                        })


                    return jsonify({
                        "stats_by_date" : response,
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
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS512"])
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
    

    


@calories_bp.route("/calories/consumption", methods=["GET"])
def get_consumption():
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

                user_callories_consumption = daily_callories(user.sex, user.weight, user.height, user.age, user.activity_level)
                
                return jsonify({
                    "callories" : user_callories_consumption,
                    "protein" : daily_proteins(user_callories_consumption),
                    "fats" : daily_fats(user_callories_consumption),
                    "carbohydrates" : daily_carbohydrates(user_callories_consumption)
                    }), 200

        except jwt.exceptions.DecodeError:
            return jsonify({"message": "Invalid token"}), 401
    else:
        return jsonify({"message": "Missing token"}), 401
    


def daily_callories(sex, weight, height, age, activity):
    add_coiff = 0
    activity_map = {"minimal" : 1.2, "weak" : 1.375, "medium" : 1.55, "high" : 1.7, "extra activity" : 1.9}
    if sex == "m":
        add_coiff = 5
    elif sex == "f":
        add_coiff = -161
    return (10 * weight + 6.25 * height - 5 * age + add_coiff) * activity_map[activity]

def daily_fats(calories):
    return calories * 0.3 / 4

def daily_proteins(calories):
    return calories * 0.3 / 9

def daily_carbohydrates(calories):
    return calories * 0.4 / 4
