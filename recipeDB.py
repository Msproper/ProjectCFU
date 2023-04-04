import requests
from flask import Flask
from DBclasses import Users, UserAccount, Recipe, db
import os
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
# URL фотографии


@app.route('/')
@app.route('/home')
def index():
    fds = []
    cr = Recipe.query.all()
    for c in cr:
        fds.append(c.category)
    for i, fd in enumerate(set(fds)):
        print("<option value= \"", i+1, "\">", fd,"</option>")
    return "s"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)