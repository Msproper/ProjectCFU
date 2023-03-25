
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        user = Users(username=username, password=password)
        with app.app_context():
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/')
            except:
                return "ERROR"

    else:
        return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page" + name + " - " + str(id)


@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":

    app.run(debug=True)
