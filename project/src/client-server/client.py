#!/usr/bin/python

# https://thrift.apache.org/tutorial/py

import sys
sys.path.append("../gen-py/")

from graphProject import GraphOperations
from graphProject.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


vertex = 1
vertex2 = 2

# Make socket
transport = TSocket.TSocket('localhost', 3031)

# Buffering is critical. Raw sockets are very slow
transport = TTransport.TBufferedTransport(transport)

# Wrap in a protocol
protocol = TBinaryProtocol.TBinaryProtocol(transport)

# Create a client to use the protocol encoder
client = GraphOperations.Client(protocol)

# Connect!
print("Connecting..\n")
transport.open()
print("Connected!\n")
client.ping()
print('ping()')


# Operation
# client.createGraph()
print("Creating Vertex!\n")
client.createVertex(932, 5, "vert5", 3.5)
client.deleteVertex(98)
read_v = client.readVertex(5)
print read_v
client.saveGraphOnServers()

# client.calculateDijkstra(1, 3)
# client.parseDataFromAllServers()

# print("Listing Neighbours Vertexes from vertex %s" % (vertex))
# print(client.listNeighbourVertexes(vertex))
# print("Creating Vertex!\n")
# client.createVertex(98, 5, "vert5", 3.5)
# # print("Just created the Vertex!\n")
# print("Listing Vertex %s" % (vertex2))
# print(client.listEdges(vertex2))
# print("\n\n")


# Close!
print("Closing Connection..\n")
transport.close()
print("Connection is closed!\n")
print("Bye!\n")
