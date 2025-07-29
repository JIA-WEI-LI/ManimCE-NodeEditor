import os
import sys
import inspect
from PyQt5.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import utils.logger

from src.node_editor_window.ui.node_editor_window import NodeEditorWindow
from utils.qss_loader import loadStylesheet

def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window = NodeEditorWindow()
    window.node_editor_widget.addNodes()

    module_path = os.path.dirname(inspect.getfile(window.__class__))
    node_editor_path = os.path.dirname(module_path)
    loadStylesheet(os.path.join(node_editor_path, 'qss', 'nodeeditor.qss'))
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()