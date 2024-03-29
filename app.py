# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from models import *


# configuration
DATABASE = './data.sqlite3'
DEBUG = False
SECRET_KEY = 'YWRtaW46YWRtaW4='

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, body from publication order by creation_date desc')
    publication = [dict(title=row[0], body=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', publication=publication)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into publication (title , body, creation_date) values ​​(?, ?, sysdate)',
                 [request.form['title'], request.form['body']])
    g.db.commit()
    flash('New publication was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        query = User.select().where(User.username == request.form['username'])
        if query.exists():
            error = 'Invalid username'
        elif query.first().password == request.form['password']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Welcome ! You are now logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/signUp')
def signUp():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Successfully logged out')
    return redirect(url_for('show_entries'))
