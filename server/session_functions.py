__author__ = 'wille'
from flask import Flask, jsonify, session
import random
from database_helper import *
from login_handler import *

app = Flask(__name__)

def change_password(token, old_password, new_password):
    if in_session(token):
        email = session[token]
