
#CREATE
#READ
#UPDATE
#DELETE
#LIST VERTEXES OF AN EDGE > listVertexes
#LIST EDGE OF A VERTEX > listEdges
#LIST NEIGHBOURS VERTEXES OF A VERTEX > listNeighbourVertexes
# Flags: 0 - From A to B, 1 = From B to A, 2 - Bidirecional

namespace py graphProject

exception CouldNotFindObject {
	1: string msg
}

exception OperationHasFailed {
	1: string msg 
}

exception InvalidObject {
	1: string msg
}


struct Edge {
	1: required i64 edgeID,
	2: required i64 vertexA,
	3: required i64 vertexB,
	4: required double weight,
	5: required i32 flag,
	6: required string description
}

struct Vertex {
  1: required i64 vertexID,
  2: required i64 color,
  3: required string description,
  4: required double weight,
  5: list<Edge> edges
}

struct Graph {
  1: i64 graphID,
  2: set<Vertex> list_of_vertexes,
  3: set<Edge> list_of_edges
}

service GraphOperations {
      
  void createVertex(1:i64 vertexID, 2:i64 color, 3:string description, 4: double weight) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  Vertex readVertex(1:i64 vertexID) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg)
  void updateVertex(1:i64 vertexID, 2:i64 color, 3:string description, 4:double weight) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg, 3: InvalidObject invalidObjMsg)
  void deleteVertex(1:i64 vertexID) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg, 3: InvalidObject invalidObjMsg)
  
  void createEdge(1:i64 edgeID, 2:i64 vertexA, 3:i64 vertexB, 4:i64 weight, 5:i32 flag, 6:i64 description) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  Edge readEdge(1:i64 vertexA, 2:i64 vertexB) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg)
  void updateEdge(1:i64 edgeID, 2:i64 vertexA, 3:i64 vertexB, 4:double weight, 5:i32 flag, 6:i64 description) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg, 3: InvalidObject invalidObjMsg)
  void deleteEdge(1:i64 edgeID) throws (1: CouldNotFindObject objectNotFound, 2: OperationHasFailed opFailedMsg, 3: InvalidObject invalidObjMsg)
  
  list<Vertex> listVertexes(1: Edge edge) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  list<Edge> listEdges(1: Vertex vertex) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
  list<Vertex> listNeighbourVertexes(1: Vertex vertex) throws (1: InvalidObject invalidObjMsg, 2: OperationHasFailed opFailedMsg)
}
