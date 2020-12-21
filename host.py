from flask import Flask, request
from flask_socketio import SocketIO
from model import *
from flask_socketio import join_room, leave_room

app = Flask(__name__, static_url_path="", static_folder="static")
app.config["SECRET_KEY"] = "gamer_time"
socketio = SocketIO(app)

services = Services([
	SongService(socketio),
	RLMMRService(),
	OWSRService()
])

@socketio.on("register")
def registerClientService(service):
	services.addServiceToClient(request.sid, service)

@socketio.on("disconnect")
def clientDisconnected():
	services.removeClient(request.sid)

@socketio.on(SongService.name)
def songService():
	service = services.getService(SongService.name)
	service.sendInfo(request.sid)

if __name__ == "__main__":
	services.start()
	socketio.run(app, host="localhost")

# import urllib.request
# def getRating():
# 	page = urllib.request.urlopen("https://rocketleague.tracker.network/rocket-league/profile/steam/76561198090366175/mmr?playlist=13")
# 	contents = page.read().decode("utf-8")
# 	index = contents.index(">Rating</div>")
# 	closeIndex = contents[index+13:].find("</div>")
# 	contentDiv = contents[index:closeIndex]
# 	print(contentDiv)
# 	page.close()