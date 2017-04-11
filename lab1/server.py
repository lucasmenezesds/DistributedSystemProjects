#!/usr/bin/python

import socket

s = socket.socket()

host = socket.gethostname()
port = 12345


s.bind((host, port))

s.listen(5)

print("The server is up!\n")

while True:
	new_socket_object, new_socket_address = s.accept()
	print 'Got connection from: ', new_socket_address

	recieved_message = new_socket_object.recv(2048)

	if recieved_message:
		print "Message recieved: %s\n" % recieved_message
		client_reply = raw_input("Send a Reply: ")
		new_socket_object.send(client_reply)
		print "The message was sent! Closing connection.."

	new_socket_object.send('\nClosing connection...Thx for connecting\n')
	new_socket_object.close()
	break

print "The server will shut down.. Bye!"

s.close()
