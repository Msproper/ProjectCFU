
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


class UserAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    date = db.Column(db.DateTime)
    User_id = db.Column(db.Integer, db.ForeignKey('users.id'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        with app.app_context():
            try:
                user = Users.query.filter_by(username=username, password=password).first()
                if user:
                    return redirect('/')
                else:
                    return render_template("login.html", error="Неправильный логин или пароль")
            except:
                return "ERROR"

    else:
        return render_template("login.html")


# @app.route('/update_account', methods=['POST', 'GET'])
# def update_account():
#     if request.method == "POST":
#
#     else:
#         return render_template("update_account")

@app.route('/create_account/<int:user_id>', methods=['POST', 'GET'])
def create_account(user_id):
    if request.method == "POST":
        print(user_id)
        name = request.form['name']
        surname = request.form['surname']
        date = request.form['date']
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        with app.app_context():
            user_acc = UserAccount(name=name, surname=surname, date=date_obj, User_id=user_id)
            db.session.add(user_acc)
            db.session.commit()
            return redirect(url_for('user', user_id=user_id))
    else:
        return render_template("create_account.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        user = Users(username=username, password=password)
        print(user.id, user.username, user.password)
        try:
            db.session.add(user)
            db.session.commit()
            print(user.id)
            return redirect(url_for('create_account', user_id=user.id))
        except:
            return "error"
    else:
        return render_template("register.html")

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/user/<int:user_id>')
def user(user_id):
    user = UserAccount.query.filter_by(User_id=user_id).first()
    print("Имя пользователя:", user.surname)
    print("Весь пользователь:", user)
    return render_template("user.html", user=user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
