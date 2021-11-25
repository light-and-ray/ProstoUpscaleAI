from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from mainWindow import MainWindow
from imagesManager import ImagesManager

def main():
    application = QApplication([])
    mainWindow = MainWindow()

    imagesManager = ImagesManager(mainWindow)

    mainWindow.showMaximized()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
