
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from DBclasses import Users, UserAccount, Recipe, db
import re
import ast


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'bruno'
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

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

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        with app.app_context():
            try:
                user = Users.query.filter_by(username=username, password=password).first()
                if user:
                    login_user(user)
                    return redirect('/user', user.id)
                else:
                    return render_template("login.html", error="Неправильный логин или пароль")
            except:
                return "ERROR"

    else:
        return render_template("login.html")


@app.route('/create_account', methods=['POST', 'GET'])
def create_account():
    if request.method == "POST":
        user = current_user
        name = request.form['name']
        surname = request.form['surname']
        date = request.form['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        with app.app_context():
            user_acc = UserAccount(name=name, surname=surname, date=date_obj, User_id=user.id)
            db.session.add(user_acc)
            db.session.commit()
            return redirect(url_for('user', user_id=user.id))
    else:
        return render_template("create_account.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        user = Users.query.filter_by(username=username).first()
        if not username or not password:
            return render_template("register.html", error="Вы не ввели логин или пароль")
        if user:
            return render_template("register.html", error="Такой пользователь уже существует")
        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('create_account'))
    else:
        return render_template("register.html")


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    AllUsers = Users.query.all()
    acc = None
    if user.is_authenticated and user.acc is not None:
        acc = user.acc.first()
    recipes = Recipe.query.all()
    recipe_dict = {key: UserAccount.query.filter_by(user_id=key.author_id).first() for key in recipes}

    return render_template("index.html")



@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    keyword = None
    country = None
    category = None
    calories_low = None
    calories_up = None
    time_low = None
    time_up = None
    fast_sort = None
    recipes = Recipe.query
    if request.method == "POST":
        fast_sort = request.form.get('fast_sort')
        keyword = request.form['keyword']
        country = request.form.get('country')
        category = request.form.get('category')
    else:
        country = request.args.get('country')
        category = request.args.get('category')
    if fast_sort == '1':
        recipes = recipes.order_by(db.desc(Recipe.likes))
    elif fast_sort=='2':
        recipes = recipes.order_by(db.desc(Recipe.date_column))
    else:
        recipes = recipes.order_by(db.asc(Recipe.date_column))
    if not (keyword == "Ключевое слово") and keyword:
        recipes = recipes.filter(Recipe.name.like(f'%{keyword}%'))
    if not (country == "Страна") and country:
        recipes = recipes.filter_by(country=country)
    if not (category == "Категория") and category:
        recipes = recipes.filter_by(category=category)
    recipes = recipes.all()
    return render_template('recipes.html', recipes=recipes)
@app.route('/recipe_details/<int:id>')
def recipe_details(id):
    recipe = Recipe.query.filter_by(id=id).first()
    text = [x for x in recipe.text[1:-1].split("', '")]
    text[-1] = text[-1][:-1]
    text[0] = text[0][1:]
    lst = ast.literal_eval(recipe.ingredients)
    ingr = {}
    for item in lst:
        ingr[item[0]] = item[1]
    return render_template('recipe_details.html', recipe=recipe, ingr=ingr, text=text)


@app.route('/user')
@login_required
def user():
    user = current_user
    acc = user.acc.first()
    return render_template('user.html', acc=acc)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
