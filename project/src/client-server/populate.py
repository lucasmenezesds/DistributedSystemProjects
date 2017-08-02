#!/usr/bin/env python

import sys
sys.path.append("../libs/")
sys.path.append("../gen-py/")
from input_parser import get_input

def open_thrift():
    global client, transport
    from graphProject import GraphOperations
    from graphProject.ttypes import *
    from thrift import Thrift
    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol

    transport = TSocket.TSocket('localhost', 3031)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = GraphOperations.Client(protocol)

    print("Connecting..\n")
    transport.open()
    print("Connected!\n")
    client.ping()
    print('ping()')


def close_thrift():
    print("Closing Connection..\n")
    transport.close()
    print("Connection is closed!\n")
    print("Bye!\n")


open_thrift()

vertexes, edges = get_input('../user_input/')

for vertexID, color, description, weight in vertexes:
    print "Creating vertex:", vertexID, color, description, weight
    client.createVertex(vertexID, color, description, weight)

for vertexA, vertexB, weight, flag, description in edges:
    print "Creating edges:", vertexA, vertexB, weight, flag, description
    client.createEdge(vertexA, vertexB, weight, flag, description)


close_thrift()
