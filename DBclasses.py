from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    acc = db.relationship('UserAccount', backref='user', lazy='dynamic')
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    country = db.Column(db.Text)
    photo = db.Column(db.Text)
    time = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    text = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))