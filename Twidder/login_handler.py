__author__ = 'wille'
import random

from flask import Flask, jsonify, session
from Twidder.database_helper import *



app = Flask(__name__)

#sets a token for a user that logs in
def set_token():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 36):
        token += random.choice(letters)
    return token

#signs a user in
def sign_in(email, password):
    if check_email_password_db(email, password):
        session['token'] = set_token()
        session['email'] = email
        return jsonify(success=True, message="Successfully logged in!", data=session['token'])
    else:
        return jsonify(success=False, Message="Wrong email or password")

#signs a user up
def sign_up(email, password, firstname, familyname, gender, city, country):
    if check_email_db(email):
        return jsonify(success=False, message="User already exist!")
    else:
        if validate_password(password):
            if check_form(email, password, firstname, familyname, gender, city, country):
                try:
                    sign_up_db(email, password, firstname, familyname, gender, city, country)
                    return jsonify(success=True, message="Successfully created a new user!")
                except:
                    return jsonify(success=False, Message="Fail")
            else:
                return jsonify(success=False, Message="All fields must contain between 1 - 30 characters")
        else:
            return jsonify(success=False, message="New password must contain at least 6 characters!")

#checks that a password is 6 characters or more
def validate_password(password):
    if len(password) < 6:
        return False
    else:
        return True

#checks that all user information is provided when signing up and that it is not to long
def check_form(email, password, firstname, familyname, gender, city, country):
    if len(email) == 0 or len(email) > 30:
        return False
    elif len(firstname) == 0 or len(firstname) > 30:
            return False
    elif len(familyname) == 0 or len(familyname) > 30:
            return False
    elif len(gender) == 0 or len(gender) > 30:
            return False
    elif len(city) == 0 or len(city) > 30:
            return False
    elif len(country) == 0 or len(country) > 30:
            return False
    else:
        return True

#checks if a token is in session, same as if a user is logged in
def in_session(token):
    try:
        if session['token']:
            return True
    except:
        pass
    return False


