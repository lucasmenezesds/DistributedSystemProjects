#!/usr/bin/python

import sys
sys.path.append("../gen-py/")

import time
from balancer import *
from rw_lock import *
from data_location import *

from graphProject import *
from graphProject.ttypes import *

from threading import Lock
from thrift import Thrift
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class DataLocation(object):
    """docstring for DataLocation"""
    def __init__(self, data_id, vertexes_dict, edges_dict, list_of_servers=[]):
        self.__data_location_id = data_id
        self.__vertexes_dict = vertexes_dict
        self.__edges_dict = edges_dict
        self.__list_of_servers_without_data_location_file = list_of_servers

    def file_wrote_on_server(self, server_id):
        self.__list_of_servers_without_data_location_file.remove(server_id)

    def get_list_of_servers_without_data_location_file(self):
        return self.__list_of_servers_without_data_location_file

    # Data Location
    def get_data_to_write_on_file(self):
        data_location = {}
        data_location["vertexes"] = [["vertex_id", "server_id_location"]]
        data_location["edges"] = [["edge_id", "server_id_location"]]
        for key, value in self.__vertexes_dict.iteritems():
            vertex_data = [str(key), str(value)]
            data_location["vertexes"].append(vertex_data)

        for key, array_of_values in self.__edges_dict.iteritems():
            for value in array_of_values:
                edge_data = [str(key), str(value)]
                # edge_data = "%s,%s\n" % (key, value)
                data_location["edges"].append(edge_data)

        print data_location
        return data_location


# if __name__ == '__main__':
#     oeoe = DataLocation(1,2,34,[1,2])

#     oeoe.file_wrote_on_server(2)
