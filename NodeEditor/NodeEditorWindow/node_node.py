from NodeEditorWindow.node_graphics_node import QDMGraphicsNode

class Node():
    def __init__(self, scene, title = "Undefined Node"):
        self.scene = scene
        self.title = title

        self.graphicsNode = QDMGraphicsNode(self, self.title)

        self.scene.addNode(self)
        
        self.inputs = []
        self.outputs = []