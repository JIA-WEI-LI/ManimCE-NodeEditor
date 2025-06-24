import logging
logger = logging.getLogger(__name__)

from node_editor_window.graphics.graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, scene, start_socket, end_socket, edge_type:int = EDGE_TYPE_BEZIER):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self
        
        self.graphicsEdge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        logger.debug(f" Edge: {self.graphicsEdge.posSource} to {self.graphicsEdge.posDestination}")
        self.scene.graphicsScene.addItem(self.graphicsEdge)
        self.scene.addEdge(self)

    def __str__(self):
        return "< Edge %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:])

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
        self.graphicsEdge.update()

    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.remove_from_socket()
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        self.scene.removeEdge(self)