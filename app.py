from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask import render_template
from flask_ngrok import run_with_ngrok
from pyngrok import ngrok
from flask_cors import CORS


import question_reader

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app, cors_allowed_origins="*")
audience_votes = [0, 0, 0, 0]
# CORS(app)
# run_with_ngrok(app)


def clear_votes():
    for i in range(0, 4):
        audience_votes[i] = 0


def get_current_votes_status():
    return audience_votes


def add_audience_vote(locked_option_idx):
    # if locked_option_idx not in audience_votes:
    #     audience_votes[locked_option_idx] = 0
    audience_votes[locked_option_idx] += 1


@app.route("/")
@app.route("/contestant")
def get_contestant():
    return render_template("contestant.html")
    # return render_template("inst_test.html")
    # return render_template("graph_test.html")


@app.route("/host")
def get_host():
    return render_template("host.html")


@app.route("/home_start")
def get_home_start():
    return render_template("home_start.html")


@app.route("/spectator")
def get_spectator():
    return render_template("spectator.html")


@app.route("/url_qr")
def get_url_qr():
    return render_template("url_qr.html")


@socketio.on("message")
def handle_message(msg):
    print("message "+str(msg))
    data = msg
    # send(msg, broadcast=True)
    # data = {"q": "one", "0":4}
    send(data, broadcast=True)


@socketio.on('get_file_names')
def get_file_names():
    file_names = question_reader.get_file_names()
    print("Filenames: "+str(file_names))
    # sending back the questions list
    emit("get_file_names", file_names)


@socketio.on('get_question_set')
def get_question_set(file_name):
    questions_set = question_reader.read_question_set_file(file_name)
    print("No of questions: "+str(len(questions_set)))
    # sending back the questions list
    emit("get_question_set", questions_set)


@socketio.on('get_audience_poll_data')
def get_audience_poll_data():
    emit("audience_poll_data", get_current_votes_status(), broadcast=True)


@socketio.on('set_timer')
def set_timer(curr_timer):
    # print(curr_timer)
    # using events not namespace
    # if we don't specify broadcast it just replies back to the client which made this call
    # broadcast true will send to all the connected clients
    emit("curr_timer", curr_timer, broadcast=True)


@socketio.on("set_question")
def set_answer(question_obj):
    print("question : " + str(question_obj))
    clear_votes()
    emit("question", question_obj, broadcast=True)


@socketio.on("set_game_rules")
def set_game_rules(rules_info):
    print("rules info: " + str(rules_info))
    emit("game_rules", rules_info, broadcast=True)


@socketio.on("set_locked_answer")
def set_locked_answer(option_idx):
    print("locked answer: "+str(option_idx))
    emit("locked_answer", option_idx, broadcast=True)


@socketio.on("set_audience_locked_answer")
def set_audience_locked_answer(option_idx):
    print("audience answer: "+str(option_idx))
    add_audience_vote(option_idx)


@socketio.on("set_answer")
def set_answer(answer_obj):
    print("correct answer: " + str(answer_obj))
    emit("answer", answer_obj, broadcast=True)


@socketio.on("set_lifelines")
def set_lifelines(lifelines_obj):
    print("Lifelines: " + str(lifelines_obj))
    emit("lifelines", lifelines_obj, broadcast=True)


@socketio.on("set_5050")
def set_5050(removed_indexes):
    print("removed_indexes: " + str(removed_indexes))
    emit("lifeline_5050", removed_indexes, broadcast=True)


if __name__ == "__main__":
    # to run as sudo, sudo venv/bin/python3.7 app.py
    # if we run at host "0.0.0.0" then we can access the server using it's ip
    # from other machines which are in the same network
    # clear_votes()
    # url = ngrok.connect(5000).public_url
    # print(' * Tunnel URL:', url)
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
    # socketio.run(app, host="0.0.0.0", port=5000)


