from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from mainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    application = MainWindow()
    application.showMaximized()

    sys.exit(app.exec())
