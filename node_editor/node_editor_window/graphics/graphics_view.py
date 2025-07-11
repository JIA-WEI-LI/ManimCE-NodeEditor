import os, sys
import pprint
import logging
logger = logging.getLogger(__name__)

from PyQt5.QtWidgets import QGraphicsView, QApplication
from PyQt5.QtGui import QPainter, QMouseEvent, QKeyEvent
from PyQt5.QtCore import Qt, QEvent, pyqtSignal

from ..core.edge import Edge, EDGE_TYPE_BEZIER
from ..graphics.graphics_cutline import QDMCutLine
from ..graphics.graphics_socket import QDMGraphicsSocket
from ..graphics.graphics_edge import QDMGraphicsEdge

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

EDGE_DRAG_START_THRESHOLD = 10

class QDMGraphicsView(QGraphicsView):
    scenePosChanged = pyqtSignal(int, int)

    def __init__(self, graphicsScene, parent=None):
        super().__init__(parent=parent)

        self.graphicsScene = graphicsScene

        self.initUI()

        self.setScene(self.graphicsScene)

        self.mode = MODE_NOOP
        self.editingFlag = False
        self.rubberBandDragginRectangle = False

        self.zoomInFator = 1.25
        self.zoomClamp = False
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        # cutline
        self.cutline = QDMCutLine()
        self.graphicsScene.addItem(self.cutline)

    def initUI(self):
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                           QPainter.RenderHint.HighQualityAntialiasing |
                           QPainter.RenderHint.TextAntialiasing |
                           QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

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
    
    def middleMouseButtonPress(self, event: QMouseEvent):
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

    def middleMouseButtonRelease(self, event: QMouseEvent):
        fakeEvent = QMouseEvent(event.type(), 
                                event.localPos(), 
                                event.screenPos(),  
                                Qt.MouseButton.LeftButton,
                                event.buttons() | -Qt.MouseButton.LeftButton,
                                event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    def leftMouseButtonPress(self, event: QMouseEvent):
        # get the which we click mouse button
        item = self.getItemAtClick(event)

        self.left_lmb_click_scene_pos = self.mapToScene(event.pos())
        logger.debug(f"LMB Click on item: {item} - {self.debug_modifiers(event)}")

        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    QEvent.Type.MouseButtonPress,
                    event.localPos(),
                    event.screenPos(),
                    Qt.MouseButton.LeftButton,
                    event.buttons() | Qt.MouseButton.LeftButton,
                    event.modifiers() | Qt.KeyboardModifier.ControlModifier
                )
                super().mousePressEvent(fakeEvent)
                return
                
        if isinstance(item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return
        
        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        if item is None:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(
                    QEvent.Type.MouseButtonRelease,
                    event.localPos(),
                    event.screenPos(),
                    Qt.MouseButton.LeftButton,
                    Qt.MouseButton.NoButton,
                    event.modifiers()
                )
                QApplication.setOverrideCursor(Qt.CursorShape.CrossCursor)
                return 
            else:
                self.rubberBandDragginRectangle = True
            
        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event: QMouseEvent):
        # get the which we release mouse button
        item = self.getItemAtClick(event)

        if hasattr(item, "node") or isinstance(item, QDMGraphicsEdge) or item is None:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    event.type(),
                    event.localPos(),
                    event.screenPos(),
                    Qt.MouseButton.LeftButton,
                    Qt.MouseButton.NoButton,
                    event.modifiers() | Qt.KeyboardModifier.ControlModifier
                )
                super().mouseReleaseEvent(fakeEvent)
                return
        
        if self.mode == MODE_EDGE_DRAG:
            if self.destanceBetweenClickAndReleaseOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges(event)
            self.cutline.line_points = []
            self.cutline.update()
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.mode = MODE_NOOP
            return 
        
        if self.rubberBandDragginRectangle:
            self.graphicsScene.scene.history.storeHistory("Selection changed")
            self.rubberBandDragginRectangle = False

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event: QMouseEvent):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)
        if isinstance(item, QDMGraphicsEdge): logger.debug(f"RBM DEBUG: {item.edge} connecting sockets: {item.edge.start_socket} <--> {item.edge.end_socket}")
        if isinstance(item, QDMGraphicsSocket): logger.debug(f"RBM DEBUG: {item.socket} has edges:\n{pprint.pformat(item.socket.edges)}")

        if item is None:
            logger.debug(f"SCENE: {self.graphicsScene}")
            logger.debug("    NODE:")
            for node in self.graphicsScene.scene.nodes:
                logger.debug(f"        {node}")
            logger.debug("    EDGE:")
            for edge in self.graphicsScene.scene.edges:
                logger.debug(f"        {edge}") 
            return

    def rightMouseButtonRelease(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.graphicsEdge.setDestination(pos.x(), pos.y())
            self.drag_edge.graphicsEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        self.last_scene_mouse_pos = self.mapToScene(event.pos())
        self.scenePosChanged.emit(
            int(self.last_scene_mouse_pos.x()),
            int(self.last_scene_mouse_pos.y())
        )

        super().mouseMoveEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        # save_path = os.path.abspath(
        #     os.path.join(os.path.dirname(__file__), "..", "..", "saves", "graph.json")
        # )
        # if event.key() == Qt.Key.Key_Delete:
        #     if not self.editingFlag:
        #         self.deleteSelected()
        #     else: 
        #         super().keyPressEvent(event)
        # elif event.key() == Qt.Key.Key_S and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # self.graphicsScene.scene.saveToFile(save_path)
        # elif event.key() == Qt.Key.Key_L and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # self.graphicsScene.scene.loadFromFile(save_path)
        # elif event.key() == Qt.Key.Key_Z and event.modifiers() & Qt.KeyboardModifier.ControlModifier and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
        #     self.graphicsScene.scene.history.undo()
        # elif event.key() == Qt.Key.Key_Z and event.modifiers() & Qt.KeyboardModifier.ControlModifier and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
        #     self.graphicsScene.scene.history.redo()
        if event.key() == Qt.Key.Key_H:
             logger.debug(f"HISTORY:    len({len(self.graphicsScene.scene.history.history_stack)}) -- current_step {self.graphicsScene.scene.history.history_current_step}")
             logger.debug(f"  * Estimated memory usage per item: {sys.getsizeof(self.graphicsScene.scene.serialize())}")
             ix = 0
             for item in self.graphicsScene.scene.history.history_stack:
                 logger.debug(f"# {ix} -- {item['desc']}")
                 ix += 1
        # else:
        super().keyPressEvent(event)

    def cutIntersectingEdges(self, event):
        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.graphicsScene.scene.edges:
                if edge.graphicsEdge.intersectsWith(p1, p2):
                    edge.remove()

        self.graphicsScene.scene.history.storeHistory("Delete cutted edges", setModified=True)

    def deleteSelected(self):
        for item in self.graphicsScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif hasattr(item, "node"):
                item.node.remove()

        self.graphicsScene.scene.history.storeHistory("Delete selected", setModified=True)

    def debug_modifiers(self, event):
        out = "KEYS: "
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier: out += "SHIFT "
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier: out += "CTRL "
        if event.modifiers() & Qt.KeyboardModifier.AltModifier: out += "ALT "
        return out

    def getItemAtClick(self, event):
        """Return the item at the click/release mouse button position"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        logger.debug("Start dragging edge")
        logger.debug(f"    assign Start Socket to: {item.socket}")
        # self.previousEdge = item.socket.edge
        self.drag_start_socket = item.socket
        self.drag_edge = Edge(self.graphicsScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        logger.debug(f"    dragEdge: {self.drag_edge}")
    
    def edgeDragEnd(self, item) -> bool:
        """Return true if skip the rest of the code"""
        self.mode = MODE_NOOP

        logger.debug("End dragging edge")
        self.drag_edge.remove()
        self.drag_edge = None

        if isinstance(item, QDMGraphicsSocket):
            if item.socket != self.drag_start_socket:
                # logger.debug(f"    ~, previous edge: {self.previousEdge}")
                # if item.socket.hasEdge():
                #     item.socket.edge.remove()

                # for edge in item.socket.edges:
                #     edge.remove()
                if item.socket != self.drag_start_socket:
                    if not item.socket.is_multi_edges:
                        item.socket.removeAllEdges()
                    if not self.drag_start_socket.is_multi_edges:
                        self.drag_start_socket.removeAllEdges()

                    new_edge = Edge(
                        self.graphicsScene.scene,
                        self.drag_start_socket,
                        item.socket,
                        edge_type=EDGE_TYPE_BEZIER
                    )
                    logger.debug(f"    create a new Edge: {new_edge} connecting {new_edge.start_socket} <--> {new_edge.end_socket} ")

                # logger.debug(f"    assign End Socket to: {item.socket}")
                # if self.previousEdge is not None: self.previousEdge.remove()
                # logger.debug("    previous edge removed")
                # self.drag_edge.start_socket = self.drag_start_socket
                # self.drag_edge.end_socket = item.socket
                # self.drag_edge.start_socket.addEdge(self.drag_edge)
                # self.drag_edge.end_socket.addEdge(self.drag_edge)
                # logger.debug(f"    reassigned start and end sockets to drag edge")
                # self.drag_edge.updatePositions()
                # store history

                self.graphicsScene.scene.history.storeHistory("Create new edge by dragging", setModified=True)
                return True
        
        # logger.debug(f"about to set socket to previous edge: {self.previousEdge}")
        # if self.previousEdge is not None:
        #     self.previousEdge.start_socket.edge = self.previousEdge
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