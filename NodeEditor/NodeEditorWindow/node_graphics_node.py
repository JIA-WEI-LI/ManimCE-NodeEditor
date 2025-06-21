from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, title="Node Graphics Item", parent=None):
        super().__init__(parent)

        self._title_color = Qt.GlobalColor.white
        self._title_font = QFont("Arial")

        self.initTitle()
        self.title = title

        self.initUI()

    def initUI(self):
        # Initialize the UI for the node
        pass

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(value)