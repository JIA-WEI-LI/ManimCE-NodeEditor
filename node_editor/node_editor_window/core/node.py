from typing import List
import logging
logger = logging.getLogger(__name__)

from ..graphics.graphics_node import QDMGraphicsNode
from ..content.node_content_widget import QDMNodeContentWidget
from .socket import Socket, LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM

class Node():
    def __init__(self, scene, title:str = "Undefined Node", inputs:List = [], outputs:List = []):
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.graphicsNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)

        self.socket_spacing = 22

        # Create sockets for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "< Node %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:]) + " Title: %s" % self.title

    @property
    def pos(self):
        return self.graphicsNode.setPos()       # QPonintF
    def setPos(self, x: int, y: int):
        self.graphicsNode.setPos(x, y)

    def setSocketPosition(self, index: int, position: str):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.graphicsNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = (self.graphicsNode.height
            - self.graphicsNode.edge_size
            - self.graphicsNode._padding
            - index * self.socket_spacing)
        else:
            y = (self.graphicsNode.title_height 
            + self.graphicsNode.edge_size 
            + self.graphicsNode._padding 
            + index * self.socket_spacing)

        return [x, y]
    
    def updateConnectedEdges(self, edge=None):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        logger.debug(f"> Remove Node {self}")
        logger.debug(f" - remove all edge from sockets")
        for socket in (self.inputs + self.outputs):
            if socket.hasEdge():
                logger.debug(f"     - removing from socket: {socket} edge {socket.edge}")
                socket.edge.remove()
        logger.debug(f" - remove graphicsNode")
        self.scene.graphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        logger.debug(f" - remove node from scene")
        self.scene.removeNode(self)
        logger.debug(f" - everythings was done.")