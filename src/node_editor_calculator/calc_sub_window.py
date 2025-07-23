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

    def setTitle(self):
        logger.info("Setting title for CalculatorSubWindow")
        self.setWindowTitle(self.getUserFriendlyFilename())
