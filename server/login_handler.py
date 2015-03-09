__author__ = 'wille'
from flask import Flask, jsonify, session
import random
from database_helper import *

app = Flask(__name__)


def set_token():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 36):
        token += random.choice(letters)
    return token


def sign_in(email, password):
    if check_email_password_db(email, password):
        token = set_token()
        session[token] = email
        return jsonify(success=True, message="Successfully logged in!", data=token)
    else:
        return jsonify(success=False, Message="Wrong email or password")


def sign_up(email, password, firstname, familyname, gender, city, country):
    if check_email_db(email):
        return jsonify(success=False, message="User already exist!")
    else:
        if validate_password(password):
            try:
                sign_up_db(email, password, firstname, familyname, gender, city, country)
                return jsonify(success=True, message="Successfully created a new user!")
            except:
                return jsonify(success=False, Message="Fail")
        else:
            return jsonify(success=False, message="New password must contain at least 6 characters!")


def sign_out(token):
    if in_session(token):
        session.pop(token, None)
        return jsonify(success=True, message="You are signed out!")
    else:
        return jsonify(success=False, message="You are not logged in!")


def validate_password(password):
    if len(password) < 6:
        return False
    else:
        return True


def in_session(token):
    try:
        if session[token]:
            return True
    except:
        pass
    return False