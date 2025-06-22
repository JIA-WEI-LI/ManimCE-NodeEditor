from NodeEditorWindow.graphics.graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, scene, start_socket, end_socket, type:int = EDGE_TYPE_DIRECT):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphicsEdge = QDMGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)