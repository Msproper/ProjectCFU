
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
                    return redirect(url_for("user"))
                else:
                    return render_template("login.html", error="Неправильный логин или пароль")
            except:
                return "ERROR"

    else:
        return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        email=request.form['email']
        print(username, password, email)
        user = Users.query.filter_by(username=username).first()
        email = Users.query.filter_by(email=email).first()
        if not username or not password:
            return render_template("register.html", error="Вы не ввели логин или пароль")
        if user:
            return render_template("register.html", error="пользователь с таким логином уже существует")
        if email:
            return render_template("register.html", error="Пользователь с такой почтой уже существует")
        if not(password==password2):
            return render_template("register.html", error="Пароли не совпадают")
        new_user = Users(username=username, password=password, email = email)
        new_acc = UserAccount(user_id=user.id)
        db.session.add(new_user)
        db.session.add(new_acc)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('user'))
    else:
        return render_template("register.html")


@app.route('/')
@app.route('/index')
def index():
    user = current_user
    acc = None
    if current_user.is_authenticated:
        acc = user.acc.first()
    recipes = Recipe.query.order_by(db.desc(Recipe.likes)).all()
    recipes = recipes[:5]
    return render_template("index.html", recipes=recipes, acc=acc)



@app.route('/recipes', methods=['POST', 'GET'])
def recipes():
    keyword = None
    country = None
    category = None
    min_time = None
    calories_low = None
    calories_up = None
    max_time = None
    fast_sort = None
    ingredient = None
    recipes = Recipe.query
    user = current_user
    acc = None
    if current_user.is_authenticated:
        acc = user.acc.first()
    if request.method == "POST":
        fast_sort = request.form.get('fast_sort')
        keyword = request.form['keyword']
        country = request.form.get('country')
        category = request.form.get('category')
        min_time = request.form['min_time']
        max_time = request.form['max_time']
    else:
        keyword = request.args.get('keyword')
        ingredient = request.args.get('ingredient')
        calories_low = request.args.get('calories_low')
        calories_up = request.args.get('calories_up')
        min_time = request.args.get('min_time')
        max_time = request.args.get('max_time')
        country = request.args.get('country')
        category = request.args.get('category')
    if fast_sort == '1':
        recipes = recipes.order_by(db.desc(Recipe.likes))
    elif fast_sort == '2':
        recipes = recipes.order_by(db.desc(Recipe.date_column))
    else:
        recipes = recipes.order_by(db.asc(Recipe.date_column))
    if keyword:
        recipes = recipes.filter(Recipe.name.ilike(f'%{keyword}%'))
    if ingredient:
        recipes = recipes.filter(Recipe.ingredients.ilike(f'%{ingredient}%'))
    if not(country=="Кухня") and country:
        recipes = recipes.filter_by(country=country)
    if not (category == "Категория") and category:
        recipes = recipes.filter_by(category=category)
    if min_time:
        recipes = recipes.filter(Recipe.time>min_time)
    if max_time:
        recipes = recipes.filter(Recipe.time<max_time)
    if calories_low:
        recipes = recipes.filter(Recipe.calories > calories_low)
    if calories_up:
        recipes = recipes.filter(Recipe.calories < calories_up)
    recipes = recipes.all()
    return render_template('recipes.html', recipes=recipes, acc=acc)


@app.route('/create/<int:id>', methods=['POST', 'GET'])
@app.route('/create', methods=['POST', 'GET'])
def create(id=None):
    if request.method == "POST":
        if id:
            recipe = Recipe.query.filter_by(id=id).first()
            recipe.name = request.form['name']
            recipe.country = request.form['country']
            recipe.description= request.form['description']
            recipe.text = request.form['text']
            recipe.category = request.form.get('category')
            # recipe.request.form['ingredient_name']
            return redirect(url_for("recipe_details", id=id))
        else:
            return redirect(url_for("recipe_details", id=id))
    else:
        if id:
            recipe = Recipe.query.filter_by(id=id).first()
            return render_template("create.html", recipe=recipe)
        else:
            return render_template("create.html", recipe=None)
@app.route('/recipe_details/<int:id>')
def recipe_details(id):
    recipe = Recipe.query.filter_by(id=id).first()
    text = [x for x in recipe.text[1:-1].split("', '")]
    lst = ast.literal_eval(recipe.ingredients)
    author = recipe.author.acc.first()
    ingr = {}
    user = current_user
    redactable = False
    if user.acc.first() == author:
        redactable = True
    acc = None
    if current_user.is_authenticated:
        acc = user.acc.first()
    for item in lst:
        ingr[item[0]] = item[1]
    return render_template('recipe_details.html', recipe=recipe, ingr=ingr, text=text, acc=acc, author=author, redactable=redactable)

@app.route('/like/<int:id>')
def like(id):
    user = current_user
    if not (current_user.is_authenticated):
        return redirect(url_for("login"))
    else:
        recipe = Recipe.query.filter_by(id=id).first()
        if user.liked_rec:
            list = [int(x) for x in user.liked_rec.split(' ')]
        else:
            list = []
        if id in list:
            list.remove(id)
            recipe.likes -= 1
        else:
            list.append(id)
            recipe.likes += 1
        user.liked_rec = ' '.join(map(str, list))
        db.session.commit()
    return redirect(url_for('recipe_details', id=id))



@app.route('/user')
@login_required
def user():
    user = current_user
    acc = None
    if current_user.is_authenticated:
        acc = user.acc.first()
    recipes = user.recipes.all()
    list = user.liked_rec.split(' ')
    recipes_liked = Recipe.query.filter(Recipe.id.in_(list)).all()
    if len(recipes)>5:
        recipes = recipes[:5]
    else:
        recipes = recipes[:len(recipes)-1]
    return render_template('user.html', acc=acc, recipes=recipes, recipes_liked=recipes_liked)

@app.route('/update', methods=['POST', 'GET'])
@login_required
def update():
    user = current_user
    if request.method == "POST":
        status = request.form['status']
        name = request.form['name']
        surname = request.form['surname']
        acc = user.acc.first()
        if status:
            acc.status = status
        if name:
            acc.name = name
        if surname:
            acc.surname = surname
        db.session.commit()
        return redirect(url_for("user"))
    else:
        user = current_user
        acc = user.acc.first()
        return render_template('update.html', acc=acc)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
