from PyQt5.QtCore import *
from node_editor_window.ui.node_editor_widget import NodeEditorWidget

class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setTitle()

        self.scene.addHasBeenModifiedListener(self.setTitle)


    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())
