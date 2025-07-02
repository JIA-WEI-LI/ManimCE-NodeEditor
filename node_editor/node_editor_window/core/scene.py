from ..graphics.graphics_scene import QDMGraphicsScene

class Scene:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.graphicsScene = QDMGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)