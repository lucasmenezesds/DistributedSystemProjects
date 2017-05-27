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

# Make socket
transport = TSocket.TSocket('localhost', 3030)

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
# client.ping()
# print('ping()')


# Operation
print("Listing Neighbours Vertexes from vertex %s"%(vertex))
print(client.listNeighbourVertexes(vertex))
print("\n\n")



# Close!
print("Closing Connection..\n")
transport.close()
print("Connection is closed!\n")
print("Bye!\n")
