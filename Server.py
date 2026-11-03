from flask import Flask, request
from flask_socketio import SocketIO, join_room, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "dominion-family-secret"

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return "Dominion Family Connect Server is Running!"

@socketio.on("join_family")
def join_family(data):
    room = data.get("room")
    username = data.get("username")

    if not room or not username:
        return

    join_room(room)

    emit("member_joined", {
        "username": username,
        "message": username + " joined the family!"
    }, to=room, include_self=False)

    emit("server_message", {
        "message": "Welcome to Dominion Family Connect, " + username
    })

@socketio.on("call_user")
def call_user(data):
    room = data.get("room")

    emit("incoming_call", {
        "from": data.get("username"),
        "call_type": data.get("call_type"),
        "offer": data.get("offer")
    }, to=room, include_self=False)

@socketio.on("answer_call")
def answer_call(data):
    emit("call_answered", data, to=data.get("room"), include_self=False)

@socketio.on("ice_candidate")
def ice_candidate(data):
    emit("ice_candidate", data, to=data.get("room"), include_self=False)

@socketio.on("end_call")
def end_call(data):
    emit("call_ended", data, to=data.get("room"), include_self=False)

if __name__ == "__main__":
    print("Dominion Family Connect Server Started!")
    socketio.run(app, host="0.0.0.0", port=5000)