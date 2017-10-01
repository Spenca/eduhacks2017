import pickle
import select
import socket as s
from src.player import Player

import sys


class Server:

	def __init__(self):
		self.Clients = []
		self.HOST = ""
		self.PORT = 2345
		self.Players = []

		self.server = s.socket(s.AF_INET, s.SOCK_STREAM)
		self.server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
		self.server.setblocking(0)

		self.bind(self.server, self.HOST, self.PORT)

		self.server.listen(4)

		self.inputs = [self.server]
		self.outputs = []

		while True:
			players = []
			# Listen for new clients
			if self.inputs:
				readable, writable, errors = select.select(self.inputs, self.outputs, self.inputs, 0.001)

				for socket in readable:
					if socket is self.server:
						conn, addr = socket.accept()
						conn.setblocking(0)
						self.Clients.append([conn, addr])
						print("Client connected")
			# Listen for messages from the clients
			for client in self.Clients:
				receive = select.select([client[0]], [], [], 0.001)
				if len(receive[0]) > 0:
					message = client[0].recv(6969)
					message = pickle.loads(message)
					p = Player()
					p.x = message['x']
					p.y = message['y']
					p.t = message['t']
					p.vx = message["vx"]
					p.vy = message["vy"]
					p.vt = message["vt"]
					p.rotation = message["rot"]
					players.append(p)
					print(message)
			# Do some stuff here and calculate what each client should receive
			#TODO
			# Message clients
			for i in range(len(self.Clients)):
				for body in players:
					self.msg(body, self.Clients[i][0])
			print("S_loop")

	def msg(self, message, socket):
		try:
			tuple = {'x': message.x, 'y': message.y, 't': message.t, "vx": message.vx, "vy": message.vy, "vt": message.vt, "rot": message.rotation}
			# Not sure how well this will work with multiple clients
			string = pickle.dumps(tuple, pickle.HIGHEST_PROTOCOL)
			file = socket.makefile("wb")
			file.write(string)
			file.flush()
			print("message sent")
		except socket.error:
			pass
			#print("Messaging failed: %s" % (socket.error))


	def bind(self, sock, host, port):
		try:
			sock.bind((host, port))
		except s.error as msg:
			print("Bind failed with %s" % (msg))
			sys.exit()


if __name__ == "__main__":
	Server()