from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from previewItem import PreviewItem
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

        self.pic = PreviewItem()
        self.updatePicBorder()
        self.pic.setPixmap(pix)
        self.pic.setX(-pix.width() // 2)
        self.pic.setY(-pix.height() // 2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene_.addItem(self.pic)

        self.upscaled = QGraphicsPixmapItem()
        self.scene_.addItem(self.upscaled)
        self.upscaled.hide()

        self.setScene(self.scene_)


    def setSibling(self, sibling):
        self.pic.setSibling(sibling.pic)

    def updatePicBorder(self):
        self.pic.setBorder(self.width(), self.height())

    def setSceneRectFromSize(self):
        self.scene_.setSceneRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self.setSceneRectFromSize()
        self.updatePicBorder()
        return super(PreviewWidget, self).resizeEvent(event)

    def wheelEvent(self, event):
        pass

    def saveVisable(self, path):
        x = -self.pic.x() // self.SCALE
        y = -self.pic.y() // self.SCALE
        w = self.width() // self.SCALE
        h = self.height() // self.SCALE
        print(x, y, w, h)

        helper.cropImage(self.imagePath, f'{helper.root()}/tmp/preview.jpg', x, y, w, h)

    def showUpscaled(self, path):
        pix = QPixmap(path)
        self.upscaled.setPixmap(pix)
        self.upscaled.show()
        self.pic.setOnMove(lambda: self.upscaled.hide())