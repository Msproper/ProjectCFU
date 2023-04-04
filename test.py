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
    urls = Recipe.query.all()

    if not os.path.exists("img"):
        os.makedirs("img")

    # открываем файл для записи бинарных данных
    for i, url in enumerate(urls):
        response = requests.get(url.photo, timeout=(10, 30))
        with open(f"img/{i}.webp", "wb") as f:
            f.write(response.content)
        time.sleep(0.1)
    return "Ok"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)