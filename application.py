import os
import requests

import datetime

from collections import deque

from flask import Flask, jsonify, session , render_template, request , redirect , flash
from flask_socketio import SocketIO, emit , leave_room , join_room
from flask_session import Session

from helpers import login_required
import database


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SECRET_KEY"] = "my secret key"  

# Initialize Flask-Session
Session(app)

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize database on startup
database.init_database()

active = []

def addmessages(data , isfile):
    room = session["current_room"]
    user = session["username"]
    
    if isfile:
        file_data = {
            'name': data["name"],
            'extension': data["name"].split(".")[-1],
            'type': data["type"],
            'size': data["size"],
            'binary': data["binary"]
        }
        return database.add_message(room, user, file_data=file_data)
    else:
        return database.add_message(room, user, content=data["msg"])

# def createroom(room , storein , isprivate , members=None):
#     storein[room] = []
#     storein[room]["created"] = datetime.datetime.now().strftime("%c")
#     storein[room]["messages"] = []
#     storein[room]["owner"] = session["username"]


@app.route("/signin" , methods=["POST" , "GET"])
def signin():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username and password:
            if database.user_exists(username):
                user = database.get_user(username)
                if password == user["password"]:
                    session["username"] = username
                    return redirect("/")
            else:
                #create user
                if database.create_user(username, password):
                    session["username"] = username
                    return redirect("/")

        flash("username or password is wrong")
        return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route("/")
@login_required
def index():
    rooms = database.get_all_rooms()
    return render_template("index.html" , username = session["username"] , rooms = rooms)

@app.route("/create" , methods=["POST"])
@login_required
def create():
    room = request.form.get("roomname")
    
    if room and not database.room_exists(room):
        print("##################### created", room, "by", session["username"]) 
        if database.create_room(room, session["username"]):
            return redirect("/room/" + room)
        else:
            return "Failed to create room"
    else:
        return "Room already exists ! use a different name"

@app.route("/getMessages/<string:roomname>" , methods=["GET"])
@login_required
def getMessages(roomname):
    if roomname and database.room_exists(roomname):
        messages = database.get_room_messages(roomname)
        print("getmessss =------ " , messages)
        return jsonify("success", messages)
    else:
        return jsonify("error")

@app.route("/room/<string:roomname>" , methods=["POST" , "GET"])
@login_required
def room(roomname):

    if database.room_exists(roomname):
        session["current_room"] = roomname
        messages = database.get_room_messages(roomname)
        return render_template("chat.html" , username = session["username"] , roomname = roomname , messages = messages)
    else:
        return "doest not exist"        

@app.route("/delete/<string:roomname>" , methods=["POST"])
@login_required
def delete(roomname):
    owner = database.get_room_owner(roomname)
    if owner and owner == session["username"]:
        database.delete_room(roomname)
        return "deleted"
    else:
        return "you are not authorized"

@socketio.on("joined")
@login_required
def joined():
    room = session.get("current_room")
    join_room(room)
    print(session["username"] , "joined")
    emit("status" , {"name" : session["username"] , "status":"joined"} , room = room)

@socketio.on("left")
@login_required
def left():
    room = session.get("current_room")
    leave_room(room)
    print(session["username"] , "left")
    emit("status" , {"name" : session["username"] , "status":"left"} , room = room)

@socketio.on("send msg")
@login_required
def msg(data):

    print(session["username"] , "sent" , data)
    room = session.get("current_room")

    isfile = None

    if "name" in data.keys():
        isfile = True
    else:
        isfile = False

    message = addmessages(data , isfile)

    emit("announce msg", message , room = room)

@app.route("/search" , methods=["POST"])
@login_required
def search():
    query = request.form.get("query")
    results = database.search_rooms(query)
    return jsonify({"results":results})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    socketio.run(app, debug=debug, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)