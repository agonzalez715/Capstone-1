# from app import db  # Import db from the current package
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(20), nullable=True)
    drive = db.Column(db.String(10), nullable=True)
    cylinders = db.Column(db.Integer, nullable=True)
    transmission = db.Column(db.String(20), nullable=True)
    city_mpg = db.Column(db.Integer, nullable=True)
    highway_mpg = db.Column(db.Integer, nullable=True)
    combined_mpg = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    on_sale = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = db.relationship('Car')
