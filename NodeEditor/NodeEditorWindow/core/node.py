from typing import List

from NodeEditorWindow.graphics.graphics_node import QDMGraphicsNode
from NodeEditorWindow.content.node_content_widget import QDMNodeContentWidget
from NodeEditorWindow.core.socket import Socket, LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM

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

        for items in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for items in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP)
            counter += 1
            self.outputs.append(socket)

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