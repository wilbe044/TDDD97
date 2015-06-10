from contextlib import closing

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

#connects to the database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv

#gets the database
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#closes the database
def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#checks if an email is in tha database
def check_email_db(email):
    c = get_db()
    result = c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    c.commit()
    return result.fetchone()

#checks if email and password matches in database
def check_email_password_db(email, password):
    c = get_db()
    result = c.execute("SELECT 1 FROM users WHERE email = ? AND password = ?", (email, password))
    c.commit()
    return result.fetchone()

#adds new user to the database
def sign_up_db(email, password, firstname, familyname, gender, city, country):
    c = get_db()
    c.execute("INSERT INTO users(email, password, firstname, familyname, gender, city, country) VALUES (?,?,?,?,?,?,?)",
              (email, password, firstname, familyname, gender, city, country,))
    c.commit()

#uppdates a password in the database
def update_password_db(email, new_password):
    c = get_db()
    c.execute("update users set password = ? where email = ?", (new_password, email,))
    c.commit()

#gets a users data by email from database
def get_user_data_db(email):
    c = get_db()
    user_data = c.execute("select * from users where email = ?", (email,))
    c.commit()
    return user_data.fetchone()

#adds a new message to the database
def save_message_db(to_email, from_email, message):
    c = get_db()
    c.execute("insert into messages(to_email, from_email, message) values (?,?,?)", (to_email, from_email, message,))
    c.commit()

#gets a users message from the database
def get_messages_db(email):
    c = get_db()
    user_messages = c.execute("select * from messages where to_email = ?", (email,))
    c.commit()
    return user_messages.fetchall()


# def get_logged_in_token_by_email_db(email):
#     c = get_db()
#     token = c.execute("select token from logged_in_users where email = ?", (email,))
#     c.commit()
#     return token
#
#
# def get_logged_in_email_by_token_db(token):
#     c = get_db()
#     email = c.execute("select email from logged_in_users where token = ?", (token,))
#     c.commit()
#     print email
#     if email is not None:
#         return email
#     else:
#         return False

#counts the number of messages in the database
def count_messages_db():
    c = get_db()
    message_count = c.execute("SELECT count(*) FROM messages").fetchone()[0]
    c.commit()
    return message_count

#counts number of users in the database
def count_users_db():
    c = get_db()
    user_count = c.execute("SELECT count(*) FROM users").fetchone()[0]
    c.commit()
    return user_count

#initiates the database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('database.schema', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()