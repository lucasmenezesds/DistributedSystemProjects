#!/usr/bin/python


class Balancer(object):
    """docstring for Balancer"""
    def __init__(self, number_of_servers=1, array_of_vertexes=[], array_of_edges=[]):
        self.__number_of_servers = number_of_servers
        self.__vertexes_dataLocation_table = {}
        self.__edges_dataLocation_table = {}  # fazer loop se array.size > 1
        self.__data_location = {}
        self.__array_of_vertexes = array_of_vertexes
        self.__array_of_edges = array_of_edges

    def balance_graph(self):
        for vertex in self.__array_of_vertexes:
            vertex_id = vertex.vertexID
            self.balance_vertex(vertex_id)
        for edge in self.__array_of_edges:
            self.balance_edge(edge)

    def balance_vertex(self, vertex_id):
        # hash_1 = hash(str(vertex_id))
        hash_value = vertex_id
        selected_server_id = hash_value % self.__number_of_servers
        selected_server_id += 1
        key = vertex_id
        self.__vertexes_dataLocation_table[key] = selected_server_id

    def balance_edge(self, edge):
        key = edge.edgeID
        vertexes = (edge.vertexA, edge.vertexB)
        for vertex_id in vertexes:
            if key in self.__edges_dataLocation_table:
                self.__edges_dataLocation_table[key].append(self.__vertexes_dataLocation_table[vertex_id])
            else:
                self.__edges_dataLocation_table[key] = [self.__vertexes_dataLocation_table[vertex_id]]

    def get_list_of_servers(self):
        return list(range(1, self.__number_of_servers))

    def get_vertex_location(self, vertex_id):
        selected_server_id = vertex_id % self.__number_of_servers
        selected_server_id += 1
        return selected_server_id

    def get_edge_location(self, edge):
        vertexes = (edge.vertexA, edge.vertexB)
        edge_locations = []
        for vertex_id in vertexes:
            edge_locations.append(self.get_vertex_location(vertex_id))

        return edge_locations
