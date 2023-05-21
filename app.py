from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from models import db, Users, Elements, Fridge, Products, Recipes, RecipesProducts


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
@app.route("/auth/me",methods=["GET"])
def h():
    return "Auth me"

@app.route("/auth/signin",methods=["POST"])
def signin():
    return "Sign in"

@app.route("/auth/signup",methods=["POST"])
def signup():
    return "Sign up"

@app.route("/calories",methods=["GET"])
def calories_get():
    return "Calories"

@app.route("/calories",methods=["POST"])
def calories_post():
    return "Calories"

@app.route("/fridge/bymyself",methods=["POST"])
def fridge_bymyself():
    return "Fridge by myself"

@app.route("/fridge/byqrcode", methods=["POST"])
def fridge_byqrcode():
    return "Fridge by QR code"

@app.route("/fridge/<int:product_id>", methods=["DELETE"])
def fridge_delete(product_id):
    return "Fridge delete"

@app.route("/fridge/<int:product_id>", methods=["PATCH"])
def fridge_patch(product_id):  
    return "Fridge patch"

@app.route("/recepes/my", methods = ["GET"])
def recepes_my():
    return "Recepes my"

@app.route("/recepes/global", methods = ["POST"])
def recepes_global():
    return "Recepes global post"

@app.route("/recepes/global", methods = ["GET"])
def recepes_global_get():
    return "Recepes global get"

@app.route("/settings", methods = ["PATCH"])
def settings_patch():
    return "Settings patch"
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

