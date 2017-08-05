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


def populate():
  client.createVertex(0,5,'zero',1.0)
  client.createVertex(1,10,'1 ro',1.1)
  client.createVertex(2,12,'2 ro',1.2)
  client.createVertex(3,13,'3 ro',1.3)
  client.createEdge(0,1,4,0,'01ok')
  client.createEdge(0,2,2,0,'02ok')
  client.createEdge(1,2,3,0,'12ok')
  client.createEdge(0,0,5,0,'00ok')

def dijkstra_populate():
  print "Creating Vertex"
  client.createVertex(1, 1,'Vertex 1', 1)
  client.createVertex(2, 2,'Vertex 2', 1)
  client.createVertex(3, 3,'Vertex 3', 1)
  client.createVertex(4, 4,'Vertex 4', 1)
  client.createVertex(5, 5,'Vertex 5', 1)
  client.createVertex(6, 6,'Vertex 6', 1)


  print "Creating Edges"
  client.createEdge(1, 2,  7, 0, 'Edge')
  client.createEdge(1, 3,  9, 0, 'Edge')
  client.createEdge(1, 6, 14, 0, 'Edge')
  client.createEdge(2, 3, 10, 0, 'Edge')
  client.createEdge(2, 4, 15, 0, 'Edge')
  client.createEdge(3, 4, 11, 0, 'Edge')
  client.createEdge(3, 6,  2, 0, 'Edge')
  client.createEdge(4, 5,  6, 0, 'Edge')
  client.createEdge(5, 6,  9, 0, 'Edge')
  print "Done"



# populate()

# dijkstra_populate()

client.calculateDijkstra(1, 5)

# print("Creating Vertex!\n")
# client.createVertex(932, 5, "vert5", 3.5)
# client.deleteVertex(98)
# read_v = client.readVertex(5)
# print read_v

# client.calculateDijkstra(1, 3)

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
