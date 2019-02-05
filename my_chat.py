from flask import Flask, render_template, request, make_response, session
from utils import util
from config import Config
import json
from datetime import datetime

from flask_socketio import SocketIO, emit  # emits data


# class flask.Flask(import_name, static_url_path=None, static_folder='static',
# static_host=None, host_matching=False, subdomain_matching=False,
# template_folder='templates', instance_path=None, instance_relative_config=False, root_path=None)


app = Flask(__name__)


# read config from class/file
app.config.from_object(Config)

socketio = SocketIO(app)


@app.route("/logout")
def logout():
    # remove the username from the session if it is there
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/")
def index():
    # return 'hello from sockets!'
    # lets use make_response to add values
    resp = make_response(
        render_template("./chatPage.html", name="Greg", port_no=util.getEnvVal("PORT"))
    )
    resp.set_cookie("room_id", "3234")
    room_id = request.cookies.get("room_id")
    if "MY_ROOM" in session:
        session_room_id = session["MY_ROOM"]
        print("My room exists", session_room_id)
    else:
        session["MY_ROOM"] = room_id
        print("I am setting session id", room_id)

    return resp


def messageRecived():
    print("message was received!!!")


@socketio.on("connect")
def test_connect():
    print(
        "my response - client connection",
        {"data": "Connected", "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")},
    )
    emit(
        "server_connection",
        {"data": "Connected", "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")},
    )


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected", datetime.utcnow())


@socketio.on("init_conn")
def new_connection(msg):
    print(
        f"New connection from client {msg}",
        datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    )


@socketio.on("chat_message")
def my_def_message(jsonmessage):
    print("session ID", request.sid)
    jsonmessage["mess_date"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    socketio.emit("my_response", jsonmessage, callback=messageRecived)


if __name__ == "__main__":
    socketio.run(
        app, port=util.getEnvVal("PORT"), debug=util.str2bool(util.getEnvVal("DEBUG"))
    )
