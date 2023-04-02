#Напиши программу, которая примет значения из таблицы xlsx и запишет их в базу данных sqlite. Я использую flask-alchemy

import pandas as pd
from flask import Flask
from DBclasses import Users, UserAccount, db, Recipe


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # указываем uri базы данных
db.init_app(app)


@app.route('/')
def home():
    user = Users(
        username = "daniar",
        password = "123"
    )
    db.session.add(user)
    db.session.commit()
    useracc = UserAccount(
        name = "BookCookHub",
        user_id = 1
    )
    db.session.add(useracc)
    data = pd.read_excel('recipe.xlsx')
    db.session.commit()
    for i in range(len(data)):
        row = Recipe(
            name = str(data.iloc[i][0]),
            category = str(data.iloc[i][1]),
            country = str(data.iloc[i][2]),
            photo = str(data.iloc[i][3]),
            time = str(data.iloc[i][4]),
            ingredients = str(data.iloc[i][5]),
            text = str(data.iloc[i][6]),
            author_id = 1
        )
        db.session.add(row)
    db.session.commit()

    return 'Данные успешно записаны в базу данных!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
