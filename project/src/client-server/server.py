#!/usr/bin/python

# https://thrift.apache.org/tutorial/py

import sys
sys.path.append("../libs/")
sys.path.append("../gen-py/")

# from graph import *
import time
import signal

# from rw_lock import *
from server_connector import *
# from dijkstra import *

from graphProject import *
from graphProject.ttypes import *

from threading import Lock, Semaphore
from thrift import Thrift
from thrift.server import TServer, TNonblockingServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from balancer import BalancedDict, id_normal


from pysyncobj import SyncObj #RAFT
from pysyncobj.batteries import ReplLockManager #RAFT
# SyncObj = object


def sleep(val):
    print("Before Sleep!")
    time.sleep(val)
    print("After Sleep!")


def with_lock(orignal_function):
    "Decorator to lock object on the function call"
    lock_obj = 'CRUD'

    def inner_function(self, *args, **kwargs):
        if self.mutual_exclusion.tryAcquire(lock_obj, sync=True):
            orignal_function(self, *args, **kwargs)
            self.mutual_exclusion.release(lock_obj)
        else:
            print "LOCK FAILLLLLLLL"
            THIS_SHOULD_NOT_HAPPEN

    return inner_function


class Handler(object):
    """
        Graph Handler Class
    """
    def __init__(self, conf):
        self.conf = conf
        self.server_id = conf.server_id
        self.raft_id = conf.raft_id
        self.number_of_servers = conf.number_of_servers
        self.server_data_path = "../outputs/server_id_{}/".format(self.server_id)
        self.file_name_vertex = self.server_data_path + "r{}.vertexes.txt".format(self.raft_id)
        self.file_name_edge = self.server_data_path + "r{}.edges.txt".format(self.raft_id)

        self.mutual_exclusion = ReplLockManager(5) # Lock()  # RWLock()

        # Data

        self.loaded_vertexes = {}
        self.loaded_edges = {}

        self.load_data()

        # self.vertexes = BalancedDict()
        # self.edges = BalancedDict()
        self.vertexes = BalancedDict(self, self.loaded_vertexes)
        self.edges = BalancedDict(self, self.loaded_edges)

        # self.edges.handler = self
        # self.vertexes.handler = self


        # super(Handler, self).__init__(*self.raft_ports()) #RAFT
        self.raft = SyncObj(*self.raft_ports(),
                consumers=[ self.vertexes.data, self.edges.data,
                            self.mutual_exclusion])

    def __del__(self):
        print "Saving data on disk (from __del__)"
        self.save_data()
        sys.exit()


    def ping(self):
        print('ping(Someone connected here!)')


    def shutdown(self):
        for server_id in range(1, self.number_of_servers):
            if server_id != self.server_id:
                with ServerConnector(server_id, self.vertexes.get_thrift_port(server_id)) as client:
                    client.shutdown()






    # def acquire_object_for_use(self):
    #     self.mutual_exclusion.acquire()

    # def release_object_of_use(self):
    #     self.mutual_exclusion.release()


    ##############
    # DATA GRAPH #
    ##############

    def save_vertexes(self):
        import csv
        with open(self.file_name_vertex, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            for vertex in self.vertexes.values():
                print("Saving vertex:", vertex)
                writer.writerow([
                    vertex.vertexID,
                    vertex.color,
                    vertex.description,
                    vertex.weight,
                ])

    def save_edges(self):
        import csv
        with open(self.file_name_edge, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            for edge in self.edges.values():
                print("Saving edge:", edge)
                writer.writerow([
                    edge.vertexA,
                    edge.vertexB,
                    edge.weight,
                    edge.flag,
                    edge.description,
                ])

    def load_vertexes(self):
        vertexes = {}
        import csv
        with open(self.file_name_vertex) as f:
            reader = csv.reader(f)
            for vertexID, color, description, weight in reader:
                vertex = Vertex( int(vertexID), int(color), description, float(weight))
                print("Loading vertex:", vertex)
                vertexes[int(vertexID)] = vertex
                self.loaded_vertexes[int(vertexID)] = vertex
                # self.vertexes[int(vertexID)] = vertex




    def load_edges(self):
        import csv
        with open(self.file_name_edge) as f:
            reader = csv.reader(f)
            for vertexA, vertexB, weight, flag, description in reader:
                edge = Edge(int(vertexA), int(vertexB), float(weight), int(flag), description)
                print("Loading edge:", edge)
                # self.edges[(int(vertexA), int(vertexB))] = edge
                self.loaded_edges[(int(vertexA), int(vertexB))] = edge

    def save_data(self):
        print "SAVING DATA........"
        self.save_vertexes()
        self.save_edges()
        print "CHECKPOINT"


    def load_data(self):
        print "LOADING DATA ...",
        try:
            self.load_vertexes()
            self.load_edges()
            print "OK"
        except IOError:
            pass    # just leave the database empty


    ####################
    # AUXILIAR METHODS #
    ####################

    # GRAPH'S DATA #

    def check_valid_data(self, data_array):
        for elem in data_array:
            if (elem == "" or elem == None):
                raise InvalidObject("Some value of edge or vertex is invalid, check the files please!")

    def update_vertexes_list_of_edges(self, server_id, recieved_vertex=False):
        if (recieved_vertex == False):
            for vertex  in self.get_vertex_list(server_id):
                for edge in self.get_edges_list(server_id):
                    if (not self.check_vertex_edges(vertex, edge.edgeID)):
                        if ((vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB)):
                            if (not self.check_vertex_edges(vertex, edge)):
                                vertex.edges.append(edge)
        else:
            for edge in self.get_edges_list(server_id):
                if (vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB):
                    vertex.edges.append(edge)


    ###############
    # VERTEX CRUD #
    ###############

    @with_lock
    def createVertex(self, vertexID, color, description, weight):
        print "createVertex:", vertexID, color, description, weight
        # sleep(5)
        if vertexID in self.vertexes:
            raise InvalidObject("Vertex already exist!")

        self.vertexes[vertexID] = Vertex(vertexID, color, description, weight)

    @with_lock
    def readVertex(self, vertexID):
        print "readVertex:", vertexID
        if vertexID not in self.vertexes:
            raise InvalidObject("READ: Vertex doesn't exist!")
        return self.vertexes[vertexID]

    @with_lock
    def updateVertex(self, vertexID, color, description, weight):
        if vertexID not in self.vertexes:
            raise InvalidObject("UPDATE: Vertex doesn't exist!")

        self.vertexes[vertexID] = Vertex(vertexID, color, description, weight)

    @with_lock
    def deleteVertex(self, vertexID):
        if vertexID not in self.vertexes:
            raise InvalidObject("DELETE: Vertex doesn't exist!")

        for edge in self.listEdges(vertexID):
            self.deleteEdge(edge.VertexA, edge.VertexB)

        del self.vertexes[vertexID]

    def hasVertex(self, vertexID):
        return vertexID in self.vertexes.data


    #############
    # EDGE CRUD #
    #############
    '''
    struct Edge
    1: required i64 edgeID,
    2: required i64 vertexA,
    3: required i64 vertexB,
    4: required double weight,
    5: required i32 flag,
    6: required string description
    '''

    @with_lock
    def createEdge(self, vertexA, vertexB, weight, flag, description):
        print "createEdge: %r, %r, %r, %r, %r" % (vertexA, vertexB, weight, flag, description)
        if  vertexA not in self.vertexes or vertexB not in self.vertexes:
            raise InvalidObject("One of the Vertex doesn't exist!")

        if  (vertexA, vertexB) in self.edges:
            raise InvalidObject("Edge already exist!")

        self.edges[(vertexA, vertexB)] = \
            Edge(vertexA, vertexB, weight, flag, description)

    @with_lock
    def readEdge(self, vertexA, vertexB):
        print "createEdge:", vertexA, vertexB
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("READ: Edge doesn't exist!")

        return self.edges[(vertexA, vertexB)]

    @with_lock
    def updateEdge(self, vertexA, vertexB, weight, flag, description):
        print "updateEdge: %r, %r, %r, %r, %r" % (vertexA, vertexB, weight, flag, description)
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("UPDATE: Edge doesn't exist!")

        self.edges[(vertexA, vertexB)] = \
            Edge(vertexA, vertexB, weight, flag, description)

    @with_lock
    def deleteEdge(self, vertexA, vertexB):
        print "deleteEdge:", vertexA, vertexB
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("DELETE: Edge doesn't exist!")

        del self.edges[(vertexA, vertexB)]

    def hasEdge(self, vertexA, vertexB):
        print "hasEdge:", vertexA, vertexB
        (vertexA, vertexB) =  id_normal(vertexA, vertexB)
        return (vertexA, vertexB) in self.edges.data

    #####################
    # OTHERS OPERATIONS #
    #####################

    def listAllVertexes(self, justLocal):
        print "listAllVertexes: justLocal", justLocal
        if justLocal: return self.vertexes.values()

        results = []
        for server_id in range(1, self.number_of_servers):
            if server_id == self.server_id:
                results.extend(self.vertexes.values())
            else:
                with ServerConnector(server_id, self.vertexes.get_thrift_port(server_id)) as client:
                    server_results = client.listAllVertexes(True)
                results.extend(server_results)
        return results

    def listAllEdges(self, justLocal):
        print "listAllEdges: justLocal", justLocal
        if justLocal: return self.edges.values()

        results = []
        for server_id in range(1, self.number_of_servers):
            if server_id == self.server_id:
                results.extend(self.edges.values())
            else:
                with ServerConnector(server_id, self.edges.get_thrift_port(server_id)) as client:
                    server_results = client.listAllEdges(True)
                results.extend(server_results)
        return results

    def listEdges(self, vertexID):
        print "listEdges:", vertexID
        return [ edge   for (vertexA, vertexB), edge in self.edges.items()
                        if vertexID in (vertexA, vertexB) ]


    def listNeighbourVertexes(self, vertexID):
        print "listNeighbourVertexes:", vertexID
        return [ self._getOtherVertex(vertexID, edge)
                    for edge in self.listEdges(vertexID) ]


    @staticmethod
    def _getOtherId(my_id, (id1, id2)):
        return id1 if my_id==id2 else id2

    @staticmethod
    def _getOtherVertex(my_id, edge):
        'Given a VertexID, returns the other one of an edge'
        id1, id2 =  edge.vertexA, edge.vertexB
        other_id = id1 if my_id==id2 else id2
        return self.readVertex(other_id)


    def dijkstra2(self, from_id , to_id):
        print "dijkstra:", from_id , to_id
        edges = [ (e.vertexA, e.vertexB, e.weight) 
                    for e in self.listAllEdges(False) ]

        r = self._dijkstra(edges, from_id, to_id)

        return r



    def _dijkstra(self, edges, f , t):
        print "_dijkstra:", edges, f , t
        from collections import defaultdict
        from heapq import heappop, heappush

        g = defaultdict(list)
        for l,r,c in edges:
            g[l].append((c,r))

        q, seen = [(0,f,())], set()
        while q:
            (cost,v1,path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == t: return (cost, path)

                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost+c, v2, path))

        return float("inf")


    def dijsktra(self, initial_vertex_id): # graph, initial_id
        visited = {initial_vertex_id: 0}
        path = {}

        # nodes = set(graph.nodes)
        nodes = set(self.listAllVertexes(False))

        while nodes:
            min_node = None
            for node in nodes:
                if node.vertexID in visited:
                    if min_node is None:
                        min_node = node
                    elif visited[node.vertexID] < visited[min_node.vertexID]:
                        min_node = node

            if min_node is None:
                break

            nodes.remove(min_node)
            current_weight = visited[min_node.vertexID]

            # for edge in graph.edges[min_node]:
            for edge in self.listEdges(min_node.vertexID):
                edge_ids = edge.vertexA, edge.vertexB

                # weight = current_weight + graph.distance[(min_node, edge)] ####
                weight = current_weight + edge.weight ####

                if edge_ids not in visited or weight < visited[edge_ids]:
                    visited[edge_ids] = weight
                    path[edge_ids] = min_node

        return visited, path

    def calculateDijkstra(self, vertex_id_a, vertex_id_b):
        global visited, path
        # print "calculateDijkstra:", vertex_id_a, vertex_id_b
        # return self.dijkstra(vertex_id_a, vertex_id_b)
        self.r = self.dijsktra(vertex_id_a)
        visited, path = self.r

        from pprint import pprint as pp
        print
        print "Visited:"
        pp(visited)
        print
        print "Path:"
        pp(path)
        # printJUS

        print self.r
        return [Vertex(1, 1,'Vertex 1', 1), Vertex(3, 3,'Vertex 3', 1)]


    def raft_ports(self):
        raft_port_range = self.conf.raft_server_port/100

        raft_servers = ['localhost:%i%i%i'%(raft_port_range, self.conf.server_id, raft_id)
                        for raft_id in range(1, self.conf.number_of_servers+1) ]
        # print raft_servers
        current_server_raft = raft_servers.pop(self.conf.raft_id-1)
        return current_server_raft, raft_servers

#################
# OTHER METHODS #
#################

# def raft_ports(conf):
#     raft_port_range = conf.raft_server_port/100

#     raft_servers = ['localhost:%i%i%i'%(raft_port_range, conf.server_id, raft_id)
#                     for raft_id in range(1, conf.number_of_servers+1) ]
#     # print raft_servers
#     current_server_raft = raft_servers.pop(conf.raft_id-1)
#     return current_server_raft, raft_servers


def load_config(filename='config.json'):
    from json import load

    with open(filename) as f:
        config_dict = load(f)
        return type('config', (object,), config_dict)()


def exit_callback(signum, frame):
    print "exiting from signal", signum
    handler_object.__del__()
    handler_object.__del__ = lambda s : s
    server.close()
    sys.exit(0)

def main(server_id, raft_id):
    global handler_object, server
    conf = load_config()
    conf.server_id = server_id
    conf.raft_id = raft_id
    conf.thrift_server_port = conf.thrift_server_port_base + server_id + (raft_id-1) * conf.number_of_servers
    port = conf.thrift_server_port
    handler_object = Handler(conf)

    processor = GraphOperations.Processor(handler_object)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    signal.signal(signal.SIGINT, exit_callback)
    signal.signal(signal.SIGTERM, exit_callback)
    signal.signal(signal.SIGQUIT, exit_callback)

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    # server = TNonblockingServer.TNonblockingServer(processor, transport, tfactory, pfactory)

    print("Server %s Port: %s" % (server_id, port))
    print("The server is ready to go!")
    try:
        server.serve()
    except KeyboardInterrupt:
        pass


    print("\n\nExiting")


vertexes_path = "../outputs/vertexes"
edges_path = "../outputs/edges"
# def __init__(self, server_id, number_of_servers):

# port = int(sys.argv[1])
# print sys.argv
_, server_id, raft_id = sys.argv

# print file_name
print server_id, raft_id
# print port
# print number_of_servers

if __name__ == '__main__':
    main(int(server_id), int(raft_id))