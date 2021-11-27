from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

from mainWindow import MainWindow
from fileCardsList import FileCardsList
import helper, config



class ImagesManager:
#public:
    def __init__(self, mainWindow : MainWindow, fileCardsList: FileCardsList):
        self._mainWindow = mainWindow
        self._mainWindow.addImagesButton.clicked.connect(self._openImages)
        self._mainWindow.setOnDrop(self._onDrop)
        self._lastDirectory = config.defaultOpenDirectory

        self._fileCardsList = fileCardsList

#private:

    def _selectImageFromDialog(self):
        print(self._lastDirectory)
        anyFilter = 'Any files (*)'
        imageFilter = 'Images (*.jpg *.png *.webp *.jpeg *.gif *.bmp)'
        file = QFileDialog.getOpenFileName(filter=imageFilter, directory=self._lastDirectory)[0]
        print(f'selected {file}')
        self._lastDirectory = os.path.dirname(file)
        return file


    def _addImages(self, paths):
        firstIndex = None
        for path in paths:
            print('add', path)
            i = self._fileCardsList.add(path)
            if firstIndex is None:
                firstIndex = i
        self._fileCardsList.select(firstIndex)
        self._mainWindow.scrollToButtom()


    def _openImages(self):
        path = self._selectImageFromDialog()
        if path == '':
            return
        self._addImages([path])


    def _onDrop(self, event):
        paths = helper.fileUrlToPath(event.mimeData().text()).split('\n')
        paths = filter(lambda x: x != '', map(helper.fileUrlToPath, paths))
        paths = list(paths)
        print('Droped', paths)
        self._addImages(paths)
