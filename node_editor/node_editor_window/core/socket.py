import logging
logger = logging.getLogger(__name__)

from node_editor_window.graphics.graphics_socket import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3 
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node, index:int = 0, position:int = LEFT_TOP, socket_type:int = 1):

        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        self.graphicsSocket = QDMGraphicsSocket(self, self.socket_type)
        self.graphicsSocket.setPos(*self.node.setSocketPosition(self.index, self.position))

        logger.debug(f"Socket -- creating with {self.index} {self.position} for node {self.node}")

        self.edge = None

    def __str__(self):
        return "< Socket %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self):
        logger.debug(f"Get socket position: {self.index} {self.position} for node {self.node}")
        res = self.node.setSocketPosition(self.index, self.position)
        logger.debug(f"Socket position (res): {res}")
        return res
    
    def setConnectedEdge(self, edge):
        self.edge = edge

    def hasEdge(self):
        return self.edge is not None