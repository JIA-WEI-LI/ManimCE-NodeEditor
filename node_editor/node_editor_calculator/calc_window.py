from PyQt5.QtWidgets import QMainWindow, QMdiArea, QWidget
from PyQt5.QtCore import Qt, QSignalMapper

from node_editor_window.ui.node_editor_window import NodeEditorWindow

class CalculatorWindow(NodeEditorWindow):
    def initUI(self):
        self.name_company = "Blenderfreak"
        self.name_product = "Calculator NodeEditor"

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.ViewMode.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()
        self.setWindowTitle("Calculator NodeEditor Example")

    def createActions(self):
        pass

    def createMenus(self):
        pass

    def createToolBars(self):
        pass

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def updateMenus(self):
        pass

    def readSettings(self):
        pass

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)
