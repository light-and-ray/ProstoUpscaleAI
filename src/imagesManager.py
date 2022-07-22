from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

from mainWindow import MainWindow
from fileCardsList import FileCardsList
from fileCard import FileCard
import helper, config

from upscaler import Upscaler


class ImagesManager:
#public:
    def __init__(self, mainWindow : MainWindow, fileCardsList: FileCardsList):
        self._mainWindow = mainWindow
        self._mainWindow.addImagesButton.clicked.connect(self._onClickedButton)
        self._mainWindow.setOnDrop(self._onDrop)
        self._mainWindow.setOnPaste(self._onPaste)
        self._lastDirectory = config.defaultOpenDirectory

        self._fileCardsList = fileCardsList

        self._upscaler = Upscaler()
        self._fileCardsList.setOnStart(self._onStartUpscale)
        self._fileCardsList.setOnCancel(self._onCancelUpscale)
        self._fileCardsList.setOnComplete(self._onCompleteUpscale)
        self._fileCardsList.setOnRemove(self._onRemoveCard)

        self._mainWindow.addOnCloseCallback(self._upscaler.kill)
        self._processingCard = None
        self._queue : list[FileCard] = []


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
        paths = event.mimeData().text().split('\n')
        paths = filter(lambda x: x != '', map(helper.fileUrlToPath, paths))
        paths = list(paths)
        print('Droped', paths)
        self._addImages(paths)


    def _onPaste(self, text):
        paths = text.split('\n')
        paths = filter(lambda x: x != '', map(helper.fileUrlToPath, paths))
        paths = list(paths)
        print('Pasted', paths)
        self._addImages(paths)



    def _onStartUpscale(self, index):
        print('_onStartUpscale')
        self._queue.append(self._fileCardsList.at(index))
        if len(self._queue) == 1:
            self._upscale(index)


    def _upscale(self, index):
        card = self._fileCardsList.at(index)
        self._processingCard = card
        pathIn = card.getImagePath()
        self._upscaler.run(card.getUpscaleOptions(), pathIn, pathIn + '_upscaled_4x.jpg')


    def _onCancelUpscale(self, index):
        print('_onCancelUpscale')
        card = self._fileCardsList.at(index)
        self._processingCard = None

        self._upscaler.kill()

        card.progressBar.setValue(0)
        if self._queue[0].index() == index:
            self._nextQueue(index)
        else:
            self._removeFromQueue(index)


    def _onCompleteUpscale(self, index):
        print('_onCompleteUpscale')
        self._processingCard = None
        self._nextQueue(index)


    def _onRemoveCard(self, index):
        self._removeFromQueue(index)


    def _nextQueue(self, index):
        self._removeFromQueue(index)
        if len(self._queue) == 0:
            return
        self._upscale(self._queue[0].index())


    def _removeFromQueue(self, index):
        for element in self._queue:
            if element.index() == index:
                self._queue.remove(element)
                return


    def _background(self):
        if self._processingCard is not None:
            per = self._upscaler.getPercents()
            if per is not None:
                self._processingCard.progressBar.setValue(int(100*per))

            if self._upscaler.complete():
                self._processingCard.markComplete()

