from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from previewPicture import PreviewPicture
import helper


class PreviewWidget(QGraphicsView):
    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent=parent)


    def setup(self, path, scale=4):
        self.imagePath = path
        self.SCALE = scale
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setMinimumSize(300, 300)

        self.scene_ = QGraphicsScene(parent=self)
        self.setSceneRectFromSize()

        pix = QPixmap(self.imagePath)
        pix = pix.scaledToWidth(pix.width() * self.SCALE, Qt.SmoothTransformation)

        self.picture = PreviewPicture()
        self.updatePicBorder()
        self.picture.setPixmap(pix)
        self.picture.setX(-pix.width() // 2)
        self.picture.setY(-pix.height() // 2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene_.addItem(self.picture)

        self.upscaled = QGraphicsPixmapItem()
        self.scene_.addItem(self.upscaled)
        self.upscaled.hide()

        self.setScene(self.scene_)


    def setSibling(self, sibling):
        self.picture.setSibling(sibling.picture)

    def updatePicBorder(self):
        self.picture.setBorder(self.width(), self.height())

    def setSceneRectFromSize(self):
        self.scene_.setSceneRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self.setSceneRectFromSize()
        self.updatePicBorder()
        return super(PreviewWidget, self).resizeEvent(event)

    def wheelEvent(self, event):
        pass

    def saveVisable(self, path):
        x = -self.picture.x() // self.SCALE
        y = -self.picture.y() // self.SCALE
        w = self.width() // self.SCALE
        h = self.height() // self.SCALE
        print(x, y, w, h)

        helper.cropImage(self.imagePath, path, x, y, w, h)

    def showUpscaled(self, path):
        pix = QPixmap(path)
        self.upscaled.setPixmap(pix)
        self.upscaled.show()
        self.picture.setOnMoveCallback(lambda: self.upscaled.hide())