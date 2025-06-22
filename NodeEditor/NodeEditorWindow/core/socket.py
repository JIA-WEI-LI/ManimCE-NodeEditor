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