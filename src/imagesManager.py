from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

from mainWindow import MainWindow
import helper



class ImagesManager:

    DEFAULT_DIRECTORY = os.environ['HOME']

    def __init__(self, mainWindow : MainWindow):
        self._mainWindow = mainWindow
        self._mainWindow.addImagesButton.clicked.connect(self.addImages)
        self._mainWindow.setOnDrop(self._onDrop)
        self._lastDirectory = self.DEFAULT_DIRECTORY


    def addImages(self):
        path = self._selectImage()
        if path != '':
            self._mainWindow.setPicture(path)

    def _selectImage(self):
        print(self._lastDirectory)
        anyFilter = 'Any files (*)'
        imageFilter = 'Images (*.jpg *.png *.webp *.jpeg *.gif *.bmp)'
        file = QFileDialog.getOpenFileName(filter=imageFilter, directory=self._lastDirectory)[0]
        print(f'selected {file}')
        self._lastDirectory = os.path.dirname(file)
        return file

    def _onDrop(self, event):
        print('Droped:', event.mimeData().text())
        path = helper.fileUrlToPath(event.mimeData().text())
        print(f'Opening {path}')
        self._mainWindow.setPicture(path)

