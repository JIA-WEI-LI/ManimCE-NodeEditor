import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from ..graphics.graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier
from ..serialization.serialzable import Serializable

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge(Serializable):
    def __init__(self, scene, start_socket = None, end_socket = None, edge_type:int = EDGE_TYPE_BEZIER):
        super().__init__()
        
        self.scene = scene

        # default init
        self._start_socket = None
        self._end_socket = None

        self.start_socket = start_socket
        self.end_socket = end_socket
        self.edge_type = edge_type

        self.scene.addEdge(self)

    def __str__(self):
        return "< Edge %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    @property
    def start_socket(self): return self._start_socket
    @start_socket.setter
    def start_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._start_socket is not None:
            self._start_socket.removeEdge(self)

        # assign new start socket
        self._start_socket = value
        if self.start_socket is not None:
            self.start_socket.addEdge(self)

    @property
    def end_socket(self): return self._end_socket
    @end_socket.setter
    def end_socket(self, value):
        # if we were assigned to some socket before, delete us from the socket
        if self._end_socket is not None:
            self._end_socket.removeEdge(self)

        # assign new end socket
        self._end_socket = value
        if self.end_socket is not None:
            self.end_socket.addEdge(self)

    @property
    def edge_type(self): return self._edge_type
    @edge_type.setter
    def edge_type(self, value):
        if hasattr(self, 'graphicsEdge') and self.graphicsEdge is not None:
            self.scene.graphicsScene.removeItem(self.graphicsEdge)

        self._edge_type = value
        if self.edge_type == EDGE_TYPE_DIRECT:
            self.graphicsEdge = QDMGraphicsEdgeDirect(self)
        elif self.edge_type == EDGE_TYPE_BEZIER:
            self.graphicsEdge = QDMGraphicsEdgeBezier(self)
        else:
            self.graphicsEdge = QDMGraphicsEdgeBezier(self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)

        if self.start_socket is not None:
            self.updatePositions()

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node.graphicsNode.pos().y()
        self.graphicsEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphicsNode.pos().x()
            end_pos[1] += self.end_socket.node.graphicsNode.pos().y()
            self.graphicsEdge.setDestination(*end_pos)
        else:
            self.graphicsEdge.setDestination(*source_pos)
        self.graphicsEdge.update()

    def remove_from_socket(self):
        #TODO: Fix me
        # if self.start_socket is not None:
        #     self.start_socket.removeEdge(None)
        # if self.end_socket is not None:
        #     self.end_socket.removeEdge(None)
        self.start_socket = None
        self.end_socket = None

    def remove(self):
        logger.debug(f"> Remove Edge {self}")
        logger.debug(f" - remove edge from all sockets")
        self.remove_from_socket()
        logger.debug(f" - remove graphicsEdge")
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        logger.debug(f" - remove edge from scene")
        try:
            self.scene.removeEdge(self)
        except ValueError:
            pass
        logger.debug(f" - everythings was done.")

    def serialize(self):
        return OrderedDict([
            ('id', self.id),
            ('edge_type', self.edge_type),
            ('start', self.start_socket.id),
            ('end', self.end_socket.id)
        ])
    
    def deserialize(self, data, hashmap={}, restore_id:bool = True):
        if restore_id: self.id = data['id']
        self.start_socket = hashmap[data['start']]
        self.end_socket = hashmap[data['end']]
        self.edge_type = data['edge_type']
        return True