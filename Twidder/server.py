__author__ = 'wille'
from flask import request, Flask
from Twidder import database_helper
from Twidder.session_functions import *
from gevent.wsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
# from Twidder import app



app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = "jullan"

#config
USERNAME = 'Wille'
PASSWORD = 'qwerty'

#added for websocket
socket_connections = []

@app.before_request
def before_request():
    database_helper.get_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()

#end

@app.route("/init_db")
def server_setup_db():
    database_helper.init_db()
    return "Database is GAME ON!"


@app.route("/")
def hello():
    return app.send_static_file("client.html")


@app.route("/sign_in", methods=['POST'])
def server_sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return sign_in(email, password)

    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            ping = ws.receive()
            print ping
            email = get_user_data_by_token(session['token'])['email']
            sign_out_socket(email)
            connection = {"email": email, "connection": ws}
            global socket_connections
            socket_connections.append(connection)
            print socket_connections

        return ""


def sign_out_socket(email):
    global socket_connections
    for conn in socket_connections:
        if conn["email"] == email:
            soc_conn = conn["connection"]
            print soc_conn
            data = {"success" : True, "message": "You have logged in in another browser"}
            remove_socket_connection(email)
            soc_conn.send(json.dumps(data))
            log_out_token = get_token_by_email(email)
            delete_logged_in_user(log_out_token)


def remove_socket_connection(email):
    global socket_connections
    for conn in socket_connections:
        if conn['email'] == email:
            socket_connections.remove(conn)
    print socket_connections


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
        return sign_out(token)


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