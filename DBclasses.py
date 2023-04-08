from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    acc = db.relationship('UserAccount', backref='user', lazy='dynamic')
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    email = db.Column(db.String(80), unique=True)
    liked_rec = db.Column(db.Text)


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    status = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))



class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    description = db.Column(db.Text)
    country = db.Column(db.Text)
    photo = db.Column(db.Text)
    time = db.Column(db.Integer)
    ingredients = db.Column(db.Text)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    CHO = db.Column(db.Integer)
    text = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    photo_arr = db.Column(db.Text)
    date_column = db.Column(db.Date, default=datetime.date.today)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))