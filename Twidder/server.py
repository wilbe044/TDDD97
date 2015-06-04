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
logged_in_users = []

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
    return app.send_static_file("client.html")

@app.route('/socketapi', methods=['GET'])
def socket_api():
    if request.environ.get('wsgi.websocket'):
        global socket_connections
        ws = request.environ['wsgi.websocket']
        #check that an email do not have two connections
        update_socket_connections()
        email = session['email']
        connection = {"email": email, "connection" : ws}
        socket_connections.append(connection)
        print "Saved ", ws, "to socket connection list"
        print "Some current socket connections"
        i = 1
        #Log current connections
        for conn in socket_connections:
            print "Connection #", i, " Socket: ", conn
            i += 1
        while True:
            #remove connection if it is closed
            if ws.receive() is None:
                for conn in socket_connections:
                    if conn['connection'] == ws:
                        socket_connections.remove(conn)
                print "The connection with the socket has closed"
                return ""
            #Receive and parse JSON object
            # else:
            #     message = ws.receive()
            #     print "message received: ", message
            #     print "websocket: ", ws
            #     message = json.loads(message)
            #     print message["message"]
            #     return ""
    return ""



# Checks if there is a connection with the same email in the connection list
# If conneciton exist the user is logged out and info is sent to client to update data
def update_socket_connections():
    global socket_connections
    email = session['email']
    for conn in socket_connections:
        if conn['email'] == email:
            socket_conn = conn["connection"]
            message = {"action" : "signOutSocket", "message" : "You have logged in in another browser"}
            socket_conn.send(json.dumps(message))
            socket_connections.remove(conn)
    print socket_connections



@app.route("/sign_in", methods=['POST', 'GET'])
def server_sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if check_email_password_db(email, password):
            session['token'] = set_token()
            session['email'] = email
            for e in logged_in_users:
                if e['email'] == email:
                    logged_in_users.remove(e)
                    print logged_in_users
            logged_user = {"email": email, "token" : session['token']}
            logged_in_users.append(logged_user)
            user_count = len(logged_in_users)
            print user_count
            global socket_connections
            message = {"action" : "updateUserCount", "message" : "Updated user count", "count": user_count}
            for conn in socket_connections:
                socket_conn= conn["connection"]
                socket_conn.send(json.dumps(message))
        #add_logged_in_user_db(session['token'], email)
            return jsonify(success=True, message="Successfully logged in!", data=session['token'])
        else:
            return jsonify(success=False, Message="Wrong email or password")


def remove_socket_connection(email):
    global socket_connections
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
            for e in logged_in_users:
                if e['token'] == token:
                    email = e['email']
                    remove_socket_connection(email)
                    logged_in_users.remove(e)
                    user_count = len(logged_in_users)
                    print user_count
                    global socket_connections
                    message = {"action" : "updateUserCount", "message" : "Updated user count", "count": user_count}
                    for conn in socket_connections:
                        socket_conn= conn["connection"]
                        socket_conn.send(json.dumps(message))
                    session.pop(token, None)
                    session.clear()
            return jsonify(success=True, message="You are signed out!")
        else:
            return jsonify(success=False, message="You are not signed in!")


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
        from_email = session['email']
        if 'token' in session:
            if check_email_db(to_email):
                save_message_db(to_email, from_email, message)
                global socket_connections
                message_count = str(count_messages_db())
                message = {"action" : "updateMessages", "message" : "Updated messages", "count": message_count}
                for conn in socket_connections:
                    socket_conn= conn["connection"]
                    socket_conn.send(json.dumps(message))
                print "just sent an update message"
                return jsonify(success=True, message = "Message successfully posted!")
            else:
                return jsonify(success=False, message="Recipient does not exist!")
        else:
            return jsonify(success=False, message="You are not logged in!")


# counts and returns the total number of messages posted on Twidder
@app.route('/get_number_messages', methods=['GET'])
def get_number_messages():
    if request.method == 'GET':
        if 'token' in session:
            message_count = count_messages_db()
            if not message_count:
                return jsonify(success = False, message = "Total number of messages could not be counted")
            else:
                return jsonify(success=True, message = "Total number of messages counted", data = str(message_count))


# counts and returns the total number of online users on Twidder
@app.route('/get_number_users', methods=['GET'])
def get_number_users():
    if request.method == 'GET':
        if 'token' in session:
            user_count = len(logged_in_users)
            print user_count
            return jsonify(success=True, message = "Total number of online users counted", data = str(user_count))


if __name__ == "__main__":
    app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()

    app.run()