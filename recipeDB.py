import requests
from flask import Flask
from DBclasses import Users, UserAccount, Recipe, db
import os
import time
import operator
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
import ast
# URL фотографии


def sum_by_word(d, word):
    total = 0
    for key, value in d.items():
        if word in key:
            total += value
            print(key)
    print(total)
def convert_to_minutes(time_str):
    pattern = r'(\d+)\s*минут'
    match = re.search(pattern, time_str)
    if match:
        minutes = int(match.group(1))
    else:
        minutes = 0

    pattern = r'(\d+)\s*час'
    match = re.search(pattern, time_str)
    if match:
        hours = int(match.group(1))
    else:
        hours = 0

    total_minutes = minutes + hours * 60
    return total_minutes


@app.route('/')
@app.route('/home')
def index():

    recipes = Recipe.query.all()
    for rec in recipes:
        rec.ingredients = rec.ingredients[1:-1]
    db.session.commit()
    # category = [rec.category for rec in recipes]
    # dict_cat = {key: category.count(key) for key in set(category)}
    # sorted_dict = dict(sorted(dict_cat.items(), key=operator.itemgetter(1), reverse=True))
    # for key, value in sorted_dict.items():
    #     print(f"<option value= \"{key}\">{key}({value})</option>")
    #
    # category = [rec.country for rec in recipes]
    # dict_cat = {key: category.count(key) for key in set(category)}
    # sorted_dict = dict(sorted(dict_cat.items(), key=operator.itemgetter(1), reverse=True))

    # ask = {}
    # for el in recipes:
    #     lst = [x[0] for x in ast.literal_eval(el.ingredients)]
    #     for el in lst:
    #         try:
    #             ask[el] += 1
    #         except:
    #             ask[el] = 1
    # sum_by_word(ask, "масло")
    # sum_by_word(ask, "жир")
    # sum_by_word(ask, "перец")
    # ask2 = dict(sorted(ask.items(), key=operator.itemgetter(1), reverse=True))

    return "s"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)