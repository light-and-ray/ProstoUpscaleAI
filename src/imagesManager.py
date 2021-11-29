from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

from mainWindow import MainWindow
from fileCardsList import FileCardsList
import helper, config

from upscaler import UpscaleRunner


class ImagesManager:
#public:
    def __init__(self, mainWindow : MainWindow, fileCardsList: FileCardsList):
        self._mainWindow = mainWindow
        self._mainWindow.addImagesButton.clicked.connect(self._onClickedButton)
        self._mainWindow.setOnDrop(self._onDrop)
        self._lastDirectory = config.defaultOpenDirectory

        self._fileCardsList = fileCardsList

        self._upscaler = UpscaleRunner()
        self._fileCardsList.setOnStart(self._onStartUpscale)
        self._fileCardsList.setOnCancel(self._onCancelUpscale)
        self._mainWindow.addOnCloseCallback(self._upscaler.kill)
        self._processingCard = None


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
        lastIndex = None
        for path in paths:
            print('add', path)
            lastIndex = self._fileCardsList.add(path)
        self._fileCardsList.select(lastIndex)
        self._mainWindow.scrollToButtom()


    def _onClickedButton(self):
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


    def _onStartUpscale(self, index):
        print('_onStartUpscale')
        card = self._fileCardsList.at(index)
        pathIn = card.getImagePath()
        self._upscaler.run(card.getUpscaleOptions(), pathIn, pathIn + '_upscaled_4x.jpg')
        self._processingCard = card


    def _onCancelUpscale(self, index):
        print('_onCancelUpscale')
        self._upscaler.kill()
        self._processingCard.progressBar.setValue(0)
        self._processingCard = None


    def _background(self):
        if self._processingCard is not None:
            per = self._upscaler.percents
            if per is not None:
                self._processingCard.progressBar.setValue(int(100*per))

            if self._upscaler.complete():
                self._processingCard.markComplete()
                self._processingCard = None

