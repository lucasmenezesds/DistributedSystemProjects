#!/usr/bin/env python

MOVIE, PERSON, CASTING = 1, 2, 3

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


def filter_vertexes(vertexes, obj_type):
    return [vertex for vertex in neighbours if vertex.color == obj_type]


def get_watched_movies(person_list):
    ''' INPUT: person list
        OUTPUT: movies list
        Returns all wached movies in by all people
    '''
    results = set()
    for person_id in person_list:
        watched = filter_vertexes(client.listNeighbourVertexes(person_id), MOVIE)
        print watched
        results |= watched

    return results


def find_nonsense(p, q):
    ''' INPUT: 2 persons p and q
        OUTPUT:
    '''
    pass


open_thrift()
close_thrift()