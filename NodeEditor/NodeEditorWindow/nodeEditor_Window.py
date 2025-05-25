from PyQt5.QtWidgets import QGraphicsView, QWidget

class NodeEditorWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(200,200,800,600)

        self.view = QGraphicsView(self)

        self.setWindowTitle("Node Editor")
        self.show()