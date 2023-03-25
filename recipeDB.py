from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
app = Flask(__name__)



# Добавление пользователя в базу данных
def add_user(username, password):
    conn = sql.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    cur.close()
    conn.close()

# Основная страница сайта
@app.route('/')
def index():
    return render_template('index.html')

# Страница входа пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка наличия пользователя в базе данных
        conn = sql.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return render_template('register.html')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Страница регистрации пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка наличия пользователя в базе данных
        conn = sql.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        if user:
            cur.close()
            conn.close()
            return render_template('register.html', error='Username already exists')
        else:
            cur.close()
            conn.close()
            # Добавление пользователя в базу данных
            add_user(username, password)
            return redirect(url_for('welcome'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('about.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
