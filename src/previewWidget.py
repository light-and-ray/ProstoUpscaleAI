from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from previewPicture import PreviewPicture
import helper, config


class PreviewWidget(QGraphicsView):
#public:
    def __init__(self, parent):
        super(PreviewWidget, self).__init__(parent=parent)
        self.setAcceptDrops(False)

        self._zoom = 4
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.setMinimumSize(300, 300)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._scene = QGraphicsScene(parent=self)
        self._setSceneRectFromSize()

        self._lastXY = None
        self.imagePath = None
        self.picture = PreviewPicture(self.updateLastXY)
        self.picture.updateLastMove()
        self._updatePicBorder()
        self._scene.addItem(self.picture)

        self.upscaled = QGraphicsPixmapItem()
        self._scene.addItem(self.upscaled)
        self.upscaled.hide()

        self.blackout = QGraphicsPixmapItem()
        self._scene.addItem(self.blackout)
        self.blackout.setOpacity(config.BLACKOUT_OPACITY)
        self.blackout.hide()

        self.setScene(self._scene)

        self.updateLastXY()


    def setPicture(self, path):
        self.imagePath = path
        if path is not None:
            pix = QPixmap(self.imagePath)
            pix = pix.scaledToWidth(pix.width() * self._zoom, Qt.SmoothTransformation)

            self.picture.setPixmap(pix)
            self.picture.setX(-pix.width() // 2)
            self.picture.setY(-pix.height() // 2)
            self.updateLastXY()
        else:
            pix = QPixmap()
            self.picture.setPixmap(pix)


    def setSibling(self, sibling):
        self.picture.setSibling(sibling.picture)


    def save(self, path):
        x = -self.picture.x() // self._zoom
        y = -self.picture.y() // self._zoom
        w = self.width() // self._zoom
        h = self.height() // self._zoom
        print(x, y, w, h)

        helper.cropImage(self.imagePath, path, x, y, w, h)


    def showUpscaled(self, path):
        pix = QPixmap(path).scaledToHeight(self.height(), Qt.SmoothTransformation)
        self.upscaled.setPixmap(pix)
        self.upscaled.show()
        self.picture.setOnMoveCallback(lambda: self.upscaled.hide())

    def showBlackout(self):
        pix = QPixmap(self.width(), self.height())
        painter = QPainter()
        painter.begin(pix)
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0))
        painter.end()
        self.blackout.setPixmap(pix)
        self.blackout.show()

    def hideBlackout(self):
        self.blackout.hide()


    def getLastXY(self):
        return self._lastXY

    def updateLastXY(self):
        self._lastMove = helper.currentTime()
        self._lastXY = (-self.picture.x() / self._zoom, -self.picture.y() / self._zoom)

    def setXY(self, x, y):
        self._lastXY = (x, y)
        self.picture.setX(-x * self._zoom)
        self.picture.setY(-y * self._zoom)

#private:

    def _updatePicBorder(self):
        self.picture.setSize(self.width(), self.height())

    def _setSceneRectFromSize(self):
        self._scene.setSceneRect(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        self._setSceneRectFromSize()
        self._updatePicBorder()
        return super(PreviewWidget, self).resizeEvent(event)

    def wheelEvent(self, event):
        pass

