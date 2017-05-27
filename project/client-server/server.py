#!/usr/bin/python

# https://thrift.apache.org/tutorial/py

import sys
sys.path.append("../gen-py/")

from graphProject import *
from graphProject.ttypes import *
# import socket
# import logging
from threading import Lock
from thrift import Thrift
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class Handler(object):
	"""
		Graph Handler Class
	"""

	def __init__(self):
		self.__mutual_exclusion = Lock()
		self.__vertexes_list = []
		self.__edges_list = []


	def get_file_for_use(self):
		self.__mutual_exclusion.acquire()

	def free_file_for_use(self):
		self.__mutual_exclusion.release()

	def append_vertex(self, vertex):
		self.__vertexes_list.append(vertex)

	def append_edge(self, edge):
		self.__edges_list.append(edge)

	def remove_vertex(self, vertex):
		self.__vertexes_list.remove(vertex)
		
	def remove_edge(self, edge):
		self.__edges_list.remove(edge)


	def check_valid_data(self, data_array):
		for elem in data_array:
			if (elem == "" or elem == None):
				sys.exit("Some value of edge or vertex is invalid, check the files please!")

	def get_vertexes_list(self):
		return self.__vertexes_list

	def get_edges_list(self):
		return self.__edges_list

	def clean_list(self, option="both"):
		if (option == "vertex"):
			self.__vertexes_list = []
		elif (option == "edge"):
			self.__edges_list = []
		else:
			self.__vertexes_list = []
			self.__edges_list = []


	def update_vertexes_list_of_edges(self, vertex=False):
		if(vertex == False):
			for vertex  in self.get_vertexes_list():
				for edge in self.get_edges_list():
					if (vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB):
						vertex.edges.append(edge)
		else:
			for edge in self.get_edges_list():
				if (vertex.vertexID == edge.vertexA or vertex.vertexID == edge.vertexB):
					vertex.edges.append(edge)

	def set_string(self, array_of_values):
		string = ','.join([str(value) for value in array_of_values])
		final_string = string+"\n"

		return final_string


	def formated_vertexes_list(self):
		string = ""
		for vertex in get_vertexes_list():
			vertex_array = [vertex.vertexID, vertex.color, vertex.description, vertex.weight]
			sub_string = self.set_string(vertex_array)
			string = string +sub_string
		return string

	def formated_edges_list(self):
		string = ""
		for edge in get_edges_list():
			edge_array = [edge.edgeID, edge.vertexA, edge.vertexB, edge.weight, edge.flag, edge.description]
			sub_string = self.set_string(edge_array)
			string = string +sub_string
		return string

	def create_graph(self, graph_id=1, vextexes_file_path="../outputs/vertexes", edges_file_path="../outputs/edges"):
		self.get_file_for_use()

		vertexes_file = open(vextexes_file_path,'r')
		vertexes_lines = vertexes_file.read().splitlines()

		vertexes_lines_header_size = len(vertexes_lines[0].split(","))
		vertexes_lines.pop(0)

		for line in vertexes_lines:
			vertex_data = line.split(",")
			if (len(vertex_data) == vertexes_lines_header_size):
				self.check_valid_data(vertex_data)

				vertex = Vertex(int(vertex_data[0]), int(vertex_data[1]), str(vertex_data[2]), float(vertex_data[3]), [])
				self.append_vertex(vertex)
			else:
				sys.exit("Some vertex data is missing! Check the file please!")

		edges_file = open(edges_file_path,'r')
		edges_lines = edges_file.read().splitlines()
		
		edge_lines_header_size = len(edges_lines[0].split(","))
		edges_lines.pop(0)

		for line in edges_lines:
			edge_data = line.split(",")
			if (len(edge_data) == edge_lines_header_size):
				self.check_valid_data(edge_data)

				edge = Edge(int(edge_data[0]), int(edge_data[1]), int(edge_data[2]), float(edge_data[3]), int(edge_data[4]), str(edge_data[5]))
				self.append_edge(edge)
			else:
				sys.exit("Some edge data is missing! Check the file please!")
		self.update_vertexes_list_of_edges()

		# print(self.get_vertexes_list()[0])
		
		self.free_file_for_use()
 
		graph = Graph(graph_id, self.get_vertexes_list, self.get_edges_list)
		return graph


	def get_vertex(self, vertex_id):
		self.create_graph()
		vertex_return = None
		for vertex in self.get_vertexes_list():
			if (vertex.vertexID == vertex_id):
				vertex_return = vertex
		return vertex_return


	def get_edge(self, edge_id):
		self.create_graph()
		edge_return = None
		for edge in self.get_edges_list():
			if (edge.edgeID == edge_id):
				edge_return = edge
		return edge_return

	def insert_vertex(self, data_array, vertexes_path="../outputs/vertexes"):
		self.get_file_for_use()
		normalized_string = self.set_string(data_array)
		with open(vertexes_path, "a") as file:
			file.write(normalized_string)
		self.free_file_for_use()

	def insert_edge(self, data_array, edges_path="../outputs/edges"):
		self.get_file_for_use()
		normalized_string = self.set_string(data_array)
		with open(edges_path, "a") as file:
			file.write(normalized_string)
		self.free_file_for_use()


	def createVertex(self, vertexID, color, description, weight):
		self.create_graph()
		if (self.get_vertex(vertexID)):
			sys.exit("Vertex already exist!")
		data_array = [vertexID, color, description, weight]
		self.insert_vertex(data_array)


	def readVertex(self, vertexID):
		self.create_graph()
		selected_vertex = None
		for vertex in self.get_vertexes_list():
			if (vertex.vertexID == vertexID):
				selected_vertex = vertex
		return selected_vertex


	def updateVertex(self, vertexID, color=None, description=None, weight=None):
		self.clean_list("vertex")
		self.create_graph()
		vertex = self.get_vertex(vertexID)
		if( vertex == None):
			sys.exit("Vertex do not exist!")

		vertex.color = color
		vertex.description = description 
		vertex.weight = weight
		self.update_vertexes_list_of_edges(vertex)


	def deleteVertex(self, vertexID):
		self.clean_list("both")
		self.create_graph()
		vertex = self.get_vertex(vertexID)
		if( vertex == None):
			sys.exit("Vertex do not exist!")
		for vertex in self.get_vertexes_list():
			if (vertex.vertexID == vertexID):
				for edge in vertex.edges:
					self.remove_edge(edge)
				self.remove_vertex(vertex)

		self.get_file_for_use()
		with open("../outputs/vertexes", "w") as file:
			file.write(self.formated_vertexes_list())
		with open("../outputs/edges", "w") as file:
			file.write(self.formated_edges_list())
		self.free_file_for_use()


	def createEdge(self, edgeID, vertexA=None, vertexB=None, weight=None, flag=2, description=None):
		self.create_graph()
		if (self.get_edge(edgeID) == None):
			sys.exit("Edge already exist!")
		data_array = [edgeID, vertexA, vertexB, weight, flag, description]
		self.insert_edge(data_array)


	def readEdge(self, vertexA, vertexB):
		self.create_graph()
		selected_edge = None
		for edge in self.get_edges_list():
			if (edge.edgeID == edgeID):
				selected_edge = edge
		return selected_edge


	def updateEdge(self, edgeID, vertexA=None, vertexB=None, weight=None, flag=None, description=None):
		self.clean_list("edge")
		self.create_graph()
		edge = self.get_edge(edgeID)
		if( edge == None):
			sys.exit("Edge do not exist!")

		edge.vertexA = vertexA 
		edge.vertexB = vertexB 
		edge.weight = weight
		edge.flag = flag
		edge.description = description


	def deleteEdge(self, edgeID):
		self.clean_list("both")
		self.create_graph()
		edge = self.get_edge(edgeID,vertexA,vertexB,weight,flag,description)
		if( edge == None):
			sys.exit("Edge do not exist!")
		for edge in self.get_edges_list():
			if (edge.edgeID == edgeID):
				self.remove_edge(edge)

		self.get_file_for_use()
		with open("../outputs/vertexes", "w") as file:
			file.write(self.formated_vertexes_list())
		with open("../outputs/edges", "w") as file:
			file.write(self.formated_edges_list())
		self.free_file_for_use()


	def listVertexes():
		self.create_graph()
		pass

	def listEdges():
		self.create_graph()
		pass

	def listNeighbourVertexes():
		self.create_graph()
		pass



vertexes_path = "../outputs/vertexes"
edges_path = "../outputs/edges"
port = 3030


handler_object = Handler()
# handler_object.create_graph(1, vertexes_path, edges_path)
# print (handler_object.get_vertexes_list())



processor = GraphOperations.Processor(handler_object)
transport = TSocket.TServerSocket(port=port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Server Port: "+str(port))
print("The server is ready to go!")
server.serve()
print("Bye Bye!")

