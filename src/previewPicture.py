from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PreviewPicture(QGraphicsPixmapItem):
    def __init__(self):
        super(PreviewPicture, self).__init__()
        self.setBorder(0, 0)
        self.sibling = None
        self.onMove_ = None

    def setSibling(self, sibling):
        self.sibling = sibling

    def _checkBorder(self):
        x = lambda: self.x()
        y = lambda: self.y()
        minX = self.width - self.pixmap().width()
        minY = self.height - self.pixmap().height()
        maxX = 0
        maxY = 0
        if (x() < minX):
            self.setPos(minX, y())
        elif (x() > maxX):
            self.setPos(maxX, y())

        if (y() < minY):
            self.setPos(x(), minY)
        elif (y() > maxY):
            self.setPos(x(), maxY)

    MOVE_SCALE = 3

    def _needMove(self, button):
        return button in [Qt.LeftButton, Qt.RightButton, Qt.MiddleButton, Qt.Key_Space]

    def _move(self, delta):
        self.setPos(self.pos() + delta * self.MOVE_SCALE)
        self._checkBorder()
        self._onMove()

    def mousePressEvent(self, event):
        if self._needMove(event.button()):
            self.startPos = QCursor.pos()

    def mouseMoveEvent(self, event):
        if self._needMove(event.buttons()):
            delta = QCursor.pos() - self.startPos
            self.startPos = QCursor.pos()
            self._move(delta)
            if self.sibling is not None:
                self.sibling._move(delta)

    def setBorder(self, width, height):
        self.width = width
        self.height = height
        self._checkBorder()

    def setOnMove(self, func):
        self.onMove_ = func

    def _onMove(self):
        if self.onMove_ is not None:
            self.onMove_()
            self.onMove_ = None

