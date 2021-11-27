from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from fileCardsList import FileCardsList
from mainWindow import MainWindow
from imagesManager import ImagesManager
import config


def main():
    application = QApplication([])
    mainWindow = MainWindow()

    fileCardsList = FileCardsList(mainWindow, lambda: None, lambda: None)
    fileCardsList.addFileCard(config.DEFAULT_PICTURE)
    fileCardsList.addFileCard('photo2.jpg')

    imagesManager = ImagesManager(mainWindow)

    def background():
        mainWindow._background()
        fileCardsList._background()

    backgroundTimer = QTimer()
    backgroundTimer.timeout.connect(background)
    backgroundTimer.start(50)

    mainWindow.showMaximized()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
