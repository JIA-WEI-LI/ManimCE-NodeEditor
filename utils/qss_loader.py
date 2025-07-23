import logging
logger = logging.getLogger(__name__)

from PyQt5.QtCore import QFile, QDir
from PyQt5.QtWidgets import QApplication

def fix_qt_path(path: str) -> str:
    return QDir.toNativeSeparators(path).replace("\\", "/")

def loadStylesheet(filename):
    logger.info(f"STYLE loading: {filename}")
    file = QFile(filename)
    file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

def loadStylesheets(*args):
    res = ''
    for arg in args:
        file = QFile(fix_qt_path(arg))
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        stylesheet = file.readAll()
        res += "\n" + str(stylesheet, encoding='utf-8')
    QApplication.instance().setStyleSheet(res)

# def loadStylesheets(*args):
#     res = ''
#     for arg in args:
#         with open(arg, 'r', encoding='utf-8') as f:
#             res += "\n" + f.read()
#     QApplication.instance().setStyleSheet(res)

