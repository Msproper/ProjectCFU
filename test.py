from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    date = db.Column(db.DateTime)
    User_id = db.Column(db.Integer, db.ForeignKey('users.id'))


from datetime import datetime

date_str = '2022-03-26'
date_obj = datetime.strptime(date_str, '%Y-%m-%d')

with app.app_context():
    user = UserAccount(name="daniar", surname="Afminov", date=date_obj, User_id=6)
    db.session.query(Users).delete()
    db.session.query(UserAccount).delete()
    db.session.commit()


