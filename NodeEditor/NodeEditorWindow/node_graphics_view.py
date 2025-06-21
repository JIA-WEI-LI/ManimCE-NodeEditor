import os
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QEvent

class QDMGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent=parent)

        self.graphicsScene = graphicsScene

        self.initUI()

        self.setScene(self.graphicsScene)

        self.zoomInFator = 1.25
        self.zoomClamp = False
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                           QPainter.RenderHint.HighQualityAntialiasing |
                           QPainter.RenderHint.TextAntialiasing |
                           QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)
    
    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.Type.MouseButtonRelease, 
                                   event.localPos(), 
                                   event.screenPos(), 
                                   Qt.MouseButton.MiddleButton, 
                                   Qt.MouseButton.NoButton,
                                   event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), 
                                event.localPos(), 
                                event.screenPos(),
                                Qt.MouseButton.MiddleButton,
                                event.buttons() | Qt.MouseButton.LeftButton,
                                event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(), 
                                event.localPos(), 
                                event.screenPos(),  
                                Qt.MouseButton.LeftButton,
                                event.buttons() | -Qt.MouseButton.LeftButton,
                                event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

    def leftMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # calculate out zoom factor
        zoomFactor = 1 / self.zoomInFator

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFator
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom = self.zoomRange[0]
            clamped = True
        if self.zoom > self.zoomRange[1]:
            self.zoom = self.zoomRange[1]
            clamped = True

        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)