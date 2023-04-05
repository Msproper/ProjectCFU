
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from DBclasses import Users, UserAccount, Recipe, db
import re
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


@app.route('/recipes/<string:type>', methods=['POST', 'GET'])
@app.route('/recipes', methods=['POST', 'GET'])
def recipes(type=None):
    if request.method == "POST":
        keyword = request.form['keyword']
        country = request.form.get('country')
        category = request.form.get('category')
        recipes = Recipe.query
        recipes=recipes.filter(Recipe.name.like(f'%{keyword}%'))
        if not(country == "Страна"):
            recipes = recipes.filter_by(country=country)
        if not(category == "Категория"):
            recipes = recipes.filter_by(category=category)
        recipes=recipes.all()
        return render_template('recipes.html', recipes=recipes)
    else:
        if type == "breakfast":
            recipes = Recipe.query.filter_by(category="Завтраки").all()
            return render_template('recipes.html', recipes=recipes)
        if type == "soup":
            recipes = Recipe.query.filter_by(category="Супы").all()
            return render_template('recipes.html', recipes=recipes)
        if type == "russian":
            recipes = Recipe.query.filter_by(country="Русская кухня").all()
            return render_template('recipes.html', recipes=recipes)
        if type == "main":
            recipes = Recipe.query.filter_by(category="Основные блюда").all()
            return render_template('recipes.html', recipes=recipes)
        if type == "fast":
            recipes=[]
            timers = Recipe.query.all()
            for timer in timers:
                if (convert_to_minutes(timer.time) < 15):
                    recipes.append(timer)
            return render_template('recipes.html', recipes=recipes)

        else: return "a"



@app.route('/recipes/recipe_details/<int:id>')
def recipe_details(id):
    recipe = Recipe.query.filter_by(id=id).first()
    ingr = [x[1:-1] for x in recipe.ingredients[1:-1].split(', ')]
    text =  recipe.text[1:-1].split("', '")
    text[0]=text[0][1:]
    text[-1] = text[-1][:-1]
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
