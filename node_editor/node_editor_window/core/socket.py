import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from ..graphics.graphics_socket import QDMGraphicsSocket
from ..serialization.serialzable import Serializable

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3 
RIGHT_BOTTOM = 4

class Socket(Serializable):
    def __init__(self, node, index:int = 0, position:int = LEFT_TOP, socket_type:int = 1, multi_edges:bool = True):
        super().__init__()

        self.node = node
        self.index = index
        self.is_multi_edges = multi_edges
        self.position = position
        self.socket_type = socket_type

        self.graphicsSocket = QDMGraphicsSocket(self, self.socket_type)
        self.graphicsSocket.setPos(*self.node.setSocketPosition(self.index, self.position))

        logger.debug(f"Socket -- creating with {self.index} {self.position} for node {self.node}")

        self.edges = []

    def __str__(self):
        return "< Socket %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self):
        logger.debug(f"Get socket position: {self.index} {self.position} for node {self.node}")
        res = self.node.setSocketPosition(self.index, self.position)
        logger.debug(f"Socket position (res): {res}")
        return res
    
    def addEdge(self, edge):
        self.edges.append(edge)

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: logger.warning(f"  WARNING!\n    Socket::removeEdge wanna remove Edge: {edge} from self.edges but it's not in the list.")
    
    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('index', self.index),
            ('multi_edges', self.is_multi_edges),
            ('position', self.position),
            ('socket_type', self.socket_type),
        ])
    
    def deserialize(self, data, hashmap={}, restore_id:bool = True):
        if restore_id: self.id = data['id']
        self.is_multi_edges = data['multi_edges']
        hashmap[data['id']] = self
        return True  