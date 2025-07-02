from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPen, QPainter, QPolygonF
from PyQt5.QtCore import Qt, QRectF

class QDMCutLine(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.line_points = []

        self._pen = QPen(Qt.GlobalColor.white)
        self._pen.setWidth(2)
        self._pen.setDashPattern([3, 3])

        self.setZValue(2)

    def boundRect(self):
        return QRectF(0, 0, 0, 1)
    
    def paint(self, painter: QPainter, QStyleOptionGraphicsItem, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(self._pen)

        poly = QPolygonF(self.line_points)
        painter.drawPolyline(poly)