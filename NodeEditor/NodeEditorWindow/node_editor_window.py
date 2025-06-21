from PyQt5.QtWidgets import QGraphicsView, QWidget, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtCore import Qt

from NodeEditorWindow.node_scene import Scene
from NodeEditorWindow.node_graphics_view import QDMGraphicsView

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
        self.scene = Scene()
        self.graphicsScene = self.scene.graphicsScene

        # Create graphics view
        self.view = QDMGraphicsView(self.graphicsScene)
        self.view.setScene(self.graphicsScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

        self.addDebugContetnt()

    def addDebugContetnt(self):
        greenBrush = QBrush(Qt.GlobalColor.green)
        outlinePen = QPen(Qt.GlobalColor.black)
        outlinePen.setWidth(2)

        rect = self.graphicsScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        text = self.graphicsScene.addText("This is a Text!", QFont("Ubuntu"))
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        text.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget_1 = QPushButton("PushButton")
        proxy_1 = self.graphicsScene.addWidget(widget_1)
        proxy_1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        proxy_1.setPos(0, 30)

        widget_2 = QTextEdit()
        proxy_2 = self.graphicsScene.addWidget(widget_2)
        proxy_2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        proxy_2.setPos(0, 80)

        line = self.graphicsScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)