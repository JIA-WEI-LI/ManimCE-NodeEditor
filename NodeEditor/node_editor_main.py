import os
import sys
from PyQt5.QtWidgets import QApplication

from NodeEditorWindow.node_editor_window import NodeEditorWindow

def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window = NodeEditorWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()