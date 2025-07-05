import os
import sys
from PyQt5.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import utils.logger

from node_editor.node_editor_window.ui.node_editor_window import NodeEditorWindow

def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window = NodeEditorWindow() 
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()