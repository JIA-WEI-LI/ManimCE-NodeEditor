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
        fileMenu = menubar.addMenu(self.tr('&File'))
        fileMenu.addAction(self.createAct(self.tr('&New'), 'Ctrl+N', self.tr("Create new graph"), self.onFileNew))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(self.tr('&Open'), 'Ctrl+O', self.tr("Open file"), self.onFileOpen))
        fileMenu.addAction(self.createAct(self.tr('&Save'), 'Ctrl+S', self.tr("Save file"), self.onFileSave))
        fileMenu.addAction(self.createAct(self.tr('Save &As'), 'Ctrl+Shift+S', self.tr("Save as new file"), self.onFileSaveAs))
        fileMenu.addSeparator()
        fileMenu.addAction(self.createAct(self.tr('&Exit'), 'Ctrl+Q', self.tr("Exit application"), self.close))

        editMenu = menubar.addMenu(self.tr('&Edit'))
        editMenu.addAction(self.createAct(self.tr('&Undo'), 'Ctrl+Z', self.tr("Undo last operation"), self.onEditUndo))
        editMenu.addAction(self.createAct(self.tr('&Redo'), 'Ctrl+Shift+Z', self.tr("Redo last operation"), self.onEditRedo))
        fileMenu.addSeparator()
        editMenu.addAction(self.createAct(self.tr('&Delet'), 'Del', self.tr("Delete selected items"), self.onEditDelete))

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
        self.status_mouse_pos.setText(self.tr("Scene Pos:") + "{ %d , %d }" % (x, y))

    def onFileNew(self):
        self.centralWidget().scene.clear()

    def onFileOpen(self):
        fname, filter = QFileDialog.getOpenFileName(self, self.tr("Open graph from file"))
        if fname == '': return
        if os.path.isfile(fname):
            self.centralWidget().scene.loadFromFile(fname)

    def onFileSave(self):
        if self.filename == None: return self.onFileSaveAs()
        self.centralWidget().scene.saveToFile(self.filename)
        self.statusBar().showMessage(self.tr("Successfully saved") + " %s" % self.filename)

    def onFileSaveAs(self):
        fname, filter = QFileDialog.getSaveFileName(self, self.tr("Save graph to file"))
        if fname == '': return
        self.filename = fname
        self.onFileSave()

    def onEditUndo(self):
        self.centralWidget().scene.history.undo()

    def onEditRedo(self):
        self.centralWidget().scene.history.redo()

    def onEditDelete(self):
        self.centralWidget().scene.graphicsScene.views()[0].deleteSelected()