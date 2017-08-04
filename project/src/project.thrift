
#CREATE
#READ
#UPDATE
#DELETE
#LIST VERTEXES OF AN EDGE > listVertexes
#LIST EDGE OF A VERTEX > listEdges
#LIST NEIGHBOURS VERTEXES OF A VERTEX > listNeighbourVertexes
# Flags: if 0, BOTH, if 1 FROM a TO b, if 2, FROM b TO a

namespace py graphProject

exception OperationHasFailed {
  1: string msg
}

exception InvalidObject {
  1: string msg
}

struct Edge {
  1: required i64 vertexA,
  2: required i64 vertexB,
  3: required double weight,
  4: required i32 flag,
  5: required string description
}

struct Vertex {
  1: required i64 vertexID,
  2: required i64 color,
  3: required string description,
  4: required double weight,
}

struct Graph {
  1: i64 graphID,
  2: set<Vertex> list_of_vertexes,
  3: set<Edge> list_of_edges
}

service GraphOperations {

  void ping()

  void shutdown()

  void createVertex(1: i64 vertexID, 2:i64 color, 3: string description, 4: double weight) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  Vertex readVertex(1: i64 vertexID) throws (1: OperationHasFailed opFailedMsg)
  void updateVertex(1: i64 vertexID, 2:i64 color, 3: string description, 4:double weight) throws (1: OperationHasFailed opFailedMsg, 3: InvalidObject invalidObjMsg)
  void deleteVertex(1: i64 vertexID) throws (1: InvalidObject invalidObjMsg)
  bool hasVertex(1: i64 vertexID) throws (1: OperationHasFailed opFailedMsg)

  void createEdge(1:i64 vertexA, 2:i64 vertexB, 3:i64 weight, 4:i32 flag, 5:string description) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  Edge readEdge(1:i64 vertexA, 2:i64 vertexB) throws (1: OperationHasFailed opFailedMsg)
  void updateEdge(1:i64 vertexA, 2:i64 vertexB, 3:double weight, 4:i32 flag, 5:string description) throws (1: OperationHasFailed opFailedMsg, 2: InvalidObject invalidObjMsg)
  void deleteEdge(1:i64 vertexA, 2:i64 vertexB) throws (1: OperationHasFailed opFailedMsg, 2: InvalidObject invalidObjMsg)
  bool hasEdge(1:i64 vertexA, 2:i64 vertexB) throws (1: OperationHasFailed opFailedMsg)


  list<Vertex> listAllVertexes(1:bool justLocal) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  list<Edge> listAllEdges(1:bool justLocal) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  list<Edge> listEdges(1: i64 vertex) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  list<Vertex> listNeighbourVertexes(1: i64 vertex) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)

  #void createVertexFile(1:list<Vertex> dataToSave, 2:i64 serverId) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  #void createEdgeFile(1:list<Edge> dataToSave, 2:i64 serverId) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  #list<Vertex> getLocalVertexes() throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  #list<Edge> getLocalEdges() throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)

  list<Vertex> calculateDijkstra(1:i64 vertexA, 2:i64 vertexB) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)

  # Part 4 Implementation

  
}