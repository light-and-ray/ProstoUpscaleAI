from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_FileCard import Ui_FileCard
from upscaler import UpscaleOptions
import helper, config


class FileCard(QPushButton):
#public:
    def __init__(self, parent, imagePath, index):
        super(FileCard, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred))
        self.setBaseSize(600, 80)
        self.ui = Ui_FileCard()
        self.ui.setupUi(self)
        self.setCheckable(True)
        self._selected = False

        self.startCancelButton = self.ui.startCancelButton
        self.startCancelButton.clicked.connect(self._start)
        self.removeButton = self.ui.removeButton
        self.removeButton.clicked.connect(self._remove)

        self._onSelect = None
        self._onStart = None
        self._onCancel = None
        self._onComplete = None
        self._onRemove = None
        self._imagePath = imagePath
        self._upscaleOptions = UpscaleOptions(imagePath, helper.dirOfFile(imagePath))
        self._upscaleOptions.setDenoiseLevel(0.4)
        self._upscaleOptions.setPreScale(0.7)
        self._index = index

        self._updateMiniature()

        self.ui.filenameLabel.setText(helper.filenameByPath(imagePath))
        self.lastXY = None

        self.progressBar = self.ui.progressBar
        self.progressBar.setMaximum(100*100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)


    def setOnSelect(self, func):
        self._onSelect = func

    def setOnStart(self, func):
        self._onStart = func

    def setOnCancel(self, func):
        self._onCancel = func

    def setOnComplete(self, func):
        self._onComplete = func

    def setOnRemove(self, func):
        self._onRemove = func


    def setSelectedColor(self):
        if self._selected == False:
            self._selected = True
            self.toggle()


    def setUnselectedColor(self):
        if self._selected == True:
            self._selected = False
            self.toggle()


    def getImagePath(self):
        return self._imagePath

    def getUpscaleOptions(self):
        return self._upscaleOptions


    def setIndex(self, index):
        self._index = index

    def index(self):
        return self._index


    def markComplete(self):
        self._setReadyState()
        self._onComplete(self._index)


#private:

    _startIcon = QIcon.fromTheme('media-playback-start')
    _cancelIcon = QIcon.fromTheme('process-stop')

    def mousePressEvent(self, event):
        self._onSelect(self._index)


    def _remove(self):
        self._onRemove(self._index)


    def _setProcessingState(self):
        self.startCancelButton.clicked.disconnect()
        self.startCancelButton.clicked.connect(self._cancel)
        self.startCancelButton.setIcon(self._cancelIcon)
        self.removeButton.hide()

    def _setReadyState(self):
        self.startCancelButton.clicked.disconnect()
        self.startCancelButton.clicked.connect(self._start)
        self.startCancelButton.setIcon(self._startIcon)
        self.removeButton.show()

    def _start(self):
        self._setProcessingState()
        self._onStart(self._index)

    def _cancel(self):
        self._setReadyState()
        self._onCancel(self._index)

    def _updateMiniature(self):
        height = self.ui.miniature.height()
        width = self.ui.miniature.width()
        pix = QPixmap(self._imagePath).scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ui.miniature.setPixmap(pix)

    def resizeEvent(self, event):
        self._updateMiniature
        super(FileCard, self).resizeEvent(event)
