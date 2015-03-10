__author__ = 'wille'
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import sqlite3
from login_handler import *
import database_helper
from session_functions import *

app = Flask(__name__)

app.secret_key = "jullan"


@app.route("/init_db")
def server_setup_db():
    database_helper.init_db()
    return "Database is GAME ON!"


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/sign_in", methods=['POST'])
def server_sign_in():
    email = request.form['email']
    password = request.form['password']
    return sign_in(email, password)


@app.route("/sign_up", methods=['POST'])
def server_sign_up():
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    familyname = request.form['familyname']
    gender = request.form['gender']
    city = request.form['city']
    country = request.form['country']
    message = sign_up(email, password, firstname, familyname, gender, city, country)
    return message


@app.route("/sign_out", methods=['POST'])
def server_sign_out():
    token = request.form['token']
    return sign_out(token)


@app.route("/change_password", methods=['POST'])
def server_change_password():
    token = request.form['token']
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    return change_password(token, old_password, new_password)


@app.route("/get_user_data_by_token", methods=['POST'])
def server_get_user_data_by_token():
    token = request.form['token']
    return get_user_data_by_token(token)


@app.route("/get_user_data_by_email", methods=['POST'])
def server_get_user_data_by_email():
    token = request.form['token']
    email = request.form['email']
    return get_user_data_by_email(token, email)


@app.route("/get_user_messages_by_token", methods=['POST'])
def server_get_user_messages_by_token():
    token = request.form['token']
    return get_user_messages_by_token(token)


@app.route("/get_user_messages_by_email", methods=['POST'])
def server_get_user_messages_by_email():
    token = request.form['token']
    email = request.form['email']
    return get_user_messages_by_email(token, email)


@app.route("/post_message", methods=['POST'])
def server_post_message():
    token = request.form['token']
    message = request.form['message']
    to_email = request.form['to_email']
    return post_message(token, message, to_email)


if __name__ == "__main__":
    app.debug = True
    app.run()