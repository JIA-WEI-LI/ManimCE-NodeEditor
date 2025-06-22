from NodeEditorWindow.graphics.graphics_edge import QDMGraphicsEdgeDirect, QDMGraphicsEdgeBezier

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

class Edge():
    def __init__(self, scene, start_socket, end_socket, type:int = EDGE_TYPE_DIRECT):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphicsEdge = QDMGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        self.scene.graphicsScene.addItem(self.graphicsEdge)

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.graphicsNode.pos().x()
        source_pos[1] += self.start_socket.node.graphicsNode.pos().y()
        self.graphicsEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.graphicsNode.pos().x()
            end_pos[1] += self.end_socket.node.graphicsNode.pos().y()
            self.graphicsEdge.setDestination(*end_pos)
        self.graphicsEdge.update()

    def remove_from_socket(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.remove_from_socket()
        self.scene.graphicsScene.removeItem(self.graphicsEdge)
        self.graphicsEdge = None
        self.scene.removeEdge(self)