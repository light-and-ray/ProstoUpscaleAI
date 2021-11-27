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


    fileCardsList = FileCardsList(mainWindow)
    imagesManager = ImagesManager(mainWindow, fileCardsList)


    fileCardsList.add(config.DEFAULT_PICTURE)
    fileCardsList.add('photo2.jpg')


    def background():
        mainWindow._background()
        fileCardsList._background()
        imagesManager._background()


    backgroundTimer = QTimer()
    backgroundTimer.timeout.connect(background)
    backgroundTimer.start(50)

    mainWindow.showMaximized()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
