from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask import render_template


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@app.route("/")
def get_contestant():
    return render_template("contestant.html")


@socketio.on("message")
def handleMessage(msg):
    print("message "+msg)
    send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
