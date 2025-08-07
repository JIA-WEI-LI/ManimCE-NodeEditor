import logging
logger = logging.getLogger(__name__)

from PyQt5.QtCore import *
from node_editor_window.ui.node_editor_widget import NodeEditorWidget

class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)

        self._close_event_listeners = []

    def setTitle(self):
        logger.info("Setting title for CalculatorSubWindow")
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)
