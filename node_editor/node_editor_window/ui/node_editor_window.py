import os
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QLabel

from .. import __version__
from .node_editor_widget import NodeEditorWidget

class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

        self.filename = None

    def createAct(self, name:str, shortcut:str, tooltip:str, callback):
        act = QAction(name, self)
        act.setShortcut(shortcut)
        act.setToolTip(tooltip)
        act.triggered.connect(callback)
        return act

    def initUI(self):
        menubar = self.menuBar()

        # initialize menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.createAct('&New', 'Ctrl+N', "Create new graph", self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Open', 'Ctrl+O', "Open file", self.onFileOpen))
        fileMenu.addAction(self.createAct('&Save', 'Ctrl+S', "Save file", self.onFileSave))
        fileMenu.addAction(self.createAct('Save &As', 'Ctrl+Shift+S', "Save as new file", self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct('&Exit', 'Ctrl+Q', "Exit application", self.close))

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(self.createAct('&Undo', 'Ctrl+Z', "Undo last operation", self.onEditUndo))
        editMenu.addAction(self.createAct('&Redo', 'Ctrl+Shift+Z', "Redo last operation", self.onEditRedo))
        fileMenu.addSeparator()
        editMenu.addAction(self.createAct('&Delet', 'Del', "Delete selected items", self.onEditDelete))

        node_editor_widget = NodeEditorWidget(self)
        self.setCentralWidget(node_editor_widget)

        # status bar
        self.statusBar().showMessage("")
        self.status_mouse_pos = QLabel("")
        self.statusBar().addPermanentWidget(self.status_mouse_pos)
        node_editor_widget.view.scenePosChanged.connect(self.onScenePosChanged)

        # set window properties
        self.setGeometry(200,200,800,600)
        self.setWindowTitle(f"Node Editor v {__version__}")
        self.show()

    def onScenePosChanged(self, x:int, y:int):
        self.status_mouse_pos.setText("Scene Pos: { %d , %d }" % (x, y))

    def onFileNew(self):
        self.centralWidget().scene.clear()

    def onFileOpen(self):
        fname, filter = QFileDialog.getOpenFileName(self, "Open graph from file")
        if fname == '': return
        if os.path.isfile(fname):
            self.centralWidget().scene.loadFromFile(fname)

    def onFileSave(self):
        if self.filename == None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage("Successfully saved %s" % self.filename)

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, "Save graph to file")
        if fname == '': return
        self.filename = fname
        self.onFileSave()

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.graphicsScene.views()[0].deleteSelected()