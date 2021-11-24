from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class PreviewItem(QGraphicsPixmapItem):
    def __init__(self):
        super(PreviewItem, self).__init__()
        self.setBorder(0, 0)
        self.sibling = None

    def setSibling(self, sibling):
        self.sibling = sibling

    def checkBorder(self):
        x = lambda: self.x()
        y = lambda: self.y()
        if (x() < self.minX):
            self.setPos(self.minX, y())
        elif (x() > self.maxX):
            self.setPos(self.maxX, y())

        if (y() < self.minY):
            self.setPos(x(), self.minY)
        elif (y() > self.maxY):
            self.setPos(x(), self.maxY)

    MOVE_SCALE = 3

    def needMove(self, button):
        return button in [Qt.LeftButton, Qt.RightButton, Qt.MiddleButton, Qt.Key_Space]

    def move(self, delta):
        self.setPos(self.pos() + delta * self.MOVE_SCALE)
        self.checkBorder()

    def mousePressEvent(self, event):
        if self.needMove(event.button()):
            self.startPos = QCursor.pos()

    def mouseMoveEvent(self, event):
        if self.needMove(event.buttons()):
            delta = QCursor.pos() - self.startPos
            self.startPos = QCursor.pos()
            self.move(delta)
            self.sibling.move(delta)

        # print(f'mouseMoveEvent: minX = {self.minX}, minY = {self.minY}, x = {x()}',
        #     f'y = {y()}, maxX = {self.maxX}, maxY = {self.maxY}')

    def setBorder(self, width, height):
        self.minX = 0 - self.pixmap().width() + width
        self.minY = 0 - self.pixmap().height() + height
        self.maxX = 0
        self.maxY = 0
        self.checkBorder()

