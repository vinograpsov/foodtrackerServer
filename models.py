from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    usr_password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)
    weight = db.Column(db.Float, nullable=False, default=62.0)
    height = db.Column(db.Float, nullable=False, default=175.0)
    sex = db.Column(db.String(6), nullable=False)
    activity_level = db.Column(db.String(100), nullable=True)
    img_url = db.Column(db.String(100), nullable=True)


class Elements(db.Model):
    __tablename__ = 'elements'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    date_usr = db.Column(db.DateTime, primary_key=True)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float)

    # user = db.relationship('Users', backref=db.backref('elements', lazy=True))


class Fridge(db.Model):
    __tablename__ = 'fridge'
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    location = db.Column(db.String(50), nullable=False)
    expire_data = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    how_much = db.Column(db.Float, nullable=False)

    # user = db.relationship('Users', backref=db.backref('fridge', lazy=True))
    # product = db.relationship('Products', backref=db.backref('fridge', lazy=True))


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_name = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float)

    # user = db.relationship('Users', backref=db.backref('products', lazy=True))


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255), nullable=False)
    annotation = db.Column(db.String(255), nullable=False)
    recepe_text = db.Column(db.String(10000), nullable=False)
    rate = db.Column(db.String(1), nullable=False)

    # user = db.relationship('Users', backref=db.backref('recipes', lazy=True))


class RecipesProducts(db.Model):
    __tablename__ = 'recipes_products'
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(
        'recipes.id'), primary_key=True)

    # product = db.relationship('Users', backref=db.backref('recipes_products', lazy=True))
    # recipe = db.relationship('Products', backref=db.backref('recipes_products', lazy=True))
