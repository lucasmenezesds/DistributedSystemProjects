#!/usr/bin/python

import socket


s = socket.socket()

host = socket.gethostname()
port = 12345

s.connect((host, port))

while True:
	message = raw_input("Send the message to the server: ")

	s.send(message)

	reply = s.recv(2048)

	print "The server replied! %s\n" % reply
	break

print "Shutting the client down.."
s.close()
