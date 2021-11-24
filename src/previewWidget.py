from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from previewItem import PreviewItem


class PreviewWidget(QGraphicsView):
    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent=parent)


    def setup(self, path, scale):
        self.SCALE = scale
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setMinimumSize(300, 300)

        self.scene = QGraphicsScene(parent=self)
        self.setSceneRectFromSize()

        pix = QPixmap(path)
        pix = pix.scaledToWidth(pix.width() * self.SCALE, Qt.SmoothTransformation)

        self.pic = PreviewItem()
        self.updatePicBorder()
        self.pic.setPixmap(pix)
        self.pic.setX(-pix.width() // 2)
        self.pic.setY(-pix.height() // 2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene.addItem(self.pic)
        self.setScene(self.scene)


    def setSibling(self, sibling):
        self.pic.setSibling(sibling.pic)

    def updatePicBorder(self):
        self.pic.setBorder(self.width(), self.height())

    def setSceneRectFromSize(self):
        self.scene.setSceneRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self.setSceneRectFromSize()
        self.updatePicBorder()
        return super(PreviewWidget, self).resizeEvent(event)

    def wheelEvent(self, event):
        pass
