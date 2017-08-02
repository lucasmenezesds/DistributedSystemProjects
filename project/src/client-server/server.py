#!/usr/bin/python

# https://thrift.apache.org/tutorial/py

import sys
sys.path.append("../libs/")
sys.path.append("../gen-py/")

# from graph import *
import time
from balancer import *
from rw_lock import *
from server_connector import *
from dijkstra import *

from graphProject import *
from graphProject.ttypes import *

from threading import Lock
from thrift import Thrift
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from UserDict import IterableUserDict

# from pysyncobj import SyncObj, replicated #RAFT
SyncObj = object
# replicated = lambda f: f

def sleep(val):
    print("Before Sleep!")
    time.sleep(val)
    print("After Sleep!")


class BalancedDict(IterableUserDict):
    balancer = None

    def __getitem__(self, key):
        pass
        # to_id = self.balancer.get_server_id(key)

        # if to_id == self.my_id:
        #     return self.data[key]
        # else:
        #     client = self.get_client(to_id)

        #     if isinstance(key, int):    # Vertex id
        #         return client.readVertex(to_id)
        #     else:   # the Edges ids tuple: (id1, id2)
        #         return client.readEdge(*to_id)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]



class Handler(SyncObj):
    """
        Graph Handler Class
    """
    def __init__(self, conf):
        self.conf = conf

        # Data
        self.edges = BalancedDict()
        self.vertexes = BalancedDict()

        self.server_id = conf.server_id
        self.raft_id = conf.raft_id
        # super(Handler, self).__init__(*raft_ports(conf)) #RAFT
        self.__mutual_exclusion = Lock()  # RWLock()
        self.number_of_servers = conf.number_of_servers
        # self.__vertexes_dict = {}
        # # self.__edges_dict = {}
        # self.__server_id = conf.server_id

        # self.__balancer = Balancer(number_of_servers=self.number_of_servers)
        # self.__servers_location = {}
        # self.__servers_graph_dict = {}

        self.server_data_path = "../outputs/server_id_{}/".format(self.server_id)
        self.file_name_vertex = self.server_data_path + "r{}.vertexes.txt".format(self.raft_id)
        self.file_name_edge = self.server_data_path + "r{}.edges.txt".format(self.raft_id)

        self.balancer = Balancer(number_of_servers=self.number_of_servers)
        self.vertexes.balancer = self.balancer
        self.edges.balancer = self.balancer
        self.edges.handler = self

        self.load_data()

    def __del__(self):
        self.save_data()

    # @OK
    def ping(self):
        print('ping(Someone connected here!)')

    # @CON
    def get_file_for_use(self, usage_type):
        if usage_type == "read":
            # self.__mutual_exclusion.reader_acquire()
            self.__mutual_exclusion.acquire()
        if usage_type == "write":
            self.__mutual_exclusion.acquire()
            # self.__mutual_exclusion.writer_acquire()
        if usage_type == "read-write":
            self.__mutual_exclusion.acquire()
            # self.__mutual_exclusion.reader_acquire()
            # self.__mutual_exclusion.writer_acquire()

    # @CON
    def free_file_for_use(self, usage_type):
        if usage_type == "read":
            self.__mutual_exclusion.release()
            # self.__mutual_exclusion.reader_release()
        if usage_type == "write":
            self.__mutual_exclusion.release()
            # self.__mutual_exclusion.writer_release()
        if usage_type == "read-write":
            self.__mutual_exclusion.release()
            # self.__mutual_exclusion.reader_release()
            # self.__mutual_exclusion.writer_release()

    # def append_vertex(self, vertex):
    #     vertex_id = vertex.vertexID
    #     server_id = self.__balancer.get_vertex_location(vertex_id)
    #     if server_id in self.__vertexes_dict:
    #         self.__vertexes_dict[server_id].append(vertex)
    #     else:
    #         self.__vertexes_dict[server_id] = [vertex]

    # # @replicated
    # def append_edge(self, edge):
    #     servers_id = self.__balancer.get_edge_location(edge)
    #     for sv_id in servers_id:
    #         if server_id in self.__edges_dict:
    #             self.__edges_dict[sv_id].append(edge)
    #         else:
    #             self.__edges_dict[sv_id] = [edge]

    # # @replicated
    # def remove_vertex(self, server_id, vertex):
    #     self.__vertexes_dict[server_id].remove(vertex)

    # # @replicated
    # def remove_edge(self, server_id, edge):
    #     self.__edges_dict[server_id].remove(edge)

    # def get_vertex_list(self, server_id):
    #     if (server_id == "vertexes" or server_id == "edges"):
    #         return self.__servers_graph_dict["vertexes"]
    #     else: # if (server_id != "vertexes" or server_id != "edges"):
    #         return self.__vertexes_dict[server_id]

    # def get_edges_list(self, server_id):
    #     # if (server_id != "vertexes" or server_id != "edges"):
    #     if (server_id == "vertexes" or server_id == "edges"):
    #         return self.__servers_graph_dict["edges"]
    #     else:
    #         return self.__edges_dict[server_id]

    # # @replicated
    # def clean_list(self, option="both"):
    #     if (option == "vertex"):
    #         self.__vertexes_dict = {}
    #     elif (option == "edge"):
    #         self.__edges_dict = {}
    #     elif (option == "both"):
    #         self.__vertexes_dict = {}
    #         self.__edges_dict = {}
    #     else:
    #         self.__servers_graph_dict = {}

    ##############
    # DATA GRAPH #
    ##############

    # def loadGraph(self, graph_id=1, vextexes_file_path="../user_input/vertexes.txt", edges_file_path="../user_input/edges.txt"):
    #     # self.clean_list("both")

    #     self.readVertexFile(vextexes_file_path)
    #     self.readEdgesFile(edges_file_path)

    #     list_of_servers_id = self.__vertexes_dict.keys()
    #     for server_id in list_of_servers_id:
    #         self.update_vertexes_list_of_edges(server_id=server_id)

    #     for selected_server_id in list_of_servers_id:
    #         self.save_graph_on_servers(selected_server_id)

    # def parseDataFromAllServers(self):
    #     list_of_servers = self.__balancer.get_list_of_servers()
    #     self.clean_list("graph")
    #     # self.get_servers_location()

    #     self.__servers_graph_dict["vertexes"] = []
    #     self.__servers_graph_dict["edges"] = []

    #     for server_id in list_of_servers:
    #         if (server_id != self.__server_id):
    #             selected_server_port = self.__servers_location[server_id]
    #             server_connector = ServerConnector(selected_server_port)
    #             message = "Getting data from the server %s, port %s" % (server_id, selected_server_port)
    #             print message
    #             graph_dict = server_connector.get_graph_data(server_id)
    #         else:
    #             local_vertexes = self.getLocalVertexes()
    #             local_edges = self.getLocalEdges()
    #             graph_dict["vertexes"] = local_vertexes
    #             graph_dict["edges"] = local_edges
    #         for vertex in graph_dict["vertexes"]:
    #             self.__servers_graph_dict["vertexes"].append(vertex)
    #         for edge in graph_dict["edges"]:
    #             self.__servers_graph_dict["edges"].append(edge)

    #     self.update_vertexes_list_of_edges("vertexes")
        # print self.__servers_graph_dict

    # def getLocalVertexes(self):
    #     local_vextexes_file_path = self.__server_file_path + self.file_name_vertex
    #     self.readVertexFile(local_vextexes_file_path)
    #     return self.__vertexes_dict[self.__server_id]

    # def getLocalEdges(self):
    #     local_edges_file_path = self.__server_file_path + self.file_name_edge
    #     self.readEdgesFile(local_edges_file_path)
    #     return self.__edges_dict[self.__server_id]

    # @property
    # def file_name_edge(self, file_path):
    #     return "r{}.edges.txt".format(self.conf.raft_id)

    # @property
    # def file_name_vertex(self, file_path):
    #     return "r{}.vertexes.txt".format(self.conf.raft_id)

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
        import csv
        with open(self.file_name_vertex) as f:
            reader = csv.reader(f)
            for vertexID, color, description, weight in reader:
                vertex = Vertex( int(vertexID), int(color), description, float(weight))
                print("Loading vertex:", vertex)
                self.vertexes[int(vertexID)] = vertex

    def load_edges(self):
        import csv
        with open(self.file_name_edge) as f:
            reader = csv.reader(f)
            for vertexA, vertexB, weight, flag, description in reader:
                edge = Edge(int(vertexA), int(vertexB), float(weight), int(flag), description)
                print("Loading edge:", edge)
                self.edges[(int(vertexA), int(vertexB))] = edge

    def save_data(self):
        self.save_vertexes()
        self.save_edges()

    def load_data(self):
        try:
            self.load_vertexes()
            self.load_edges()
        except IOError:
            pass    # just leave the database empty

    ################
    # FILE METHODS #
    ################

    # def readFile(self, file_path):
    #     self.get_file_for_use("read")
    #     file = open(file_path, 'r')
    #     file_lines = file.read().splitlines()
    #     self.free_file_for_use("read")
    #     return file_lines

    # def createVertexFile(self, data_to_save, server_id):

    #     file_path = self.__server_file_path + self.file_name_vertex

    #     file_header = "vertexID,color,description,weight\n"
    #     formated_vertex = self.formated_vertexes_list(server_id, data_to_save)
    #     final_string = file_header+formated_vertex
    #     self.get_file_for_use("write")
    #     # sleep(15)
    #     with open(file_path, 'w') as file:
    #         file.write("%s" % (final_string))
    #     self.free_file_for_use("write")
    #     # print "Done!"

    # def createEdgeFile(self, data_to_save, server_id):

    #     file_path = self.__server_file_path + self.file_name_edge

    #     file_header = "edgeID,vertexA,vertexB,weight,flag,description\n"
    #     formated_vertex = self.formated_edges_list(server_id, data_to_save)
    #     final_string = file_header+formated_vertex
    #     self.get_file_for_use("write")
    #     # sleep(15)
    #     with open(file_path, 'w') as file:
    #         file.write("%s" % (final_string))
    #     self.free_file_for_use("write")
    #     # print "Done!"

    # def readVertexFile(self, vextexes_file_path, flag=True):
    #     if flag:
    #         self.clean_list("vertex")
    #     vertexes_lines = self.readFile(vextexes_file_path)
    #     vertexes_lines_header_size = len(vertexes_lines[0].split(","))
    #     vertexes_lines.pop(0)
    #     for line in vertexes_lines:
    #         vertex_data = line.split(",")
    #         if (len(vertex_data) == vertexes_lines_header_size):
    #             self.check_valid_data(vertex_data)

    #             vertex = Vertex(int(vertex_data[0]), int(vertex_data[1]), str(vertex_data[2]), float(vertex_data[3]), [])
    #             self.append_vertex(vertex)
    #         else:
    #             raise InvalidObject("Some vertex data is missing! Check the file please!")

    # def readEdgesFile(self, edges_file_path, flag=True):
    #     if flag:
    #         self.clean_list("edge")
    #     edges_lines = self.readFile(edges_file_path)

    #     edge_lines_header_size = len(edges_lines[0].split(","))
    #     edges_lines.pop(0)

    #     for line in edges_lines:
    #         edge_data = line.split(",")
    #         if (len(edge_data) == edge_lines_header_size):
    #             self.check_valid_data(edge_data)
    #             edge = Edge(int(edge_data[0]), int(edge_data[1]), int(edge_data[2]), float(edge_data[3]), int(edge_data[4]), str(edge_data[5]))
    #             self.append_edge(edge)
    #         else:
    #             raise InvalidObject("Some edge data is missing! Check the file please!")

    # # @replicated
    # def save_graph_on_servers(self, server_id=None):
    #     list_of_servers = []
    #     if server_id is None:
    #         list_of_servers = self.__vertexes_dict.keys()
    #     else:
    #         list_of_servers.append(server_id)

    #     for selected_server_id in list_of_servers:
    #         if (selected_server_id == self.__server_id):
    #             self.createVertexFile(self.__vertexes_dict[selected_server_id], selected_server_id)
    #             self.createEdgeFile(self.__edges_dict[selected_server_id], selected_server_id)

    #         else:
    #             self.get_servers_location()
    #             selected_server_port = self.__servers_location[selected_server_id]
    #             server_connector = ServerConnector(selected_server_port)
    #             message = "I could not save some data, I'm connecting to the server %s, port %s" % (selected_server_id, selected_server_port)
    #             print message
    #             vertex_tuple = (self.__vertexes_dict[selected_server_id], "vertexes")
    #             edge_tuple = (self.__edges_dict[selected_server_id], "edges")
    #             tuple_array = (vertex_tuple, edge_tuple)
    #             server_connector_client = server_connector.save_graph_data_file(tuple_array=tuple_array, server_id=selected_server_id)

    # def saveGraphOnServers(self):
    #     self.save_graph_on_servers()


    #####################
    # FORMATING METHODS #
    #####################

    # def set_string(self, array_of_values):
    #     string = ','.join([str(value) for value in array_of_values])
    #     final_string = string+"\n"

    #     return final_string

    # def formated_vertexes_list(self, server_id, data_to_format=None):
    #     string = ""
    #     if data_to_format is None:
    #         vertexes_list = self.get_vertex_list(server_id)
    #     else:
    #         vertexes_list = data_to_format

    #     for vertex in vertexes_list:
    #         vertex_array = [vertex.vertexID, vertex.color, vertex.description, vertex.weight]
    #         sub_string = self.set_string(vertex_array)
    #         string = string + sub_string
    #     return string

    # def formated_edges_list(self, server_id, data_to_format=None):
    #     string = ""
    #     if data_to_format is None:
    #         edges_list = self.get_edges_list(server_id)
    #     else:
    #         edges_list = data_to_format

    #     for edge in edges_list:
    #         edge_array = [edge.edgeID, edge.vertexA, edge.vertexB, edge.weight, edge.flag, edge.description]
    #         sub_string = self.set_string(edge_array)
    #         string = string + sub_string
    #     return string

    # def formated_data(self, graph_element):
    #     formated_data = None
    #     if (graph_element == "vertex"):
    #         formated_data = self.formated_vertexes_list()

    #     if (graph_element == "edge"):
    #         formated_data = self.formated_edges_list()

    #     return formated_data

    # def format_list(self,array_of_objects, object_type):
    #     string = ""
    #     for selected_object in array_of_objects:
    #         if(object_type == "vertexes"):
    #             object_array = [selected_object.vertexID, selected_object.color, selected_object.description, selected_object.weight]
    #         if(object_type == "edges"):
    #             object_array = [selected_object.edgeID, selected_object.vertexA, selected_object.vertexB, selected_object.weight, selected_object.flag, selected_object.description]

    #         sub_string = self.set_string(object_array)
    #         string = string + sub_string
    #     return string


    # def format_from_array_to_string(self, array):
    #     string = ""
    #     for element in array:
    #         sub_elem1, sub_elem2 = element
    #         sub_string = "%s,%s\n" % (sub_elem1, sub_elem2)
    #         string = string + sub_string
    #     return string


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

    # def check_vertex_edges(self, vertex, edge_recieved):
    #     for edge in vertex.edges:
    #         if (edge.edgeID == edge_recieved):
    #             return True
    #         else:
    #             return False

    # def search_vertex(self, vertex_id):
    #     # self.createGraph()
    #     vertex_return = None
    #     for server_id in self.__vertexes_dict.keys():
    #         for vertex in self.get_vertex_list(server_id):
    #             if (vertex.vertexID == vertex_id):
    #                 vertex_return = vertex
    #     return vertex_return

    # def search_edge(self, edge_id):
    #     # self.createGraph()
    #     edge_return = None
    #     for server_id in self.__vertexes_dict.keys():
    #         for edge in self.get_edges_list(server_id):
    #             if (edge.edgeID == edge_id):
    #                 edge_return = edge
    #     return edge_return

    # def insert_vertex(self, data_array, vertexes_path="../outputs/vertexes"):
    #     self.get_file_for_use("write")
    #     sleep(30)
    #     normalized_string = self.set_string(data_array)
    #     with open(vertexes_path, "a") as file:
    #         file.write(normalized_string)
    #     self.free_file_for_use("write")

    # def insert_edge(self, data_array, edges_path="../outputs/edges"):
    #     self.get_file_for_use("write")
    #     sleep(30)
    #     normalized_string = self.set_string(data_array)
    #     with open(edges_path, "a") as file:
    #         file.write(normalized_string)
    #     self.free_file_for_use("write")

    # GENERAL DATA #

    # def get_servers_location(self):
    #     self.__servers_location = dict(zip(
    #         range(1, self.conf.number_of_servers+1),
    #         range(self.conf.thrift_server_port,
    #         self.conf.thrift_server_port + self.conf.number_of_servers)
    #     ))
    #     print self.__servers_location


    ###############
    # VERTEX CRUD #
    ###############

    def createVertex(self, vertexID, color, description, weight):
        # self.createGraph()
        if vertexID in self.vertexes:
            raise InvalidObject("Vertex already exist!")

        self.vertexes[vertexID] = Vertex(vertexID, color, description, weight)

        # self.append_vertex(new_vertex)
        # self.save_graph_on_servers()
        # self.insert_vertex(data_array)

    def readVertex(self, vertexID):
        # self.createGraph()
        # selected_vertex = None
        # for server_id in self.__vertexes_dict.keys():
        #     # self.update_vertexes_list_of_edges(server_id)
        #     for vertex in self.get_vertex_list(server_id):
        #         if (vertex.vertexID == vertexID):
        #             selected_vertex = vertex
        # return selected_vertex
        if vertexID not in self.vertexes:
            raise InvalidObject("Vertex doesn't exist!")

        return self.vertexes[vertexID]


    def updateVertex(self, vertexID, color, description, weight):
        if vertexID not in self.vertexes:
            raise InvalidObject("Vertex doesn't exist!")

        self.vertexes[vertexID] = Vertex(vertexID, color, description, weight)

        # self.clean_list("vertex")
        # self.createGraph()
        # vertex = self.search_vertex(vertexID)


        # vertex.color = color
        # vertex.description = description
        # vertex.weight = weight
        # self.update_vertexes_list_of_edges(self.__server_id, vertex)
        # self.save_graph_on_servers()

    def deleteVertex(self, vertexID):
        if vertexID not in self.vertexes:
            raise InvalidObject("Vertex doesn't exist!")

        for edge in self.listEdges(vertexID):
            self.deleteEdge(edge.VertexA, edge.VertexB)

        del self.vertexes[vertexID]

        # self.clean_list("both")
        # self.createGraph()
        # vertex = self.search_vertex(vertexID)
        # if (vertex == None):
        #     raise InvalidObject("Vertex do not exist!")
        # for server_id in self.__vertexes_dict.keys():
        #     for vertex in self.get_vertex_list(server_id):
        #         if (vertex.vertexID == vertexID):
        #             for edge in vertex.edges:
        #                 self.remove_edge(server_id, edge)
        #             self.remove_vertex(server_id, vertex)
        # self.save_graph_on_servers()



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

    def createEdge(self, vertexA, vertexB, weight, flag, description):
        if  vertexA not in self.vertexes or vertexB not in self.vertexes:
            raise InvalidObject("One of the Vertex doesn't exist!")

        if  (vertexA, vertexB) in self.edges:
            raise InvalidObject("Edge already exist!")

        self.edges[(vertexA, vertexB)] = \
            Edge(vertexA, vertexB, weight, flag, description)

        # self.createGraph()
        # if (self.search_edge(edgeID) == None):
        #     raise InvalidObject("Edge already exist!")
        # data_array = [edgeID, vertexA, vertexB, weight, flag, description]
        # self.append_edge(data_array)




    def readEdge(self, vertexA, vertexB):
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("Edge doesn't exist!")

        return self.edges[(vertexA, vertexB)]
        # self.createGraph()
        # selected_edge = None
        # for server_id in self.__vertexes_dict.keys():
        #     for edge in self.get_edges_list(server_id):
        #         if (edge.edgeID == edgeID):
        #             selected_edge = edge
        # return selected_edge
        

    def updateEdge(self, vertexA, vertexB, weight, flag, description):
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("Edge doesn't exist!")

        self.edges[(vertexA, vertexB)] = \
            Edge(vertexA, vertexB, weight, flag, description)
        # self.clean_list("edge")
        # # self.createGraph()
        # edge = self.search_edge(edgeID)
        # if (edge == None):
        #     raise InvalidObject("Edge do not exist!")

        # edge.vertexA = vertexA
        # edge.vertexB = vertexB
        # edge.weight = weight
        # edge.flag = flag
        # edge.description = description
        # self.save_graph_on_servers()


    def deleteEdge(self, vertexA, vertexB):
        if (vertexA, vertexB) not in self.edges:
            raise InvalidObject("Edge doesn't exist!")

        del self.edges[(vertexA, vertexB)]

        # self.clean_list("both")
        # # self.createGraph()
        # edge = self.search_edge(edgeID, vertexA, vertexB, weight, flag, description)
        # if (edge == None):
        #     raise InvalidObject("Edge do not exist!")
        # for server_id in self.__vertexes_dict.keys():
        #     for edge in self.get_edges_list(server_id):
        #         if (edge.edgeID == edgeID):
        #             self.remove_edge(server_id, edge)
        # self.save_graph_on_servers()


    #####################
    # OTHERS OPERATIONS #
    #####################

    # def listVertexes(self, vertexA, vertexB):
        # pass
        # self.createGraph()
        # vertexes_list = []
        # for edge in self.get_edges_list(server_id):
        #     if (edge.edgeID == edgeID):
        #         vertexes_list.append(edge)  # edge.vertexA
        #         vertexes_list.append(edge)  # edge.vertexB
        # return vertexes_list

    def listEdges(self, vertexID):
        return [ edge   for (vertexA, vertexB), edge in self.edges.items()
                        if VertexID in (vertexA, vertexB) ]

        # self.createGraph()
        # vertex = self.search_vertex(vertexID)
        # if (vertex == None):
        #     raise InvalidObject("Vertex do not exist!")
        # return vertex.edges


    def listNeighbourVertexes(self, vertexID):
        return [ self._getOtherVertex(VertexID, edge)
                    for edge in self.listEdges(VertexID) ]

        # self.createGraph()
        # neighbour_vertexes_list = []
        # if (self.search_vertex(vertexID) == None):
        #     raise InvalidObject("Vertex do not exist!")
        # for server_id in self.__vertexes_dict.keys():
        #     for edge in self.get_edges_list(server_id):
        #         if (edge.vertexA == vertexID):
        #             neighbour_vertexes_list.append(edge)  # edge.edgeID
        #         elif (edge.vertexB == vertexID):
        #             neighbour_vertexes_list.append(edge)  # edge.edgeID

        # return neighbour_vertexes_list



    @staticmethod
    def _getOtherId(my_id, (id1, id2)):
        return id1 if my_id==id2 else id2

    @staticmethod
    def _getOtherVertex(my_id, edge):
        'Given a VertexID, returns the other one of an edge'
        id1, id2 =  edge.vertexA, edge.vertexB
        other_id = id1 if my_id==id2 else id2
        return self.readVertex(other_id)

    def calculateDijkstra(self, vertex_id_a, vertex_id_b):
        self.parseDataFromAllServers()
        dijkstra = Dijkstra()
        dijkstra.parse_data_to_objects(self.__servers_graph_dict)
        dijkstra.get_shortest_path(vertex_id_a, vertex_id_b)


#################
# OTHER METHODS #
#################



def raft_ports(conf):
    raft_port_range = conf.raft_server_port/100

    raft_servers = ['localhost:%i%i%i'%(raft_port_range, conf.server_id, raft_id)
                    for raft_id in range(1, conf.number_of_servers+1) ]
    # print raft_servers
    current_server_raft = raft_servers.pop(conf.raft_id-1)
    return current_server_raft, raft_servers


def load_config(filename='config.json'):
    from json import load

    with open(filename) as f:
        config_dict = load(f)
        return type('config', (object,), config_dict)()



def main(server_id, raft_id):
    conf = load_config()
    conf.server_id = server_id
    conf.raft_id = raft_id
    conf.thrift_server_port += server_id
    port = conf.thrift_server_port
    handler_object = Handler(conf)

    processor = GraphOperations.Processor(handler_object)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

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

main(int(server_id), int(raft_id))
