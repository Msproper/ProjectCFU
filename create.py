import pandas as pd
from flask import Flask
from DBclasses import Users, UserAccount, db, Recipe
import re
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

import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # указываем uri базы данных
db.init_app(app)


@app.route('/')
def home():
    data = pd.read_excel('recipes.xlsx')
    user = Users(username='daniar', password=123, email='aminov.daniar0@gmail.com', liked_rec=json.dumps([1, 2]))
    user_account = UserAccount(name="daniar", surname="aminov",status="somebody once told me" , user_id=1)
    db.session.add(user)
    db.session.add(user_account)
    db.session.commit()
    for i in range(len(data)):
        row = Recipe(
            name = str(data.iloc[i][0]),
            category = str(data.iloc[i][1]),
            description = str(data.iloc[i][2]),
            country = str(data.iloc[i][3]).replace("кухня", ""),
            photo = str(data.iloc[i][4]),
            time = str(convert_to_minutes(data.iloc[i][5])),
            ingredients = str(data.iloc[i][6]),
            calories=str(data.iloc[i][7]),
            protein=str(data.iloc[i][8]),
            fat=str(data.iloc[i][9]),
            CHO=str(data.iloc[i][10]),
            text = str(data.iloc[i][11]),
            photo_arr=str(data.iloc[i][12]),
            author_id = 1
        )
        db.session.add(row)
    db.session.commit()

    return str(Recipe.query.first())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)