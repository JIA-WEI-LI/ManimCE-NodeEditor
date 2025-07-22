import sys
from PyQt5.QtWidgets import QApplication

from node_editor_calculator.calc_window import CalculatorWindow

def main():
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    window = CalculatorWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()