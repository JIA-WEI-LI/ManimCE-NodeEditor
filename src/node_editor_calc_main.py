import os, sys
from PyQt5.QtWidgets import QApplication

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
import utils.logger

from node_editor_calculator.calc_window import CalculatorWindow

def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    app.setStyle('Fusion')
    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()