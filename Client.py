import socket
import select
import json
import time
import pickle

class Client:

	def __init__(self):
		self.msg = {'x':0, 'y':0, 'r':0, 'v':0, 't':0}
		self.host = "127.0.0.1"
		self.port = 2345
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		except socket.error as msg:
			print ("Failed to create socket: " + str(msg))

		try:
			server_ip = socket.gethostbyname(self.host)
		except socket.gaierror:
			print ("Server could not be resolved")
			raise

		self.sock.connect((server_ip, self.port))

		print("Connected to server")
		self.Loop()

	def Loop(self):
		input = True
		while True:
			if input:
				self.send()
				input = False

			gamestate = select.select([self.sock], [], [], 0.001)
			if gamestate[0]:
				state = self.sock.recv(6969)
			time.sleep(1)

	def send(self):
		try:
			# Not sure how well this will work with multiple clients
			# self.sock.sendall()
			string = pickle.dumps(self.msg, pickle.HIGHEST_PROTOCOL)
			file = self.sock.makefile("wb")
			# file.write("%d\n" % len(string))
			file.write(string)
			file.flush()
			print("message sent")
			# data_string = json.dumps(self.msg)
			# data_string = json.loads(self.msg)
			# self.sock.send(data_string)
		except socket.error:
			print("Messaging failed: %s" % (socket.error))

if __name__ == "__main__":
	Client()