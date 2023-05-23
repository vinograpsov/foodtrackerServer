# flask run --reload -> auto reloads on changes

import os

from flask import Flask, jsonify

from models import db, Users

from routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.environ.get('USERNAME')}:{os.environ.get('PASSWORD')}@{os.environ.get('DATABASE_SERVER_URL')}/{os.environ.get('DATABASE_NAME')}?ssl_ca={os.environ.get('CERTIFICATE_PATH')}"
)

db.init_app(app)


@app.route("/")
def index():
    return jsonify({"message": "Hello world from the backend!"}), 200


@app.route("/check-db-connection")
def check_db_connection():
    try:
        with app.app_context():
            users = Users.query.all()

            result = ''

            for user in users:
                result += user.username + ' '

            return jsonify({"message": "Database connection successful", "usernames": result.strip()}), 200

    except Exception as e:
        return jsonify({"message": "Database connection failed", "error": str(e)}), 500
