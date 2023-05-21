from flask import Flask, jsonify,  request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db, Users, Elements, Fridge, Products, Recipes, RecipesProducts
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

SECRET_KEY = 'tmp_secret_key'

# ----------------- DATABASE CONNECTION-----------------
def get_db_secrets():
    with open('./secrets.txt', 'r') as f:
        username = f.readline().strip()
        password = f.readline().strip() 
    return username, password

app = Flask(__name__)
username, password = get_db_secrets()
database_server_url = 'food-app-server.mysql.database.azure.com'
database_name = 'foodtracker'
cert_path = './certs/DigiCertGlobalRootCA.crt.pem'

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{username}:{password}@{database_server_url}/{database_name}"
    f"?ssl_ca={cert_path}"
)
db.init_app(app)
# ----------------- DATABASE CONNECTION-----------------


# -----------------  ADD VIEWS -----------------
from views import *
# -----------------  ADD VIEWS -----------------



if __name__ == "__main__":
    with app.app_context():
        db.create_all();
        try:
            users = Users.query.all()
            for user in users:
                print(f"User ID: {user.id}, Username: {user.username}")

            elements = Elements.query.all()
            for element in elements:
                print(f"User ID: {element.user_id}, Date: {element.date_usr}")

            fridges = Fridge.query.all()
            for fridge in fridges:
                print(f"User ID: {fridge.user_id}, Product ID: {fridge.product_id}")

            products = Products.query.all()
            for product in products:
                print(f"Product ID: {product.id}, Product Name: {product.product_name}")

            recipes = Recipes.query.all()
            for recipe in recipes:
                print(f"Recipe ID: {recipe.id}, Recipe Name: {recipe.name}")

            recipes_products = RecipesProducts.query.all()
            for rp in recipes_products:
                print(f"Product ID: {rp.product_id}, Recipe ID: {rp.recipe_id}")
        except Exception as e:
            print("connection to database failed")
            print(e)    

