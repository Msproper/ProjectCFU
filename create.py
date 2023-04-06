#Напиши программу, которая примет значения из таблицы xlsx и запишет их в базу данных sqlite. Я использую flask-alchemy

import pandas as pd
from flask import Flask
from DBclasses import Users, UserAccount, db, Recipe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # указываем uri базы данных
db.init_app(app)


@app.route('/')
def home():
    data = pd.read_excel('recipes.xlsx')
    db.session.commit()
    for i in range(len(data)):
        row = Recipe(
            name = str(data.iloc[i][0]),
            category = str(data.iloc[i][1]),
            description = str(data.iloc[i][2]),
            country = str(data.iloc[i][3]),
            photo = str(data.iloc[i][4]),
            time = str(data.iloc[i][5]),
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
