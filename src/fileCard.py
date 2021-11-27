from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Ui_FileCard import Ui_FileCard
import helper


class FileCard(QFrame):
#public:
    def __init__(self, parent, imagePath, index):
        super(FileCard, self).__init__(parent)
        self.ui = Ui_FileCard()
        self.ui.setupUi(self)
        self.startCancelButton = self.ui.startCancelButton
        self.startCancelButton.clicked.connect(self._start)
        self.removeButton = self.ui.removeButton
        self.removeButton.clicked.connect(self._remove)

        self._onSelect = None
        self._onStart = None
        self._onCancel = None
        self._onRemove = None
        self._imagePath = imagePath
        self._index = index

        height = self.ui.miniature.height()
        pix = QPixmap(imagePath).scaledToHeight(height)
        self.ui.miniature.setPixmap(pix)

        self.ui.filenameLabel.setText(helper.filenameByPath(imagePath))

        self.lastXY = None


    def setOnSelect(self, func):
        self._onSelect = func

    def setOnStart(self, func):
        self._onStart = func

    def setOnCancel(self, func):
        self._onCancel = func

    def setOnRemove(self, func):
        self._onRemove = func


    def setSelectedColor(self):
        pal = QPalette()
        pal.setColor(QPalette.Background, Qt.gray)
        self.setPalette(pal)


    def setUnselectedColor(self):
        pal = QPalette()
        self.setPalette(pal)


    def getImagePath(self):
        return self._imagePath


    def setIndex(self, index):
        self._index = index

#private:

    _startIcon = QIcon.fromTheme('media-playback-start')
    _cancelIcon = QIcon.fromTheme('process-stop')

    def mousePressEvent(self, event):
        self._onSelect(self._index)

    def _start(self):
        self.startCancelButton.clicked.connect(self._cancel)
        self.startCancelButton.setIcon(self._cancelIcon)
        self._onStart()

    def _cancel(self):
        self.startCancelButton.clicked.connect(self._start)
        self.startCancelButton.setIcon(self._startIcon)
        self._onCancel()

    def _remove(self):
        self._onRemove(self._index)