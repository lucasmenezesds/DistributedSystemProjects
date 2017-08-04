#!/usr/bin/python

from UserDict import IterableUserDict
from server_connector import *

# from pysyncobj import SyncObj, replicated #RAFT
from pysyncobj.batteries import ReplDict
# SyncObj = object
# replicated = lambda f: f


def id_normal(vertexA, vertexB):
    id_normal = (vertexA, vertexB)  if vertexA <= vertexB else (vertexB, vertexA)
    "Printing id_normal", id_normal
    return id_normal


class BalancedDict(IterableUserDict, object):
    handler = None

    # def __init__(self, handler):
    #     self.handler = handler
    #     super(BalancedDict, self).__init__()
    #     # IterableUserDict.__get__(self, IterableUserDict).__init__()
    # #     SyncObj.__get__(self, SyncObj).__init__(*self.handler.raft_ports()) #RAFT

    def __init__(self, handler, data):
        self.handler = handler
        super(BalancedDict, self).__init__()
        self.data = ReplDict()
        raw = self.data.rawData()
        raw.update(data)



    def __getitem__(self, key):
        if self.is_vertex(key):
            print "GET-ITEM - VERTEX"
            server_location = self.calculate_server_location(key)
            if self.handler.server_id == server_location:
                return self.data[key]
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.readVertex(key)

        elif self.is_edge(key):
            print "GET-ITEM - EDGE"
            key = id_normal(*key)
            vertexA, vertexB = key
            server_location = self.calculate_server_location(vertexA)
            if self.handler.server_id == server_location:
                return self.data[key]
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.readEdge(vertexA, vertexB)
        else:
            raise KeyError

    # @replicated
    def __setitem__(self, key, value):
        self.data[key] = value
        if self.is_vertex(key):
            print "SET-ITEM - VERTEX"
            server_location = self.calculate_server_location(key)
            if self.handler.server_id == server_location:
                self.data[key] = value
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    if server_client.hasVertex(value.vertexID):
                        return server_client.updateVertex(**value.__dict__)
                    else:
                        return server_client.createVertex(**value.__dict__)

        elif self.is_edge(key):
            print "SET-ITEM - EDGE"
            key = id_normal(*key)
            vertexA, vertexB = key
            server_location = self.calculate_server_location(vertexA)
            if self.handler.server_id == server_location:
                self.data[key] = value
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    if server_client.hasEdge(*key):
                        return server_client.updateEdge(**value.__dict__)
                    else:
                        return server_client.createEdge(**value.__dict__)

        else:
            raise KeyError

    # @replicated
    def __delitem__(self, key):
        if self.is_vertex(key):
            print "DEL-ITEM - VERTEX"
            server_location = self.calculate_server_location(key)
            if self.handler.server_id == server_location:
                del self.data[key]
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.deleteVertex(key)

        elif self.is_edge(key):
            print "DEL-ITEM - EDGE"
            key = id_normal(*key)
            server_location = self.calculate_server_location(key[0])
            if self.handler.server_id == server_location:
                del self.data[key]
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.deleteEdge(*key)
        else:
            raise KeyError

    def __contains__(self, key):
        if self.is_vertex(key):
            print "balncer contains - VERTEX", key
            server_location = self.calculate_server_location(key)
            if self.handler.server_id == server_location:
                return key in self.data
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.hasVertex(key)

        elif self.is_edge(key):
            print "balncer contains - EDGE"
            key = id_normal(*key)
            vertexA, vertexB = key
            server_location = self.calculate_server_location(vertexA)
            if self.handler.server_id == server_location:
                return key in self.data
            else:
                with ServerConnector(server_location, self.get_thrift_port(server_location)) as server_client:
                    return server_client.hasEdge(vertexA, vertexB)
        else:
            raise KeyError

    def calculate_server_location(self, index):
        s = (hash(index) % self.handler.number_of_servers) + 1
        print "Hashing: INDEX, RESULT", index,'->', s
        return s
        # return (hash(index) % self.handler.number_of_servers) + 1

    def is_vertex(self, key):
        return isinstance(key, int)

    def is_edge(self, key):
        return  isinstance(key, tuple) and len(key) == 2 and \
                isinstance(key[0], int) and isinstance(key[1], int)

    def get_thrift_port(self, server_id):
        return self.handler.conf.thrift_server_port_base + server_id + (self.handler.raft_id-1) * self.handler.number_of_servers

    def id_normal(self, vertexA, vertexB):
        return (vertexA, vertexB)  if vertexA <= vertexB else (vertexB, vertexA)