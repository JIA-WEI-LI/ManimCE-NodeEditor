from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QFont, QPainterPath, QPen, QColor, QBrush, QPainter

class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.GlobalColor.white
        self._title_font = QFont("Arial")

        self._was_moved = False
        self._last_selected_state = False

        self.initSizes()
        self.initAssets()
        self.initUI()

    def initUI(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        self.initTitle()
        self.title = self.node.title
        self.initSockets()
        self.initContent()

    def initSizes(self):
        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24
        self._padding = 4.0

    def initAssets(self):
        self._title_color = Qt.GlobalColor.white
        self._title_font = QFont("Ubuntu", 10)

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    def onSelected(self):
        # print("grNode onSelected")
        self.node.scene.graphicsScene.itemSelected.emit()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        for node in self.scene().scene.nodes:
            if node.graphicsNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

        if self._last_selected_state != self.isSelected():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(value)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height).normalized()

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width -2 * self._padding)

    def initContent(self):
        self.graphicsContents = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            int(self.edge_size),
            int(self.title_height + self.edge_size),
            int(self.width - 2 * self.edge_size),
            int(self.height - 2 * self.edge_size - self.title_height)
        )
        self.graphicsContents.setWidget(self.content)

    def initSockets(self):
        pass

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget = None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.FillRule.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, 
                           self.title_height - self.edge_size, 
                           self.edge_size, 
                           self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.FillRule.WindingFill)
        path_content.addRoundedRect(0, self.title_height,  self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path_outline.simplified())