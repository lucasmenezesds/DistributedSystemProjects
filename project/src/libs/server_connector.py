#!/usr/bin/python

# https://thrift.apache.org/tutorial/py

import sys
sys.path.append("../gen-py/")

from graphProject import *
from graphProject.ttypes import *

from threading import Lock
from thrift import Thrift
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class ServerConnector(object):
    """docstring for ServersClient"""
    def __init__(self, port, server_address="localhost"):
        self.__port = port
        self.__server_address = server_address
        self.__transport = None
        self.__protocol = None
        self.__client = None

    def get_port(self):
        return self.__port

    def get_server_address(self):
        return self.__server_address

    def setup_connection(self):
        # Make socket
        self.__transport = TSocket.TSocket(self.get_server_address(), self.get_port())
        # Buffering is critical. Raw sockets are very slow
        self.__transport = TTransport.TBufferedTransport(self.__transport)
        # Wrap in a protocol
        self.__protocol = TBinaryProtocol.TBinaryProtocol(self.__transport)
        # Create a client to use the protocol encoder
        self.__client = GraphOperations.Client(self.__protocol)

    # Connect!
    def connect_to_server(self, server_id):
        print("\n===\nConnecting to server %s..\n===\n" % (server_id))
        self.__transport.open()
        print("Connected!\n")
        self.__client.ping()

    # Close!
    def close_connection(self, server_id):
        print("\n===\nClosing Connection with server %s..\n===\n" % (server_id))
        self.__transport.close()
        print("Connection is closed!\n")

    def ping(self):
        print('ping()')


    def save_graph_data_file(self, tuple_array, server_id=None):
        self.setup_connection()
        self.connect_to_server(server_id)
        for tuple_element in tuple_array:
            data_to_save, data_type = tuple_element
            if data_type == "vertexes":
                print "Creating dataGraphs, saving %s" %(data_type)
                self.__client.createVertexFile(data_to_save, server_id)
                print "Done!\n"
            if data_type == "edges":
                print "Creating dataGraphs, saving %s" %(data_type)
                self.__client.createEdgeFile(data_to_save, server_id)
                print "Done!\n"
        self.close_connection(server_id)

    def get_graph_data(self, server_id):
        graph_data = {}
        self.setup_connection()
        self.connect_to_server(server_id)
        local_vertexes = self.__client.getLocalVertexes()
        local_edges = self.__client.getLocalEdges()
        graph_data["vertexes"] = local_vertexes
        graph_data["edges"] = local_edges
        self.close_connection(server_id)
        print "Got the data, returning it!\n"
        return graph_data
