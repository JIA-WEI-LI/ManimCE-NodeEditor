from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout

from NodeEditorWindow.nodeGraphics_Scene import QDMGraphicsScene

class NodeEditorWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Create graphics scene
        self.graphicsScene = QDMGraphicsScene()

        # Create graphics view
        self.view = QGraphicsView(self)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()