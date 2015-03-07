__author__ = 'wille'
from sqlite3 import dbapi2 as sqlite3
from flask import g, Flask
import os

"""Used to get the path to the webbogge-folder"""
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
"""Creates the path for the database-file"""
DATABASE = os.path.join(PROJECT_ROOT, 'database.db')

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def check_email_db(email):
    c = get_db()
    result = c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    c.commit()
    return result.fetchone()


def check_email_password_db(email, password):
    c = get_db()
    result = c.execute("SELECT 1 FROM users WHERE email = ? AND password = ?", (email, password))
    c.commit()
    return result.fetchone()


def sign_up_db(email, password, firstname, familyname, gender, city, country):
    c = get_db()
    c.execute("INSERT INTO users(email, password, firstname, familyname, gender, city, country) VALUES (?,?,?,?,?,?,?)",
              (email, password, firstname, familyname, gender, city, country,))
    c.commit()


def update_password_db(email, new_password):
    c = get_db()
    password = c.execute("update users set password = new_password where email = ?", (email))
    return password


def init_db():
    db = get_db()
    with app.open_resource('database.schema', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()