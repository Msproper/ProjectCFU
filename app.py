
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

@app.route('/create_account>', methods=['POST', 'GET'])
def update_account():
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        date = request.form['date']
        user = request.form['var']
        with app.app_context():
            try:
                db.session.add(user)
                user_acc = UserAccount(name=name, surname=surname, date=date, User_id=user.id)
                db.session.add(user_acc)
            except:
                return "ERROR"
    else:
        return render_template("create_account.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        user = Users(username=username, password=password)
        return render_template('create_account.html', user=user)
    else:
        return render_template("register.html")

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/user/<int:id>')
def user(id):
    return


@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
