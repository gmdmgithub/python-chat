from flask import Flask, render_template
from utils import util
from config import Config
import json
from datetime import datetime

from flask_socketio import SocketIO, emit  # emits data


app = Flask(__name__)


# read config from class/file
app.config.from_object(Config)

socketio = SocketIO(app)


@app.route("/")
def index():
    # return 'hello from sockets!'
    return render_template(
        "./chatPage.html", name="Greg", port_no=util.getEnvVal("PORT")
    )


def messageRecived():
    print("message was received!!!")


@socketio.on("connect")
def test_connect():
    emit("my response", {"data": "Connected"})


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")


@socketio.on("chat_message")
def my_def_message(jsonmessage):
    print("recived my event: " + str(jsonmessage))
    jsonmessage["mess_date"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    socketio.emit("my_response", jsonmessage, callback=messageRecived)


if __name__ == "__main__":
    socketio.run(
        app, port=util.getEnvVal("PORT"), debug=util.str2bool(util.getEnvVal("DEBUG"))
    )
