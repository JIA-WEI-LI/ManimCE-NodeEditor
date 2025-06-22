from typing import List

from NodeEditorWindow.graphics.graphics_node import QDMGraphicsNode
from NodeEditorWindow.content.node_content_widget import QDMNodeContentWidget
from NodeEditorWindow.core.socket import Socket

class Node():
    def __init__(self, scene, title:str = "Undefined Node", inputs:List = [], outputs:List = []):
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.graphicsNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)

        self.inputs = []
        self.outputs = []
        for items in inputs:
            socket = Socket(node=self)
            self.inputs.append(socket)