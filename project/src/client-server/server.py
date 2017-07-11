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


def sleep(val):
    print("Before Sleep!")
    time.sleep(val)
    print("After Sleep!")


class Handler(object):
    """
        Graph Handler Class
    """
    def __init__(self, server_id, number_of_servers):
        self.__mutual_exclusion = Lock() # RWLock() 
        self.__vertexes_dict = {}
        self.__edges_dict = {}
        self.__server_id = server_id
        self.number_of_servers = number_of_servers
        self.__server_file_path = "../outputs/server_id_%s/" % (self.__server_id)
        self.__balancer = Balancer(number_of_servers=self.number_of_servers)
        self.__servers_location = {}
        self.__servers_graph_dict = {}

    def ping(self):
        print('ping(Someone connected here!)')

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

    def append_vertex(self, vertex):
        # print "==================================================================================================================="
        # print "==================================================================================================================="
        # print "append vertex"
        # print vertex
        vertex_id = vertex.vertexID
        # print "vertexID"
        # print vertex_id
        server_id = self.__balancer.get_vertex_location(vertex_id)
        if server_id in self.__vertexes_dict:
            self.__vertexes_dict[server_id].append(vertex)
        else:
            self.__vertexes_dict[server_id] = [vertex]
        # print "dict"
        # print self.__vertexes_dict
            # print "no else append_vertex =>"
            # print self.__vertexes_dict
            # print self.__vertexes_dict[server_id]

    def append_edge(self, edge):
        servers_id = self.__balancer.get_edge_location(edge)
        for sv_id in servers_id:
            if server_id in self.__edges_dict:
                self.__edges_dict[sv_id].append(edge)
            else:
                self.__edges_dict[sv_id] = [edge]

    def remove_vertex(self, server_id, vertex):
        self.__vertexes_dict[server_id].remove(vertex)

    def remove_edge(self, server_id, edge):
        self.__edges_dict[server_id].remove(edge)

    def get_vertex_list(self, server_id):
        if (server_id == "vertexes" or server_id == "edges"):
            return self.__servers_graph_dict["vertexes"]
        else: # if (server_id != "vertexes" or server_id != "edges"):
            return self.__vertexes_dict[server_id]


    def get_edges_list(self, server_id):
        # if (server_id != "vertexes" or server_id != "edges"):
        if (server_id == "vertexes" or server_id == "edges"):
            return self.__servers_graph_dict["edges"]
        else:
            return self.__edges_dict[server_id]

    def clean_list(self, option="both"):
        if (option == "vertex"):
            self.__vertexes_dict = {}
        elif (option == "edge"):
            self.__edges_dict = {}
        elif (option == "both"):
            self.__vertexes_dict = {}
            self.__edges_dict = {}
        else:
            self.__servers_graph_dict = {}


    ##############
    # DATA GRAPH #
    ##############

    def createGraph(self, graph_id=1, vextexes_file_path="../user_input/vertexes.txt", edges_file_path="../user_input/edges.txt"):
        # self.clean_list("both")
        # self.__balancer = Balancer(number_of_servers=self.number_of_servers)

        self.readVertexFile(vextexes_file_path)

        self.readEdgesFile(edges_file_path)

        list_of_servers_id = self.__vertexes_dict.keys()
        for server_id in list_of_servers_id:
            self.update_vertexes_list_of_edges(server_id=server_id)

        # print("--------------")
        # print "vertex_dict =>"
        # print self.__vertexes_dict

        # print("--------------")
        # print "__edges_dict =>"
        # print self.__edges_dict

        for selected_server_id in list_of_servers_id:
            self.save_graph_on_servers(selected_server_id)
            # if (selected_server_id == self.__server_id):
            #     self.createVertexFile(self.__vertexes_dict[selected_server_id], selected_server_id)
            #     self.createEdgeFile(self.__edges_dict[selected_server_id], selected_server_id)

            # else:
            #     self.get_servers_location()
            #     selected_server_port = self.__servers_location[selected_server_id]
            #     server_connector = ServerConnector(selected_server_port)
            #     message = "I could not save some data, I'm connecting to the server %s, port %s" % (selected_server_id, selected_server_port)
            #     print message
            #     vertex_tuple = (self.__vertexes_dict[selected_server_id], "vertexes")
            #     edge_tuple = (self.__edges_dict[selected_server_id], "edges")
            #     tuple_array = (vertex_tuple, edge_tuple)
            #     server_connector_client = server_connector.save_graph_data_file(tuple_array=tuple_array, server_id=selected_server_id)

        # graph = Graph(graph_id, self.get_vertex_list, self.get_edges_list)
        # return graph

    def parseDataFromAllServers(self):
        list_of_servers = self.__balancer.get_list_of_servers()
        self.clean_list("graph")
        # self.get_servers_location()

        self.__servers_graph_dict["vertexes"] = []
        self.__servers_graph_dict["edges"] = []

        for server_id in list_of_servers:
            if (server_id != self.__server_id):
                selected_server_port = self.__servers_location[server_id]
                server_connector = ServerConnector(selected_server_port)
                message = "Getting data from the server %s, port %s" % (server_id, selected_server_port)
                print message
                graph_dict = server_connector.get_graph_data(server_id)
            else:
                local_vertexes = self.getLocalVertexes()
                local_edges = self.getLocalEdges()
                graph_dict["vertexes"] = local_vertexes
                graph_dict["edges"] = local_edges
            for vertex in graph_dict["vertexes"]:
                self.__servers_graph_dict["vertexes"].append(vertex)
            for edge in graph_dict["edges"]:
                self.__servers_graph_dict["edges"].append(edge)

        self.update_vertexes_list_of_edges("vertexes")
        # print self.__servers_graph_dict



    def getLocalVertexes(self):
        local_vextexes_file_path = self.__server_file_path + "graphData/vertexes.txt"
        self.readVertexFile(local_vextexes_file_path)
        return self.__vertexes_dict[self.__server_id]

    def getLocalEdges(self):
        local_edges_file_path = self.__server_file_path + "graphData/edges.txt"
        self.readEdgesFile(local_edges_file_path)
        return self.__edges_dict[self.__server_id]



    # def getLocalGraphData(self):
    #     local_vertexes = self.get_local_vertexes()
    #     local_edges = self.get_local_edges()
    #     graph_data_array = [local_vertexes[self.__server_id], local_edges[self.__server_id]]
    #     return graph_data_array



    ################
    # FILE METHODS #
    ################

    def readFile(self, file_path):
        self.get_file_for_use("read")
        file = open(file_path, 'r')
        file_lines = file.read().splitlines()
        self.free_file_for_use("read")
        return file_lines

    def createVertexFile(self, data_to_save, server_id):
        
        # print "================== createVertexFile =================="
        # print "creating the vertex file!"
        # print data_to_save

        server_path = self.__server_file_path
        file_path = server_path + "graphData/vertexes.txt"

        file_header = "vertexID,color,description,weight\n"
        formated_vertex = self.formated_vertexes_list(server_id, data_to_save)
        final_string = file_header+formated_vertex
        self.get_file_for_use("write")
        # sleep(15)
        with open(file_path, 'w') as file:
            file.write("%s" % (final_string))
        self.free_file_for_use("write")
        # print "Done!"

    def createEdgeFile(self, data_to_save, server_id):

        # print "================== createEdgeFile =================="
        # print "creating the edge file!"
        # print data_to_save

        server_path = self.__server_file_path
        file_path = server_path + "graphData/edges.txt"

        file_header = "edgeID,vertexA,vertexB,weight,flag,description\n"
        formated_vertex = self.formated_edges_list(server_id, data_to_save)
        final_string = file_header+formated_vertex
        self.get_file_for_use("write")
        # sleep(15)
        with open(file_path, 'w') as file:
            file.write("%s" % (final_string))
        self.free_file_for_use("write")
        # print "Done!"

    def readVertexFile(self, vextexes_file_path, flag=True):
        if flag:
            self.clean_list("vertex")
        vertexes_lines = self.readFile(vextexes_file_path)
        vertexes_lines_header_size = len(vertexes_lines[0].split(","))
        vertexes_lines.pop(0)
        # print "VERTEXFILE"
        # print vertexes_lines
        for line in vertexes_lines:
            vertex_data = line.split(",")
            if (len(vertex_data) == vertexes_lines_header_size):
                self.check_valid_data(vertex_data)

                vertex = Vertex(int(vertex_data[0]), int(vertex_data[1]), str(vertex_data[2]), float(vertex_data[3]), [])
                self.append_vertex(vertex)
            else:
                raise(InvalidObject("Some vertex data is missing! Check the file please!"))

    def readEdgesFile(self, edges_file_path, flag=True):
        if flag:
            self.clean_list("edge")
        edges_lines = self.readFile(edges_file_path)

        edge_lines_header_size = len(edges_lines[0].split(","))
        edges_lines.pop(0)

        for line in edges_lines:
            edge_data = line.split(",")
            if (len(edge_data) == edge_lines_header_size):
                self.check_valid_data(edge_data)
                edge = Edge(int(edge_data[0]), int(edge_data[1]), int(edge_data[2]), float(edge_data[3]), int(edge_data[4]), str(edge_data[5]))
                self.append_edge(edge)
            else:
                raise(InvalidObject("Some edge data is missing! Check the file please!"))


    def save_graph_on_servers(self, server_id=None):
        # print 'serverid  no savegraph'
        # print server_id
        list_of_servers = []
        if server_id is None:
            # print "entrou"
            list_of_servers = self.__vertexes_dict.keys()
            # print "lista"
            # print list_of_servers
        else:
            list_of_servers.append(server_id)

        for selected_server_id in list_of_servers:
            if (selected_server_id == self.__server_id):
                self.createVertexFile(self.__vertexes_dict[selected_server_id], selected_server_id)
                self.createEdgeFile(self.__edges_dict[selected_server_id], selected_server_id)

            else:
                self.get_servers_location()
                selected_server_port = self.__servers_location[selected_server_id]
                server_connector = ServerConnector(selected_server_port)
                message = "I could not save some data, I'm connecting to the server %s, port %s" % (selected_server_id, selected_server_port)
                print message
                vertex_tuple = (self.__vertexes_dict[selected_server_id], "vertexes")
                edge_tuple = (self.__edges_dict[selected_server_id], "edges")
                tuple_array = (vertex_tuple, edge_tuple)
                server_connector_client = server_connector.save_graph_data_file(tuple_array=tuple_array, server_id=selected_server_id)

    def saveGraphOnServers(self):
        self.save_graph_on_servers()

    # def updateVertexFile(self,vertex, server_id):
    #     server_path = self.__server_file_path
    #     vextexes_file_path = server_path + "graphData/vertexes.txt"
    #     vertexes_lines = self.readFile(vextexes_file_path)
    #     vertexes_lines_header_size = len(vertexes_lines[0].split(","))
    #     vertexes_lines.pop(0)
    #     pass

    #####################
    # FORMATING METHODS #
    #####################

    def set_string(self, array_of_values):
        string = ','.join([str(value) for value in array_of_values])
        final_string = string+"\n"

        return final_string

    def formated_vertexes_list(self, server_id, data_to_format=None):
        string = ""
        if data_to_format is None:
            vertexes_list = self.get_vertex_list(server_id)
        else:
            vertexes_list = data_to_format

        for vertex in vertexes_list:
            vertex_array = [vertex.vertexID, vertex.color, vertex.description, vertex.weight]
            sub_string = self.set_string(vertex_array)
            string = string + sub_string
        return string

    def formated_edges_list(self, server_id, data_to_format=None):
        string = ""
        if data_to_format is None:
            edges_list = self.get_edges_list(server_id)
        else:
            edges_list = data_to_format

        for edge in edges_list:
            edge_array = [edge.edgeID, edge.vertexA, edge.vertexB, edge.weight, edge.flag, edge.description]
            sub_string = self.set_string(edge_array)
            string = string + sub_string
        return string

    def formated_data(self, graph_element):
        formated_data = None
        if (graph_element == "vertex"):
            formated_data = self.formated_vertexes_list()

        if (graph_element == "edge"):
            formated_data = self.formated_edges_list()

        return formated_data

    def format_list(self,array_of_objects, object_type):
        string = ""
        for selected_object in array_of_objects:
            if(object_type == "vertexes"):
                object_array = [selected_object.vertexID, selected_object.color, selected_object.description, selected_object.weight]
            if(object_type == "edges"):
                object_array = [selected_object.edgeID, selected_object.vertexA, selected_object.vertexB, selected_object.weight, selected_object.flag, selected_object.description]

            sub_string = self.set_string(object_array)
            string = string + sub_string
        return string


    def format_from_array_to_string(self, array):
        string = ""
        # print array
        for element in array:
            sub_elem1, sub_elem2 = element
            sub_string = "%s,%s\n" % (sub_elem1, sub_elem2)
            string = string + sub_string
        # print "final string = %s" % (string)
        return string


    ####################
    # AUXILIAR METHODS #
    ####################

    # GRAPH'S DATA #

    def check_valid_data(self, data_array):
        for elem in data_array:
            if (elem == "" or elem == None):
                raise(InvalidObject("Some value of edge or vertex is invalid, check the files please!"))

    def update_vertexes_list_of_edges(self, server_id, recieved_vertex=False):
        if (recieved_vertex == False):
            for vertex  in self.get_vertex_list(server_id):
                # print  "VERTEX dentro do update"
                # print vertex
                for edge in self.get_edges_list(server_id):
                    # print "EDGE DENTRO DO UPDATE"
                    # print edge
                    if (not self.check_vertex_edges(vertex, edge.edgeID)):
                        if ((vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB)):
                            if (not self.check_vertex_edges(vertex, edge)):
                                vertex.edges.append(edge)
        else:
            for edge in self.get_edges_list(server_id):
                if (vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB):
                    vertex.edges.append(edge)

    def check_vertex_edges(self, vertex, edge_recieved):
        for edge in vertex.edges:
            if (edge.edgeID == edge_recieved):
                return True
            else:
                return False

    def search_vertex(self, vertex_id):
        self.createGraph()
        vertex_return = None
        for server_id in self.__vertexes_dict.keys():
            for vertex in self.get_vertex_list(server_id):
                if (vertex.vertexID == vertex_id):
                    vertex_return = vertex
        return vertex_return

    def search_edge(self, edge_id):
        self.createGraph()
        edge_return = None
        for server_id in self.__vertexes_dict.keys():
            for edge in self.get_edges_list(server_id):
                if (edge.edgeID == edge_id):
                    edge_return = edge
        return edge_return

    def insert_vertex(self, data_array, vertexes_path="../outputs/vertexes"):
        self.get_file_for_use("write")
        sleep(30)
        normalized_string = self.set_string(data_array)
        with open(vertexes_path, "a") as file:
            file.write(normalized_string)
        self.free_file_for_use("write")

    def insert_edge(self, data_array, edges_path="../outputs/edges"):
        self.get_file_for_use("write")
        sleep(30)
        normalized_string = self.set_string(data_array)
        with open(edges_path, "a") as file:
            file.write(normalized_string)
        self.free_file_for_use("write")

    # GENERAL DATA #

    def get_servers_location(self):
        path = self.__server_file_path
        server_lines = self.readFile(path + "servers_info.txt")
        server_lines.pop(0)
        server_lines = [elem for elem in server_lines if elem]
        for line in server_lines:
                server_id, port = line.split(',')
                self.__servers_location[int(server_id)] = int(port)


    ###############
    # VERTEX CRUD #
    ###############

    def createVertex(self, vertexID, color, description, weight):
        self.createGraph()
        if (self.search_vertex(vertexID)):
            raise(InvalidObject("Vertex already exist!"))

        new_vertex = Vertex(int(vertexID), int(color), str(description), float(weight))
        # print "recebi new vertex"
        # print new_vertex
        self.append_vertex(new_vertex)
        self.save_graph_on_servers()
        # self.insert_vertex(data_array)

    def readVertex(self, vertexID):
        self.createGraph()
        selected_vertex = None
        for server_id in self.__vertexes_dict.keys():
            # self.update_vertexes_list_of_edges(server_id)
            for vertex in self.get_vertex_list(server_id):
                if (vertex.vertexID == vertexID):
                    selected_vertex = vertex
        return selected_vertex

    def updateVertex(self, vertexID, color=None, description=None, weight=None):
        # self.clean_list("vertex")
        self.createGraph()
        vertex = self.search_vertex(vertexID)
        if (vertex == None):
            raise(InvalidObject("Vertex do not exist!"))

        vertex.color = color
        vertex.description = description
        vertex.weight = weight
        self.update_vertexes_list_of_edges(self.__server_id, vertex)
        self.save_graph_on_servers()
        # self.createVertexFile(vertex)

    def deleteVertex(self, vertexID):
        # self.clean_list("both")
        self.createGraph()
        vertex = self.search_vertex(vertexID)
        if (vertex == None):
            raise(InvalidObject("Vertex do not exist!"))
        for server_id in self.__vertexes_dict.keys():
            for vertex in self.get_vertex_list(server_id):
                if (vertex.vertexID == vertexID):
                    for edge in vertex.edges:
                        self.remove_edge(server_id, edge)
                    self.remove_vertex(server_id, vertex)
        self.save_graph_on_servers()
        # self.get_file_for_use("write")
        # with open("../outputs/vertexes", "w") as file:
        #     file.write(self.formated_vertexes_list())
        # self.save_file(vertex)
        # with open("../outputs/edges", "w") as file:
        #     file.write(self.formated_edges_list())
        # self.free_file_for_use("write")



    #############
    # EDGE CRUD #
    #############

    def createEdge(self, edgeID, vertexA=None, vertexB=None, weight=None, flag=0, description=None):
        self.createGraph()
        if (self.search_edge(edgeID) == None):
            raise(InvalidObject("Edge already exist!"))
        data_array = [edgeID, vertexA, vertexB, weight, flag, description]
        self.append_edge(data_array)

    def readEdge(self, edgeID):
        self.createGraph()
        selected_edge = None
        for server_id in self.__vertexes_dict.keys():
            for edge in self.get_edges_list(server_id):
                if (edge.edgeID == edgeID):
                    selected_edge = edge
        return selected_edge


    def updateEdge(self, edgeID, vertexA=None, vertexB=None, weight=None, flag=0, description=None):
        self.clean_list("edge")
        self.createGraph()
        edge = self.search_edge(edgeID)
        if (edge == None):
            raise(InvalidObject("Edge do not exist!"))

        edge.vertexA = vertexA
        edge.vertexB = vertexB
        edge.weight = weight
        edge.flag = flag
        edge.description = description
        self.save_graph_on_servers()

    def deleteEdge(self, edgeID):
        self.clean_list("both")
        self.createGraph()
        edge = self.search_edge(edgeID, vertexA, vertexB, weight, flag, description)
        if (edge == None):
            raise(InvalidObject("Edge do not exist!"))
        for server_id in self.__vertexes_dict.keys():
            for edge in self.get_edges_list(server_id):
                if (edge.edgeID == edgeID):
                    self.remove_edge(server_id, edge)
        self.save_graph_on_servers()
        # self.get_file_for_use("write")
        # with open("../outputs/vertexes", "w") as file:
        #     file.write(self.formated_vertexes_list())
        # with open("../outputs/edges", "w") as file:
        #     file.write(self.formated_edges_list())
        # self.free_file_for_use("write")

    #####################
    # OTHERS OPERATIONS #
    #####################

    def listVertexes(self, edgeID):
        self.createGraph()
        vertexes_list = []
        for edge in self.get_edges_list(server_id):
            if (edge.edgeID == edgeID):
                vertexes_list.append(edge)  # edge.vertexA
                vertexes_list.append(edge)  # edge.vertexB
        return vertexes_list

    def listEdges(self, vertexID):
        self.createGraph()
        vertex = self.search_vertex(vertexID)
        if (vertex == None):
            raise(InvalidObject("Vertex do not exist!"))
        return vertex.edges

    def listNeighbourVertexes(self, vertexID):
        self.createGraph()
        neighbour_vertexes_list = []
        if (self.search_vertex(vertexID) == None):
            raise(InvalidObject("Vertex do not exist!"))
        for server_id in self.__vertexes_dict.keys():
            for edge in self.get_edges_list(server_id):
                if (edge.vertexA == vertexID):
                    neighbour_vertexes_list.append(edge)  # edge.edgeID
                elif (edge.vertexB == vertexID):
                    neighbour_vertexes_list.append(edge)  # edge.edgeID

        return neighbour_vertexes_list

    def calculateDijkstra(self, vertex_id_a, vertex_id_b):
        self.parseDataFromAllServers()
        dijkstra = Dijkstra()
        dijkstra.parse_data_to_objects(self.__servers_graph_dict)
        dijkstra.get_shortest_path(vertex_id_a, vertex_id_b)


def main(server_id, number_of_servers, port=3030):

    handler_object = Handler(server_id, number_of_servers)

    processor = GraphOperations.Processor(handler_object)
    transport = TSocket.TServerSocket(port=port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Server %s Port: %s" % (server_id, port))
    print("The server is ready to go!")
    server.serve()

    print("Bye Bye!")





vertexes_path = "../outputs/vertexes"
edges_path = "../outputs/edges"
# def __init__(self, server_id, number_of_servers):

# port = int(sys.argv[1])
file_name, server_id, number_of_servers, port = sys.argv

# print file_name
# print server_id
# print port
# print number_of_servers

main(int(server_id), int(number_of_servers), int(port))
