from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QRectF

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type:int = 1):
        self.socket = socket
        super().__init__(socket.node.graphicsNode)

        self.radius = 6.0
        self.outline_width = 1.0
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52E220"),
            QColor("#FF0056A6"),
            QColor("#FFA86DB1"),
            QColor("#FFB54747"),
            QColor("#FFDBE220"),
        ]
        self._color_background = self._colors[socket_type - 1] if 0 < socket_type <= len(self._colors) else self._colors[0]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QColor(self._color_background)

    def __str__(self):
        return "< QDMGraphicsSocket %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget = None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(
            int(-self.radius),
            int(-self.radius),
            int(2 * self.radius),
            int(2 * self.radius)
        )

    def boundingRect(self) -> QRectF:
        return QRectF(-self.radius - self.outline_width,
                      -self.radius - self.outline_width, 
                      2 * self.radius - self.outline_width, 
                      2 * self.radius - self.outline_width)