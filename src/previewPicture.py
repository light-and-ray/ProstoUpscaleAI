from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import helper, config


class PreviewPicture(QGraphicsPixmapItem):
#public:
    def __init__(self):
        super(PreviewPicture, self).__init__()
        self.setSize(0, 0)
        self._sibling = None
        self._onMoveCallback = None
        self.updateLastMove()


    def setSibling(self, sibling):
        self._sibling = sibling


    def setSize(self, width, height):
        self.width = width
        self.height = height
        self._checkBorder()


    def setOnMoveCallback(self, func):
        self._onMoveCallback = func

    def getLastMove(self):
        return self._lastMove

    def updateLastMove(self):
        self._lastMove = helper.currentTime()

#private:

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

    def _isGoodButton(self, button):
        return button in [Qt.LeftButton, Qt.RightButton, Qt.MiddleButton]

    def _move(self, delta):
        self.setPos(self.pos() + delta * config.MOVE_SCALE)
        self._checkBorder()
        self._CallOnMoveCallback()
        self.updateLastMove()

    def mousePressEvent(self, event):
        if self._isGoodButton(event.button()):
            self.startPos = QCursor.pos()

    def mouseMoveEvent(self, event):
        if self._isGoodButton(event.buttons()):
            delta = QCursor.pos() - self.startPos
            self.startPos = QCursor.pos()
            self._move(delta)
            if self._sibling is not None:
                self._sibling._move(delta)

    def _CallOnMoveCallback(self):
        if self._onMoveCallback is not None:
            self._onMoveCallback()
            self._onMoveCallback = None

