__author__ = 'wille'
from flask import Flask, jsonify, session
import random
from database_helper import *
from login_handler import *

app = Flask(__name__)

def change_password(token, old_password, new_password):
    if in_session(token):
        email = session[token]
        if check_email_password_db(email, old_password):
            if validate_password(new_password):
                update_password_db(email, new_password)
                return jsonify(success=True, message="Password changed!")
            else:
                return jsonify(success=False, message="New password must contain at least 6 characters!")
        else:
            return jsonify(success=False, message="Incorrect old password!")
    else:
        return jsonify(success=False, message="You are not logged in!")


def get_user_data_by_token(token):
    email = session[token]
    return get_user_data_by_email(token, email)


def get_user_data_by_email(token, email):
    if in_session(token):
        user_data = get_user_data_db(email)

        user_info = {'email': user_data[0],
                                  'firstname': user_data[2],
                                  'familyname': user_data[3],
                                  'gender': user_data[4],
                                  'city': user_data[5],
                                  'country': user_data[6]}

        return jsonify(success=True, message="User data successfully retrieved.", data=user_info)
    else:
        return jsonify(success=False, message="You are not logged in!")


def post_message(token, message, to_email):
    from_email = session[token]
    if in_session(token):
        if check_email_db(to_email):
            save_message_db(to_email, from_email, message)
            return jsonify(success=True, message="Message successfully posted.")
        else:
            return jsonify(success=False, message="Recipient does not exist!")
    else:
        return jsonify(success=False, message="You are not logged in!")


def get_user_messages_by_token(token):
    email = session[token]
    return get_user_messages_by_email(token, email)


def get_user_messages_by_email(token, email):
    if in_session(token):
        user_messages = get_messages_db(email)
       # i = 0
        #while (i < len(user_messages)):
        print user_messages[1]
        user_wall = {'writer': user_messages[1],
                    'message': user_messages[1]}
            #i = i+1
        return jsonify(success=True, message="User messages successfully retrieved.", data=user_wall)
    else:
        return jsonify(success=False, message="You are not logged in!")