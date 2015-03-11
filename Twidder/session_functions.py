__author__ = 'wille'
from flask import Flask, jsonify, session
from Twidder.login_handler import *

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
        if check_email_db(email):
            user_data = get_user_data_db(email)

            user_info = {'email': user_data[0],
                                  'firstname': user_data[2],
                                  'familyname': user_data[3],
                                  'gender': user_data[4],
                                  'city': user_data[5],
                                  'country': user_data[6]}

            return jsonify(success=True, message="User data successfully retrieved.", data=user_info)
        else:
            return jsonify(success=False, message="User does not exist!")
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
        if check_email_db(email):
            user_messages = get_messages_db(email)
            wall_messages = []
            for i in user_messages:
                user_wall = {'id': i[0],
                            'reciever': i[1],
                            'writer': i[2],
                            'message': i[3]}
                wall_messages.append(user_wall)
            return jsonify(success=True, message="User messages successfully retrieved.", data=wall_messages)
        else:
            return jsonify(success=False, message="Nu such user")
    else:
        return jsonify(success=False, message="You are not logged in!")
