from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class QDMNodeContentWidget(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget_label = QLabel("Some Title")
        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(QTextEdit("Some content here..."))