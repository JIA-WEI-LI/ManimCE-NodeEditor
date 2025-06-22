from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QColor, QPen, QPainter
from PyQt5.QtCore import QRectF

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.radius = 6.0
        self.outline_width = 1.0
        self._color_background = QColor("#FFFF7700")
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QColor(self._color_background)

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