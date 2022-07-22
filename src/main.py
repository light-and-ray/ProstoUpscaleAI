from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from fileCardsList import FileCardsList
from mainWindow import MainWindow
from imagesManager import ImagesManager
import errorHandling
import helper, config


def main():
    application = QApplication([])
    mainWindow = MainWindow()


    fileCardsList = FileCardsList(mainWindow)
    imagesManager = ImagesManager(mainWindow, fileCardsList)


    for image in helper.listDirImages(f'{config.root}/src/testImages'):
        fileCardsList.add(image)


    def background():
        mainWindow._background()
        fileCardsList._background()
        imagesManager._background()
        errorHandling.instance.handle()

    backgroundTimer = QTimer()
    backgroundTimer.timeout.connect(background)
    backgroundTimer.start(50)
    helper.mkdir(config.tmp)

    mainWindow.showMaximized()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
