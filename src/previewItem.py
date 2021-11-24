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
            if self.sibling is not None:
                self.sibling.move(delta)

    def setBorder(self, width, height):
        self.width = width
        self.height = height
        self.checkBorder()

