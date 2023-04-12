import requests
from flask import Flask
from DBclasses import Users, UserAccount, Recipe, db
import os
import time
from urllib.request import urlretrieve
from requests.exceptions import ConnectTimeout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)
# URL фотографии


@app.route('/')
@app.route('/home')
def index():
    urls = Recipe.query.all()
    urls_items = [x.photo_arr.split("', '") for x in urls ]
    for el in urls_items:
        print(el[0][2:])
    if not os.path.exists("img_little2"):
        os.makedirs("img_little2")

    max_retries = 13
    # открываем файл для записи бинарных данных
    for i, url in enumerate(urls_items):
        try:
            retries = 0
            time.sleep(2)
            while retries < max_retries:
                try:
                    response = requests.get(url[-1][:-2], stream=True, timeout=10)
                    if response.status_code == 200:
                        filename = f"arr_{i+1}.webp"
                        filepath = os.path.join("img_little2", filename)
                        urlretrieve(url[-1][:-2], filepath)
                        break
                except ConnectTimeout:
                    retries += 1
        except:
            pass

    return "hello"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)