from NodeEditorWindow.graphics.graphics_node import QDMGraphicsNode
from NodeEditorWindow.content.node_content_widget import QDMNodeContentWidget

class Node():
    def __init__(self, scene, title = "Undefined Node"):
        self.scene = scene
        self.title = title

        self.content = QDMNodeContentWidget(self)
        self.graphicsNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)

        self.inputs = []
        self.outputs = []