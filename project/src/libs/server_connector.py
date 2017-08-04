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
    def __init__(self, server_id, port, server_address="localhost"):
        self.__port = port
        self.__server_address = server_address
        self.__transport = None
        self.__protocol = None
        self.__client = None
        self.server_id = server_id

    def get_port(self):
        return self.__port

    def get_server_address(self):
        return self.__server_address

    def setup_connection(self):
        self.__transport = TSocket.TSocket(self.get_server_address(), self.get_port())
        self.__transport = TTransport.TBufferedTransport(self.__transport)
        self.__protocol = TBinaryProtocol.TBinaryProtocol(self.__transport)
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

    def __enter__(self):
        try:
            self.setup_connection()
            self.connect_to_server(self.server_id)
        except:
            self.__port += 1
            try:
                self.setup_connection()
                self.connect_to_server(self.server_id)
            except:
                self.__port += 1
                self.setup_connection()
                self.connect_to_server(self.server_id)

        return self.__client

    def __exit__(self, exc_type, exc_val, exc_tb):
        print "== CLOSING CONNECTION =="
        self.close_connection(self.server_id)
