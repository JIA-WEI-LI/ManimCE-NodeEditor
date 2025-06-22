from NodeEditorWindow.graphics.graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

class Edge():
    def __init__(self, scene, start_socket, end_socket):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphicsEdge = QDMGraphicsEdgeDirect(self)

        self.scene.graphicsScene.addItem(self.graphicsEdge)