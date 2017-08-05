#!/usr/bin/python

# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php

import sys
sys.path.append("../gen-py/")

import heapq

from graphProject import *
from graphProject.ttypes import *

from threading import Lock
from thrift import Thrift
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

##########################
# Settings Objects Class #
##########################

class Edge(object):
    """docstring for Edge"""
    def __init__(self, edgeID, vertexA, vertexB, weight, flag, description=0):
        self.edgeID = edgeID
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.weight = weight
        self.flag = flag
        # Useless attributes just to fit the main object
        self.description = description

class Vertex:
    def __init__(self, vertexID, color=0, description=0, weight=0):
        self.vertexID = vertexID
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None
        # Useless attributes just to fit the main object
        self.color = color
        self.description = description
        self.weight = weight

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.vertexID

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, vertexID):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(vertexID)
        self.vert_dict[vertexID] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0, flag=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        if (flag == 0):
            self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
            self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)
        if (flag == 1):
            self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        if (flag == 2):
            self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous



##################
# Dijkstra Class #
##################


class Dijkstra(object):
    """docstring for Dijkstra"""
    def __init__(self):
        self.graph = Graph()
        self.unvisited_queue = None

    def dijkstra(self, aGraph, start):
        print "Dijkstra's shortest path"
        # Set the distance for the start node to zero
        start.set_distance(0)

        # Put tuple pair into the priority queue
        self.unvisited_queue = [(v.get_distance(),v) for v in aGraph]
        heapq.heapify(self.unvisited_queue)

        while len(self.unvisited_queue):
            # Pops a vertex with the smallest distance
            uv = heapq.heappop(self.unvisited_queue)
            current = uv[1]
            current.set_visited()

            #for next in v.adjacent:
            for next in current.adjacent:
                # if visited, skip
                if next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)

                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)
                    print 'updated : current = %s next = %s new_dist = %s' \
                            %(current.get_id(), next.get_id(), next.get_distance())
                else:
                    print 'not updated : current = %s next = %s new_dist = %s' \
                            %(current.get_id(), next.get_id(), next.get_distance())

            # Rebuild heap
            # 1. Pop every item
            while len(self.unvisited_queue):
                heapq.heappop(self.unvisited_queue)
            # 2. Put all vertices not visited into the queue
            self.unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
            heapq.heapify(self.unvisited_queue)

    def shortest(self, v, path):
        ''' make shortest path from v.previous'''
        if v.previous:
            path.append(v.previous.get_id())
            self.shortest(v.previous, path)
        return

    def parse_data_to_objects(self, servers_graph_dict):
        for vertex in servers_graph_dict["vertexes"]:
            vertexID = vertex.vertexID
            self.graph.add_vertex(vertexID)
        for edge in servers_graph_dict["edges"]:
            v_from = edge.vertexA
            v_to = edge.vertexB
            cost = edge.weight
            flag = edge.flag # if 0, BOTH, if 1 FROM a TO b, if 2, FROM b TO a
            self.graph.add_edge(frm=v_from, to=v_to, cost=cost, flag=flag)


    def get_shortest_path(self, start_vertex, final_vertex):
        # g = Graph()
        print "Getting the shortest path from %s to %s" % (start_vertex, final_vertex)
        print 'Graph data:'
        print "(Vertex A, Vertex B, Cost)"
        for v in self.graph:
            for w in v.get_connections():
                vid = v.get_id()
                wid = w.get_id()
                print '(    %s   ,     %s   , %3d )'  % ( vid, wid, v.get_weight(w))

        self.dijkstra(self.graph, self.graph.get_vertex(start_vertex))

        target = self.graph.get_vertex(final_vertex)
        path = [target.get_id()]
        self.shortest(target, path)
        print 'The shortest path is: %s' %(path[::-1])






if __name__ == '__main__':
    servers_graph_dict = {'vertexes': [Vertex(vertexID=1,color=1,description=1,weight=1), Vertex(vertexID=2,color=1,description=1,weight=1),Vertex(vertexID=3,color=1,description=1,weight=1), Vertex(vertexID=4,color=1,description=1,weight=1),Vertex(vertexID=5,color=1,description=1,weight=1)],'edges': [Edge(edgeID=1, weight=110.0, flag=0, vertexA=1, vertexB=2, description=0),Edge(edgeID=2, weight=80.0, flag=0, vertexA=2, vertexB=3, description=0),Edge(edgeID=3, weight=30.0, flag=0, vertexA=1, vertexB=3, description=0),Edge(edgeID=4, weight=70.0, flag=0, vertexA=2, vertexB=5, description=0),Edge(edgeID=5, weight=20.0, flag=0, vertexA=3, vertexB=5, description=0),Edge(edgeID=6, weight=90.0, flag=0, vertexA=4, vertexB=5, description=0),Edge(edgeID=7, weight=100.0, flag=1, vertexA=4, vertexB=3, description=0)]}

    calc = Dijkstra()
    calc.parse_data_to_objects(servers_graph_dict)
    calc.get_shortest_path(1,4)


    # g = Graph()
    # for vertex in servers_graph_dict["vertexes"]:
    #     vertexID = vertex.vertexID
    #     g.add_vertex(vertexID)
    # for edge in servers_graph_dict["edges"]:
    #     v_from = edge.vertexA
    #     v_to = edge.vertexB
    #     cost = edge.weight
    #     flag = edge.flag # if 0, BOTH, if 1 FROM a TO b, if 2, FROM b TO a
    #     g.add_edge(frm=v_from, to=v_to, cost=cost, flag=flag)

    # print 'Graph data:'
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print '( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w))


    # dijkstra(g, g.get_vertex(1))

    # target = g.get_vertex(4)
    # path = [target.get_id()]
    # shortest(target, path)
    # print 'The shortest path : %s' %(path[::-1])


# [Vertex(vertexID=1,color=1,description=1,weight=1), Vertex(vertexID=2,color=1,description=1,weight=1),Vertex(vertexID=3,color=1,description=1,weight=1), Vertex(vertexID=4,color=1,description=1,weight=1),Vertex(vertexID=5,color=1,description=1,weight=1)],

# 'edges': [Edge(edgeID=1, weight=110.0, flag=0, vertexA=1, vertexB=2, description=0),Edge(edgeID=2, weight=80.0, flag=0, vertexA=2, vertexB=3, description=0),Edge(edgeID=3, weight=30.0, flag=0, vertexA=1, vertexB=3, description=0),Edge(edgeID=4, weight=70.0, flag=0, vertexA=2, vertexB=5, description=0),Edge(edgeID=5, weight=20.0, flag=0, vertexA=3, vertexB=5, description=0),Edge(edgeID=6, weight=90.0, flag=0, vertexA=4, vertexB=5, description=0),Edge(edgeID=7, weight=100.0, flag=0, vertexA=4, vertexB=3, description=0)]


# [Vertex(vertexID=1,color=1,description=1,weight=1), Vertex(vertexID=2,color=1,description=1,weight=1),
# Vertex(vertexID=3,color=1,description=1,weight=1), Vertex(vertexID=4,color=1,description=1,weight=1),
# Vertex(vertexID=5,color=1,description=1,weight=1)],
# 'edges': [
# Edge(edgeID=1, weight=110.0, flag=0, vertexA=1, vertexB=2, description=0),
# Edge(edgeID=2, weight=80.0, flag=0, vertexA=2, vertexB=3, description=0),
# Edge(edgeID=3, weight=30.0, flag=0, vertexA=1, vertexB=3, description=0),
# Edge(edgeID=4, weight=70.0, flag=0, vertexA=2, vertexB=5, description=0),
# Edge(edgeID=5, weight=20.0, flag=0, vertexA=3, vertexB=5, description=0),
# Edge(edgeID=6, weight=90.0, flag=0, vertexA=4, vertexB=5, description=0),
# Edge(edgeID=7, weight=100.0, flag=0, vertexA=4, vertexB=3, description=0)
#  ]
