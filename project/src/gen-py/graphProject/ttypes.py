#
# Autogenerated by Thrift Compiler (0.10.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
import sys

from thrift.transport import TTransport


class WrongServer(TException):
    """
    Attributes:
     - msg
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'msg', 'UTF8', None, ),  # 1
    )

    def __init__(self, msg=None,):
        self.msg = msg

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.msg = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('WrongServer')
        if self.msg is not None:
            oprot.writeFieldBegin('msg', TType.STRING, 1)
            oprot.writeString(self.msg.encode('utf-8') if sys.version_info[0] == 2 else self.msg)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class OperationHasFailed(TException):
    """
    Attributes:
     - msg
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'msg', 'UTF8', None, ),  # 1
    )

    def __init__(self, msg=None,):
        self.msg = msg

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.msg = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('OperationHasFailed')
        if self.msg is not None:
            oprot.writeFieldBegin('msg', TType.STRING, 1)
            oprot.writeString(self.msg.encode('utf-8') if sys.version_info[0] == 2 else self.msg)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class InvalidObject(TException):
    """
    Attributes:
     - msg
    """

    thrift_spec = (
        None,  # 0
        (1, TType.STRING, 'msg', 'UTF8', None, ),  # 1
    )

    def __init__(self, msg=None,):
        self.msg = msg

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.msg = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('InvalidObject')
        if self.msg is not None:
            oprot.writeFieldBegin('msg', TType.STRING, 1)
            oprot.writeString(self.msg.encode('utf-8') if sys.version_info[0] == 2 else self.msg)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __str__(self):
        return repr(self)

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Edge(object):
    """
    Attributes:
     - edgeID
     - vertexA
     - vertexB
     - weight
     - flag
     - description
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I64, 'edgeID', None, None, ),  # 1
        (2, TType.I64, 'vertexA', None, None, ),  # 2
        (3, TType.I64, 'vertexB', None, None, ),  # 3
        (4, TType.DOUBLE, 'weight', None, None, ),  # 4
        (5, TType.I32, 'flag', None, None, ),  # 5
        (6, TType.STRING, 'description', 'UTF8', None, ),  # 6
    )

    def __init__(self, edgeID=None, vertexA=None, vertexB=None, weight=None, flag=None, description=None,):
        self.edgeID = edgeID
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.weight = weight
        self.flag = flag
        self.description = description

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.edgeID = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.vertexA = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.vertexB = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.weight = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.flag = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.description = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Edge')
        if self.edgeID is not None:
            oprot.writeFieldBegin('edgeID', TType.I64, 1)
            oprot.writeI64(self.edgeID)
            oprot.writeFieldEnd()
        if self.vertexA is not None:
            oprot.writeFieldBegin('vertexA', TType.I64, 2)
            oprot.writeI64(self.vertexA)
            oprot.writeFieldEnd()
        if self.vertexB is not None:
            oprot.writeFieldBegin('vertexB', TType.I64, 3)
            oprot.writeI64(self.vertexB)
            oprot.writeFieldEnd()
        if self.weight is not None:
            oprot.writeFieldBegin('weight', TType.DOUBLE, 4)
            oprot.writeDouble(self.weight)
            oprot.writeFieldEnd()
        if self.flag is not None:
            oprot.writeFieldBegin('flag', TType.I32, 5)
            oprot.writeI32(self.flag)
            oprot.writeFieldEnd()
        if self.description is not None:
            oprot.writeFieldBegin('description', TType.STRING, 6)
            oprot.writeString(self.description.encode('utf-8') if sys.version_info[0] == 2 else self.description)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.edgeID is None:
            raise TProtocolException(message='Required field edgeID is unset!')
        if self.vertexA is None:
            raise TProtocolException(message='Required field vertexA is unset!')
        if self.vertexB is None:
            raise TProtocolException(message='Required field vertexB is unset!')
        if self.weight is None:
            raise TProtocolException(message='Required field weight is unset!')
        if self.flag is None:
            raise TProtocolException(message='Required field flag is unset!')
        if self.description is None:
            raise TProtocolException(message='Required field description is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Vertex(object):
    """
    Attributes:
     - vertexID
     - color
     - description
     - weight
     - edges
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I64, 'vertexID', None, None, ),  # 1
        (2, TType.I64, 'color', None, None, ),  # 2
        (3, TType.STRING, 'description', 'UTF8', None, ),  # 3
        (4, TType.DOUBLE, 'weight', None, None, ),  # 4
        (5, TType.LIST, 'edges', (TType.STRUCT, (Edge, Edge.thrift_spec), False), None, ),  # 5
    )

    def __init__(self, vertexID=None, color=None, description=None, weight=None, edges=None,):
        self.vertexID = vertexID
        self.color = color
        self.description = description
        self.weight = weight
        self.edges = edges

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.vertexID = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.color = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.description = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.DOUBLE:
                    self.weight = iprot.readDouble()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.LIST:
                    self.edges = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = Edge()
                        _elem5.read(iprot)
                        self.edges.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Vertex')
        if self.vertexID is not None:
            oprot.writeFieldBegin('vertexID', TType.I64, 1)
            oprot.writeI64(self.vertexID)
            oprot.writeFieldEnd()
        if self.color is not None:
            oprot.writeFieldBegin('color', TType.I64, 2)
            oprot.writeI64(self.color)
            oprot.writeFieldEnd()
        if self.description is not None:
            oprot.writeFieldBegin('description', TType.STRING, 3)
            oprot.writeString(self.description.encode('utf-8') if sys.version_info[0] == 2 else self.description)
            oprot.writeFieldEnd()
        if self.weight is not None:
            oprot.writeFieldBegin('weight', TType.DOUBLE, 4)
            oprot.writeDouble(self.weight)
            oprot.writeFieldEnd()
        if self.edges is not None:
            oprot.writeFieldBegin('edges', TType.LIST, 5)
            oprot.writeListBegin(TType.STRUCT, len(self.edges))
            for iter6 in self.edges:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.vertexID is None:
            raise TProtocolException(message='Required field vertexID is unset!')
        if self.color is None:
            raise TProtocolException(message='Required field color is unset!')
        if self.description is None:
            raise TProtocolException(message='Required field description is unset!')
        if self.weight is None:
            raise TProtocolException(message='Required field weight is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class Graph(object):
    """
    Attributes:
     - graphID
     - list_of_vertexes
     - list_of_edges
    """

    thrift_spec = (
        None,  # 0
        (1, TType.I64, 'graphID', None, None, ),  # 1
        (2, TType.SET, 'list_of_vertexes', (TType.STRUCT, (Vertex, Vertex.thrift_spec), False), None, ),  # 2
        (3, TType.SET, 'list_of_edges', (TType.STRUCT, (Edge, Edge.thrift_spec), False), None, ),  # 3
    )

    def __init__(self, graphID=None, list_of_vertexes=None, list_of_edges=None,):
        self.graphID = graphID
        self.list_of_vertexes = list_of_vertexes
        self.list_of_edges = list_of_edges

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.I64:
                    self.graphID = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.SET:
                    self.list_of_vertexes = set()
                    (_etype10, _size7) = iprot.readSetBegin()
                    for _i11 in range(_size7):
                        _elem12 = Vertex()
                        _elem12.read(iprot)
                        self.list_of_vertexes.add(_elem12)
                    iprot.readSetEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.SET:
                    self.list_of_edges = set()
                    (_etype16, _size13) = iprot.readSetBegin()
                    for _i17 in range(_size13):
                        _elem18 = Edge()
                        _elem18.read(iprot)
                        self.list_of_edges.add(_elem18)
                    iprot.readSetEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, (self.__class__, self.thrift_spec)))
            return
        oprot.writeStructBegin('Graph')
        if self.graphID is not None:
            oprot.writeFieldBegin('graphID', TType.I64, 1)
            oprot.writeI64(self.graphID)
            oprot.writeFieldEnd()
        if self.list_of_vertexes is not None:
            oprot.writeFieldBegin('list_of_vertexes', TType.SET, 2)
            oprot.writeSetBegin(TType.STRUCT, len(self.list_of_vertexes))
            for iter19 in self.list_of_vertexes:
                iter19.write(oprot)
            oprot.writeSetEnd()
            oprot.writeFieldEnd()
        if self.list_of_edges is not None:
            oprot.writeFieldBegin('list_of_edges', TType.SET, 3)
            oprot.writeSetBegin(TType.STRUCT, len(self.list_of_edges))
            for iter20 in self.list_of_edges:
                iter20.write(oprot)
            oprot.writeSetEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
