import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

from ..serialization.serializable import Serializable

class QDMNodeContentWidget(QWidget, Serializable):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget_label = QLabel("Some Title")
        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(QDMTextEdit("Some content here..."))

    def setEditingFlag(self, value):
        self.node.scene.graphicsScene.views()[0].editingFlag = value

    def serialize(self):
        return OrderedDict([
        ])
    
    def deserialize(self, data, hashmap={}):
        return False

class QDMTextEdit(QTextEdit):
    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)