import requests
from flask import Flask
from DBclasses import Users, UserAccount, Recipe, db
import os
import time
import operator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
# URL фотографии


@app.route('/')
@app.route('/home')
def index():
    fds = []
    ddd = {}
    cr = Recipe.query.all()
    for c in cr:
        fds.append(c.country)
    for item in set(fds):
        count = fds.count(item)
        ddd[item] = count

    print(ddd)
    sorted_dict = dict(sorted(ddd.items(), key=operator.itemgetter(1), reverse=True))
    print(sorted_dict)
    for key, value in sorted_dict.items():
        print(f"<option value= \"{key}\">{key}({value})</option>")
    return "s"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)