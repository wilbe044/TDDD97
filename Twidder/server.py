import json

__author__ = 'wille'
from flask import request, Flask
from Twidder import database_helper
from Twidder.session_functions import *
from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
# from Twidder import app


app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
app.debug = True
app.secret_key = "jullan"

#config
USERNAME = 'Wille'
PASSWORD = 'qwerty'

#added for websocket
socket_connections = []

#@app.before_request
#def before_request():
 #   get_db()

#@app.teardown_request
#def teardown_request(exception):
 #   close_db()

#end

@app.route("/init_db")
def server_setup_db():
    print "server init db"
    init_db()
    return "Database is GAME ON!"


@app.route("/")
def hello():
    print "hello"
    return app.send_static_file("client.html")

@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        email = ws.receive()
        print email
        logged_in = True
        if logged_in:
            data = {"success": True, "message": "hello"}
            ws.send(json.dumps(data))
        else:
            ws.send("You are logged in")
    return ""



@app.route("/sign_in", methods=['POST', 'GET'])
def server_sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return sign_in(email, password)

    if request.environ.get('wsgi.websocket'):
        print "sign in wsgi stuff"
        ws = request.environ['wsgi.websocket']
        while True:
            ping = ws.receive()
            print ping
            email = get_logged_in_email_by_token_db(session['token'])
            print email
            sign_out_socket(email)
            connection = {"email": email, "connection": ws}
            global socket_connections
            socket_connections.append(connection)
            print "ovan socket connections"
            print socket_connections

        return ""


def sign_out_socket(email):
    print "i sign out socket"
    global socket_connections
    for conn in socket_connections:
        if conn["email"] == email:
            soc_conn = conn["connection"]
            print soc_conn
            data = {"success" : True, "message": "You have logged in in another browser"}
            remove_socket_connection(email)
            soc_conn.send(json.dumps(data))
            log_out_token = get_logged_in_email_by_token_db(email)
            delete_logged_in_user_db(log_out_token)


def remove_socket_connection(email):
    global socket_connections
    print socket_connections
    for conn in socket_connections:
        if conn['email'] == email:
            socket_connections.remove(conn)
    print socket_connections
    print "socket connection removed"


@app.route("/sign_up", methods=['POST'])
def server_sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        familyname = request.form['familyname']
        gender = request.form['gender']
        city = request.form['city']
        country = request.form['country']
        message = sign_up(email, password, firstname, familyname, gender, city, country)
        return message


@app.route("/sign_out/<token>", methods=['GET'])
def server_sign_out(token):
    if request.method == 'GET':
        if 'token' in session:
            #data = get_user_data_by_token(session['token']).data
            #print data
            #ska fixa sen sa vi kommer at email ovan --------------------------------------------
            #email = session['email']
            email = get_logged_in_email_by_token_db(token)
            remove_socket_connection(email)
            deleted_user = delete_logged_in_user_db(session['token'])
            if deleted_user:
                session.pop(token, None)
                session.clear()
                return jsonify(success=True, message="You are signed out!")
            else:
                return jsonify(success=False, message="You are not logged in!")
        else:
            return jsonify(success=False, message="No such user!")


@app.route("/change_password", methods=['POST'])
def server_change_password():
    if request.method == 'POST':
        token = request.form['token']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        return change_password(token, old_password, new_password)


@app.route("/get_user_data_by_token/<token>", methods=['GET'])
def server_get_user_data_by_token(token):
    if request.method == 'GET':
        return get_user_data_by_token(token)


@app.route("/get_user_data_by_email", methods=['POST'])
def server_get_user_data_by_email():
    if request.method == 'POST':
        token = request.form['token']
        email = request.form['to_email']
        return get_user_data_by_email(token, email)


@app.route("/get_user_messages_by_token/<token>", methods=['GET'])
def server_get_user_messages_by_token(token):
    if request.method == 'GET':
        return get_user_messages_by_token(token)


@app.route("/get_user_messages_by_email", methods=['POST'])
def server_get_user_messages_by_email():
    if request.method == 'POST':
        token = request.form['token']
        email = request.form['email']
        return get_user_messages_by_email(token, email)


@app.route("/post_message", methods=['POST'])
def server_post_message():
    if request.method == 'POST':
        token = request.form['token']
        message = request.form['message']
        to_email = request.form['to_email']
        return post_message(token, message, to_email)


if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    app.run()