import logging
logger = logging.getLogger(__name__)

from NodeEditorWindow.graphics.graphics_socket import QDMGraphicsSocket

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3 
RIGHT_BOTTOM = 4

class Socket():
    def __init__(self, node, index:int = 0, position:int =LEFT_TOP):

        self.node = node
        self.index = index
        self.position = position

        self.graphicsSocket = QDMGraphicsSocket(self.node.graphicsNode)
        self.graphicsSocket.setPos(*self.node.setSocketPosition(self.index, self.position))

        logger.debug(f"Socket -- creating with {self.index} {self.position} for node {self.node}")

        self.edge = None

    def getSocketPosition(self):
        logger.debug(f"Get socket position: {self.index} {self.position} for node {self.node}")
        res = self.node.setSocketPosition(self.index, self.position)
        logger.debug(f"Socket position (res): {res}")
        return res
    
    def setConnectedEdge(self, edge):
        self.edge = edge