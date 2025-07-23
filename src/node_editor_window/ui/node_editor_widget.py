import os
import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import QFile

from ..core.scene import Scene
from ..core.node import Node
from ..core.edge import Edge, EDGE_TYPE_BEZIER
from ..graphics.graphics_view import QDMGraphicsView

class NodeEditorWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.stylesheet_filename = "src/node_editor_window/qss/nodeeditor.qss"
        self.loadStylesheet(self.stylesheet_filename)

        self.filename = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()
        # self.graphicsScene = self.scene.graphicsScene

        self.addNodes()

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.graphicsScene, self)
        self.layout.addWidget(self.view)

    def isModified(self):
        return self.scene.has_been_modified

    def isFilenameSet(self):
        return self.filename is not None

    def getUserFriendlyFilename(self):
        name = os.path.basename(self.filename) if self.isFilenameSet() else "New Graph"
        return name + ("*" if self.isModified() else "")

    def addNodes(self):
        node_1 = Node(self.scene, "My Node 1", inputs=[0, 0, 0], outputs=[1])
        node_2 = Node(self.scene, "My Node 2", inputs=[1, 1, 1], outputs=[1])
        node_3 = Node(self.scene, "My Node 3", inputs=[2, 2, 2], outputs=[1])
        node_1.setPos(-350, -250)
        node_2.setPos(-75, 0)
        node_3.setPos(200, -150)

        edge_1 = Edge(self.scene, node_1.outputs[0], node_2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge_2 = Edge(self.scene, node_2.outputs[0], node_3.inputs[0], edge_type=EDGE_TYPE_BEZIER)

    def loadStylesheet(self, filename):
        logger.info(f"Loading stylesheet from {filename}")
        file = QFile(filename)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))