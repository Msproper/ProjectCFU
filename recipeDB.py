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
# URL фотографии

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
    category = [rec.category for rec in recipes]
    dict_cat = {key: category.count(key) for key in set(category)}
    sorted_dict = dict(sorted(dict_cat.items(), key=operator.itemgetter(1), reverse=True))
    for key, value in sorted_dict.items():
        print(f"<option value= \"{key}\">{key}({value})</option>")

    category = [rec.country for rec in recipes]
    dict_cat = {key: category.count(key) for key in set(category)}
    sorted_dict = dict(sorted(dict_cat.items(), key=operator.itemgetter(1), reverse=True))
    for key, value in sorted_dict.items():
        print(f"<option value= \"{key}\">{key}({value})</option>")

    time = [convert_to_minutes(rec.time) for rec in recipes]
    ranges = {"5-15": 0, "15-30": 0, "30-60": 0, "60-120": 0, "120+": 0}

    for num in time:
        if num <= 15:
            ranges["5-15"] += 1
        elif num <= 30:
            ranges["15-30"] += 1
        elif num <= 60:
            ranges["30-60"] += 1
        elif num <= 120:
            ranges["60-120"] += 1
        else:
            ranges["120+"] += 1

    calories = [rec.calories for rec in recipes]
    ranges = {"250-": 0, "250-500": 0, "500-750": 0, "750-1000": 0, "1000+": 0}
    for num in calories:
        if num <= 125:
            ranges["250-"] += 1
        elif num <= 250:
            ranges["250-500"] += 1
        elif num <= 750:
            ranges["500-750"] += 1
        elif num <= 1000:
            ranges["750-1000"] += 1
        else:
            ranges["1000+"] += 1

    for key, value in ranges.items():
        print(f"<option value= \"{key}\">{key}({value})</option>")
    return "s"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)