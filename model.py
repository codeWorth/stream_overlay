import subprocess
from flask_socketio import emit, join_room, leave_room
import threading
from time import sleep

class Services:
	def __init__(self, serviceObjects):
		self.services = {}
		self.running = False
		for service in serviceObjects:
			self.services[service.name] = {"clients": set(), "service": service, "time_left": service.interval}

	def getService(self, serviceName):
		return self.services[serviceName]["service"]

	def addServiceToClient(self, clientID, serviceName):
		if not(serviceName in self.services):
			print("Client asked for unknown service", service)
		else:
			print("Client", clientID, "registered for", serviceName)
			join_room(serviceName)
			self.services[serviceName]["clients"].add(clientID)

	def removeClient(self, clientID):
		for serviceName in self.services:
			if clientID in self.services[serviceName]["clients"]:
				print("Client", clientID, "deregistered for", serviceName)
				leave_room(serviceName)
				self.services[serviceName]["clients"].remove(clientID)

	def start(self, blocking=False):
		self.running = True
		if blocking:
			self.run()
		else:
			thread = threading.Thread(target=self.run)
			thread.daemon = True
			thread.start()

	def run(self):
		while self.running:	
			t_left_min = min(s["time_left"] for s in self.services.values())
			sleep(t_left_min)

			for serviceInfo in self.services.values():
				serviceInfo["time_left"] -= t_left_min
				if serviceInfo["time_left"] <= 0:
					serviceInfo["time_left"] += serviceInfo["service"].interval
					if len(serviceInfo["clients"]) > 0: # only run services which have at least one client
						print(f'Running service {serviceInfo["service"].name} for clients {serviceInfo["clients"]}')
						serviceInfo["service"].run()

class Service:
	def __init__(self, name, interval):
		self.name = name
		self.interval = interval
		if interval <= 0:
			raise ValueError("Interval is", interval, "but must be greater than zero.")

	def run(self):
		raise NotImplementedError("run not implemented for", self.name)

class SongService(Service):
	name = "song_info"

	def __init__(self, socketio):
		super().__init__(SongService.name, 5)
		self.songName = ""
		self.artist = ""
		self.infoChanged = False
		self.socketio = socketio
		self.updateInfo()

	def run(self):
		self.updateInfo()
		if self.infoChanged:
			self.sendInfo(SongService.name)

	def updateInfo(self):
		info = self.getInfo()
		if len(info) >= 2:
			self.infoChanged = self.songName != info[0] or self.artist != info[1]
			self.songName = info[0]
			self.artist = info[1]

	def sendInfo(self, room):
		self.socketio.emit(self.name, (self.songName, self.artist), room=room)

	def getInfo(self):
		spOut = subprocess.check_output(["powershell.exe", "C:\\Users\\agcum\\Documents\\Code\\GetSongname\\get_songname.ps1"])
		return [s.strip() for s in spOut.decode("utf-8").split("\n") if len(s) > 0]

class RLMMRService(Service):
	name = "rl_mmr"

	def __init__(self):
		super().__init__(RLMMRService.name, 60)
		self.mmr_3s = 0
		self.mmr_2s = 0
		self.mmr_1s = 0

	def run(self):
		pass

class OWSRService(Service):
	name = "ow_sr"

	def __init__(self):
		super().__init__(OWSRService.name, 60)
		self.tank_sr = 0
		self.dps_sr = 0
		self.support_sr = 0

	def run(self):
		pass