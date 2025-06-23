import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QEvent

from node_editor_window.graphics.graphics_socket import QDMGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

class QDMGraphicsView(QGraphicsView):
    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent=parent)

        self.graphicsScene = graphicsScene

        self.initUI()

        self.setScene(self.graphicsScene)

        self.mode = MODE_NOOP

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
        item = self.getItemAtClick(event)

        self.left_lmb_click_scene_pos = self.mapToScene(event.pos())
        if isinstance(item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                logger.debug("Start dragging edge")
                logger.debug("  assign Start Socket")
                return
        
        if self.mode == MODE_EDGE_DRAG:
            self.mode = MODE_NOOP
            logger.debug("End dragging edge")
            if isinstance(item, QDMGraphicsSocket):
                logger.debug("  assign End Socket")
                return
            
        super().mousePressEvent(event)
            

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:

            new_lmb_relaese_scene_pos = self.mapToScene(event.pos())
            dist_scene = new_lmb_relaese_scene_pos - self.left_lmb_click_scene_pos

            if (dist_scene.x()**2 + dist_scene.y()**2) < (EDGE_DRAG_START_THRESHOLD**2):
                pass
            else:
                self.mode = MODE_NOOP
                logger.debug("End dragging edge")
                if isinstance(item, QDMGraphicsSocket):
                    logger.debug("  assign End Socket")
                    return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)

        return obj

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