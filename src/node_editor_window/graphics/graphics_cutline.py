import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QPainter, QPolygonF, QPainterPath
from PyQt5.QtCore import Qt, QPointF

class QDMCutLine(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.line_points = []

        self._pen = QPen(Qt.GlobalColor.white)
        self._pen.setWidth(2)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundingRect(self):
        return self.shape().boundingRect()

    def shape(self):
        poly = QPolygonF(self.line_points)

        if len(self.line_points) > 1:
            path = QPainterPath(self.line_points[0])
            for pt in self.line_points[1:]:
                path.lineTo(pt)
        else:
            path = QPainterPath(QPointF(0, 0))
            path.lineTo(QPointF(1, 1))

        return path
    
    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)