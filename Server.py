import pickle
import select
import socket as s
from threading import Thread

import sys


class Server:

	def __init__(self):
		self.Clients = []
		self.HOST = ""
		self.PORT = 2345

		self.server = s.socket(s.AF_INET, s.SOCK_STREAM)
		self.server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
		self.server.setblocking(0)

		self.bind(self.server, self.HOST, self.PORT)

		self.server.listen(4)

		self.inputs = [self.server]
		self.outputs = []

		while True:
			if self.inputs:
				readable, writable, errors = select.select(self.inputs, self.outputs, self.inputs)

				for socket in readable:
					if socket is self.server:
						conn, addr = socket.accept()
						conn.setblocking(0)
						self.Clients.append([conn, addr])
						print("Client connected")
			for client in self.Clients:
				print(client)
				receive = select.select([client[0]], [], [], 0.001)
				message = client[0].recv(6969)
				message = pickle.loads(message)
				print(message)

	def bind(self, sock, host, port):
		try:
			sock.bind((host, port))
		except s.error as msg:
			print("Bind failed with %s" % (msg))
			sys.exit()


if __name__ == "__main__":
	Server()