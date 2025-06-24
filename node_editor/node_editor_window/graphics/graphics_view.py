import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtCore import Qt, QEvent

from node_editor_window.core.edge import Edge, EDGE_TYPE_BEZIER
from node_editor_window.graphics.graphics_socket import QDMGraphicsSocket
from node_editor_window.graphics.graphics_edge import QDMGraphicsEdge

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
        # get the which we click mouse button
        item = self.getItemAtClick(event)

        self.left_lmb_click_scene_pos = self.mapToScene(event.pos())
        if isinstance(item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
        
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return
            
        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        # get the which we release mouse button
        item = self.getItemAtClick(event)

        # if the mode is edge drag, check if the distance between click and release is enough
        if self.mode == MODE_EDGE_DRAG:
            if self.destanceBetweenClickAndReleaseOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)
        if isinstance(item, QDMGraphicsEdge): logger.debug(f"RBM DEBUG: {item.edge} connecting sockets: {item.edge.start_socket} <--> {item.edge.end_socket}")
        if isinstance(item, QDMGraphicsSocket): logger.debug(f"RBM DEBUG: {item.socket} has edge {item.socket.edge}")

        if item is None:
            logger.debug(f"SCENE: {self.graphicsScene}")
            logger.debug("    NODE:")
            for node in self.graphicsScene.scene.nodes:
                logger.debug(f"        {node}")
            logger.debug("    EDGE:")
            for edge in self.graphicsScene.scene.edges:
                logger.debug(f"        {edge}") 
            return

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.graphicsEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.graphicsEdge.update()
        super().mouseMoveEvent(event)

    def getItemAtClick(self, event):
        """Return the item at the click/release mouse button position"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        logger.debug("Start dragging edge")
        logger.debug(f"    assign Start Socket to: {item.socket}")
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.graphicsScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        logger.debug(f"    dragEdge: {self.dragEdge}")
    
    def edgeDragEnd(self, item) -> bool:
        """Return true if skip the rest of the code"""
        self.mode = MODE_NOOP

        if isinstance(item, QDMGraphicsSocket):
            logger.debug(f"    ~, previous edge: {self.previousEdge}")
            if item.socket.hasEdge():
                item.socket.edge.remove()
            logger.debug(f"    assign End Socket to: {item.socket}")
            if self.previousEdge is not None: self.previousEdge.remove()
            logger.debug("    previous edge removed")
            self.dragEdge.start_socket = self.last_start_socket
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            logger.debug(f"    reassigned start and end sockets to drag edge")
            self.dragEdge.updatePositions()
            return True
        
        logger.debug("End dragging edge")
        self.dragEdge.remove()
        self.dragEdge = None
        logger.debug(f"about to set socket to previous edge: {self.previousEdge}")
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        logger.debug("everything done.")
        return False
    
    def destanceBetweenClickAndReleaseOff(self, event):
        """measure if we are too far form the LMB click scene position"""
        new_lmb_relaese_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_relaese_scene_pos - self.left_lmb_click_scene_pos
        edge_drag_start_threshold_squared = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_start_threshold_squared

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