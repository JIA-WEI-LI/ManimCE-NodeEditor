from PyQt5.QtWidgets import QGraphicsView, QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit, QApplication
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QFile

from NodeEditorWindow.node_scene import Scene
from NodeEditorWindow.node_node import Node
from NodeEditorWindow.node_graphics_view import QDMGraphicsView

class NodeEditorWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.stylesheet_filename = "NodeEditor/qss/nodestyle.qss"
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.scene = Scene()
        self.graphicsScene = self.scene.graphicsScene

        node = Node(self.scene, "My Node")

        # Create graphics view
        self.view = QDMGraphicsView(self.scene.graphicsScene, self)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

    def loadStylesheet(self, filename):
        import inspect, os; print('>', os.path.basename(inspect.stack()[0].filename), '-', inspect.stack()[0].lineno, " filename: ", filename)
        file = QFile(filename)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))